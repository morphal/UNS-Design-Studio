# factory.py
# Royal Farmers Collective – Enterprise UNS Simulator (FULLY DYNAMIC)

import asyncio
import os as _os
import signal
import threading
import logging
import random
import json
import socket
import time
import datetime
from opcua import Server, ua

logging.getLogger('opcua').setLevel(logging.ERROR)
logging.basicConfig(level=logging.WARN)

# ================================================================
# CONFIG
# ================================================================
def _load_server_cfg():
    cfg_path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'server_config.json')
    try:
        with open(cfg_path) as f:
            return json.load(f)
    except Exception:
        return {}

_scfg = _load_server_cfg()
_OPC_BIND_IP    = _scfg.get('opc_bind_ip',    '0.0.0.0')   # Important: 0.0.0.0
_OPC_PORT       = int(_scfg.get('opc_port',   4840))
_TCP_PORT       = int(_scfg.get('tcp_port',   9999))
_HOST_IP        = (_scfg.get('host_ip') or '').strip()
_OPC_CLIENT_HOST = (_scfg.get('opc_client_host') or '').strip()

def _resolve_endpoint_host() -> str:
    # 0.0.0.0 is valid for binding but not for client connections.
    if _HOST_IP:
        return _HOST_IP
    if _OPC_CLIENT_HOST:
        return _OPC_CLIENT_HOST
    if _OPC_BIND_IP and _OPC_BIND_IP != '0.0.0.0':
        return _OPC_BIND_IP
    return '127.0.0.1'

SERVER_ENDPOINT = f"opc.tcp://{_resolve_endpoint_host()}:{_OPC_PORT}/freeopcua/server/"
NAMESPACE_URI   = "http://royalfarmerscollective.com/uns"
TCP_SERVER_IP   = "0.0.0.0"
TCP_SERVER_PORT = _TCP_PORT

stop_flag = False
anomaly_overrides = {}

# ================================================================
# SIMULATION PROFILES
# ================================================================
SIMULATION_PROFILES = {
    "oee":          {"type": "gauss_walk", "base": 92.0, "std": 2.5,  "min": 65.0, "max": 99.5},
    "percent":      {"type": "gauss_walk", "base": 85.0, "std": 3.0,  "min": 0.0,  "max": 100.0},
    "temperature":  {"type": "gauss_walk", "base": 75.0, "std": 1.8,  "min": 20.0, "max": 180.0},
    "accumulator":  {"type": "increment",  "step_min": 0.05, "step_max": 2.5},
    "boolean":      {"type": "toggle",     "probability": 0.08},
    "truck_id":     {"type": "string_cycle"},
    "default":      {"type": "gauss_walk", "base": 50.0, "std": 8.0,  "min": 0.0,  "max": 100.0},
}

def _load_uns_config():
    path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'uns_config.json')
    with open(path, encoding='utf-8') as f:
        return json.load(f)

# ================================================================
# DYNAMIC OPC-UA BUILDER
# ================================================================
def _create_dynamic_address_space(server, idx, enterprise_obj):
    cfg = _load_uns_config()
    tree = cfg['tree']
    variables = {}
    anomaly_key_map = {}

    def _walk(node, uns_parts, opc_parts, area_opc_parts):
        ntype = node.get('type', '')
        name = node.get('name', '')
        opc_name = ('Factory' + name) if ntype == 'site' else name

        new_uns = uns_parts + [name]
        new_opc = opc_parts + [opc_name]
        new_area = new_opc if ntype == 'area' else area_opc_parts

        for tag in node.get('tags', []):
            t_name = tag['name']
            t_opc_name = tag.get('opcNodeName', t_name)
            data_type = tag.get('dataType', 'Float')

            if 'opcPath' in tag:
                rel = tag['opcPath'].split('/')
                target_opc = new_area + rel
            else:
                target_opc = new_opc + [t_opc_name]

            # Navigate or create only the parent objects for this variable.
            # The final segment is the variable name itself.
            current = enterprise_obj
            parent_parts = target_opc[:-1]
            var_name = target_opc[-1]
            for part in parent_parts:
                try:
                    current = current.get_child([f"{idx}:{part}"])
                except:
                    current = current.add_object(idx, part)

            # Create variable
            if data_type == 'Float':
                default = 0.0
                vt = ua.VariantType.Double
            elif data_type == 'Int':
                default = 0
                vt = ua.VariantType.Int64
            elif data_type == 'Bool':
                default = False
                vt = ua.VariantType.Boolean
            elif data_type == 'String':
                default = ""
                vt = ua.VariantType.String
            elif data_type == 'DateTime':
                default = datetime.datetime.now(datetime.UTC)  # Fixed deprecation
                vt = ua.VariantType.DateTime
            else:
                default = 0.0
                vt = ua.VariantType.Double

            var = current.add_variable(idx, var_name, default, vt)
            var.set_writable(str(tag.get('access', 'R')).upper() == 'RW')

            sim = tag.get('simulation')
            if not sim or not isinstance(sim, dict):
                sim = {"profile": "default"}
            elif "profile" not in sim:
                sim["profile"] = "default"

            variables[tuple(target_opc)] = (var, sim)
            anomaly_key = "".join(target_opc)
            anomaly_key_map[anomaly_key] = var

        for child in node.get('children', []):
            _walk(child, new_uns, new_opc, new_area)

    for child in tree.get('children', []):
        _walk(child, [], [], [])
    print(f"[factory] Dynamic address space ready - {len(variables)} tags")
    return variables, anomaly_key_map

# ================================================================
# SIMULATOR
# ================================================================
async def run_simulation(variables, anomaly_key_map):
    while not stop_flag:
        for opc_path, (var, sim) in list(variables.items()):
            try:
                current = var.get_value()
                anomaly_key = "".join(opc_path)

                if anomaly_key in anomaly_overrides and anomaly_overrides[anomaly_key] is not None:
                    var.set_value(anomaly_overrides[anomaly_key])
                    continue

                profile = SIMULATION_PROFILES.get(sim.get("profile"), SIMULATION_PROFILES["default"])

                if profile["type"] == "gauss_walk":
                    std = sim.get("std", profile["std"])
                    new_val = current + random.gauss(0, std)
                    new_val = max(sim.get("min", profile.get("min", 0)),
                                  min(sim.get("max", profile.get("max", 9999)), new_val))
                    var.set_value(float(new_val))

                elif profile["type"] == "increment":
                    step = random.uniform(profile["step_min"], profile["step_max"])
                    var.set_value(current + step)

                elif profile["type"] == "toggle":
                    if random.random() < profile["probability"]:
                        var.set_value(not bool(current))

                elif profile["type"] == "string_cycle" and isinstance(current, str):
                    if random.random() < 0.07:
                        var.set_value(f"TRK-{random.randint(10000,99999)}")

            except Exception:
                pass

        await asyncio.sleep(1.2)

# ================================================================
# TCP Anomaly Server
# ================================================================
def handle_client(client_socket_arg):
    global anomaly_overrides
    try:
        data = client_socket_arg.recv(1024).decode('utf-8')
        if data:
            payload = json.loads(data)
            overrides = payload.get('anomaly_overrides')
            if overrides is not None:
                anomaly_overrides.update(overrides)
    except Exception:
        pass
    finally:
        client_socket_arg.close()

def start_tcp_server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((TCP_SERVER_IP, TCP_SERVER_PORT))
        s.listen(5)
        print(f"[factory] Anomaly TCP server listening on {TCP_SERVER_IP}:{TCP_SERVER_PORT}")
        while not stop_flag:
            client, _ = s.accept()
            threading.Thread(target=handle_client, args=(client,), daemon=True).start()
    except Exception as e:
        print(f"[factory] TCP server error: {e}")

# ================================================================
# Shutdown
# ================================================================
def signal_handler(_sig, _frame):
    global stop_flag
    stop_flag = True
    print("[factory] Shutdown signal received...")

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ================================================================
# MAIN
# ================================================================
async def main():
    global stop_flag
    server = Server()
    server.set_endpoint(SERVER_ENDPOINT)
    server.set_server_name("Royal Farmers Collective UNS Simulator")
    
    idx = server.register_namespace(NAMESPACE_URI)
    objects = server.get_objects_node()
    enterprise_obj = objects.add_object(idx, "RoyalFarmersCollective")

    variables, anomaly_key_map = _create_dynamic_address_space(server, idx, enterprise_obj)

    server.start()
    print(f"[factory] OPC UA Server started on {SERVER_ENDPOINT}")

    # Give the server a moment to fully initialize the socket
    await asyncio.sleep(1.5)

    asyncio.create_task(run_simulation(variables, anomaly_key_map))

    print("=" * 70)
    print("    Royal Farmers Collective - Enterprise UNS Simulator")
    print("    OPC UA Server is RUNNING")
    print(f"    Endpoint: {SERVER_ENDPOINT}")
    print("=" * 70)
    print("[factory] Ready for client connections - simulation active")

    try:
        while not stop_flag:
            await asyncio.sleep(1)
    finally:
        server.stop()
        print("[factory] Server stopped.")

if __name__ == "__main__":
    threading.Thread(target=start_tcp_server, daemon=True).start()
    asyncio.run(main())
