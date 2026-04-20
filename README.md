<div align="center">

# 🏭 Virtual UNS Enterprise Simulator

**A fully self-contained Unified Namespace simulator for industrial IoT demos, training and development.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](docker-compose.yml)
[![OPC-UA](https://img.shields.io/badge/OPC--UA-4840-green)](https://opcfoundation.org/)
[![MQTT](https://img.shields.io/badge/MQTT-1883-orange)](https://mqtt.org/)
[![NATS](https://img.shields.io/badge/NATS-4222-purple)](https://nats.io/)

*Simulate a complete multi-site food manufacturing enterprise — publishing realistic, stateful OT and IT data over OPC-UA, MQTT and NATS — without needing a single piece of real hardware.*

[Quick Start](#-quick-start) · [Features](#-features) · [UNS Designer](#-uns-topic-designer) · [Simulation Engine](#-simulation-engine) · [API Reference](#-api-reference) · [Release Notes](#-release-notes)

</div>

---

## 🎯 What is this?

The **Virtual UNS Enterprise Simulator** is a hands-on learning and demo environment for anyone working with **Unified Namespace (UNS)** architecture, **ISA-95 hierarchy**, **OPC-UA**, **MQTT/NATS** and **industrial data modelling**.

It ships with a fictional five-division food manufacturer — 13 factories across Europe — all producing coherent, realistic process data driven by a proper plant state machine. No random noise. No hardcoded tags. Everything is configurable through a visual browser-based designer.

**Built for:**
- Engineers learning UNS and ISA-95 concepts hands-on
- Teams evaluating MQTT brokers, NATS or time-series databases
- Demonstrating IIoT architecture to stakeholders without real equipment
- Testing Grafana dashboards, Telegraf pipelines or digital twin tooling

---

## ✨ Features

### Simulation
- **Stateful plant engine** — each factory runs a full state machine: `Running → Fault → Recovery → Stopped`. Every tag derives from the same coherent plant state — never independent random values
- **44 simulation profiles** spanning the full IT/OT stack: OEE pillars, process variables, maintenance/CMMS, quality lab, logistics, ERP/finance and energy utilities
- **OEE always computed correctly** as `Availability × Performance × Quality / 10000`
- **Accumulators** (energy, good output, bad output, revenue) only advance when the plant is running
- **Silo levels** drain during production and auto-refill on simulated truck arrivals
- **String tags** publish meaningful values — batch IDs, lot IDs, truck IDs, order statuses, ERP numbers

### UNS Designer
- **Visual ISA-95 hierarchy editor** — build Enterprise → Business Unit → Site → Area → Work Center trees in the browser
- **Asset library** — 16 predefined asset bundles (Pump, Valve, Silo, Boiler, Packing Machine, IQF Tunnel, Conveyor, Batch Reactor, Weighbridge, Quality Lab, CMMS Feed, ERP Feed, Energy Meter, Fryer, Drum Dryer, Crystallizer) — drop any asset onto any node, tags and profiles pre-wired
- **Grouped simulation profile picker** with contextual hints per profile
- **Live topic path preview** — see your full MQTT/NATS topic as you build
- **Payload Schema Designer** — define your own message schemas (Standard, Sparkplug B-like, ISA-95 Extended, PI-like, InfluxDB-like)

### Connectivity
- **OPC-UA server** — full address space built dynamically from your UNS config
- **MQTT and NATS bridge** — configurable polling interval, topic prefix and payload schema
- **Dynamic enterprise name** — dashboard header and topic examples update live when you rename the root node

### Infrastructure
- **Docker-first** — single `docker compose up` gets everything running
- **Persistent config volume** — namespace, schemas and asset library survive container rebuilds
- **REST API** — every feature accessible programmatically

---

## 🏢 The Example Enterprise

The simulator ships with **GlobalFoodCo** — a fictional food manufacturing holding. Rename it to anything you like in the UNS designer — the dashboard and topic paths update automatically.

| Division | Product | Factories |
|---|---|---|
| 🥔 **CrispCraft** | Chips & Snacks | Antwerp, Ghent |
| 🌾 **FlakeMill** | Potato Flakes | Leiden, Groningen |
| 🍟 **FrostLine** | Frozen Frites | Dortmund, Bremen, Hanover, Leipzig, Cologne, Dresden |
| 🌿 **RootCore** | Chicory & Inulin | Lille |
| 🍬 **SugarWorks** | Sugar Beet & Sugar | Bruges, Liege |

> All names, divisions and locations are entirely fictional.

---

## 🚀 Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) with Docker Compose
- Ports **5000** (dashboard), **4840** (OPC-UA) and **9999** (anomaly TCP) available on your host

### 1 — Clone

```bash
git clone https://github.com/your-username/virtual-uns-simulator.git
cd virtual-uns-simulator
```

### 2 — Build

```bash
docker build -t uns-simulator:latest .
```

### 3 — Run

```bash
docker compose up -d
```

### 4 — Open

```
http://localhost:5000
```

The OPC-UA server starts automatically. All 13 factories boot in **Running** state and immediately begin publishing data. The MQTT/NATS bridge is off by default — configure and start it from the dashboard when ready.

---

## 🔌 Connecting a Broker

### MQTT

1. Dashboard → **Bridge** tab
2. Set protocol to `mqtt`, enter your broker host and port (default `1883`)
3. Click **Start Bridge**

Topics are structured as:
```
GlobalFoodCo/CrispCraft/Antwerp/ProductionLine/OEE/OEEPercent
```

### NATS

Set protocol to `nats` and port to `4222`. Subjects use `.` separators:
```
GlobalFoodCo.CrispCraft.Antwerp.ProductionLine.OEE.OEEPercent
```

### TimescaleDB via Telegraf

Use the Telegraf MQTT consumer input plugin with topic filter `GlobalFoodCo/#`. The ISA-95 topic hierarchy maps directly to `L1`–`L6` hierarchy columns in the `mqtt_consumer_tag` table.

---

## 🎨 UNS Topic Designer

Open the designer at `http://localhost:5000/uns`.

### Building a namespace from scratch

1. Click **+ Node** in the left panel to add a child under any node
2. Set the node **Type** — Enterprise, Business Unit, Site, Area, Work Center, Work Unit or Device
3. Switch to the **Tags** tab to add data points

### Inserting an asset bundle

The fastest way to populate a node with realistic tags:

1. Select a node in the tree
2. Click **🧩 Insert Asset Bundle** in the Tags tab
3. Filter by category and click an asset card to preview its tags
4. Click **Insert Tags** — the full bundle drops in with profiles already configured

### Assigning simulation profiles

Click the **Simulation Profile** cell on any tag row. Profiles are grouped by domain:

| Domain | Example profiles |
|---|---|
| **OT / Process** | `oee` · `availability` · `performance` · `quality` · `motor_current` · `vibration` · `flow_rate` · `level` · `pressure` · `temperature_process` |
| **Accumulators** | `accumulator_good` · `accumulator_bad` · `accumulator_energy` · `counter_faults` |
| **Maintenance / CMMS** | `mtbf` · `mttr` · `pm_compliance` · `remaining_useful_life` · `corrective_wo_count` |
| **Quality / Lab** | `quality_metric_cont` · `quality_metric_pct` · `quality_hold` · `batch_id` · `lot_id` |
| **Logistics** | `silo_level` · `truck_id` · `days_of_supply` · `inbound_tons` · `order_status` |
| **ERP / Finance** | `erp_order_id` · `revenue_eur` · `production_cost_eur` · `margin_pct` |
| **Energy / Utilities** | `power_kw` · `steam_flow` · `compressed_air` · `co2_kg` · `accumulator_energy` |

Each profile shows a hint explaining its behaviour — e.g. *"Drops sharply during fault, climbs during recovery"* for `availability`.

---

## 🧠 Simulation Engine

Each factory runs an independent `PlantState` object. Every tag derives its value purely from the assigned simulation profile and the plant's current state — no tag names are hardcoded anywhere.

```
                    ┌──────────────────────────────────┐
                    ▼                                  │
  ┌─────────┐   fault    ┌───────┐   repaired   ┌──────────┐
  │ Running │───────────►│ Fault │─────────────►│ Recovery │
  └─────────┘            └───────┘              └──────────┘
       ▲                                              │
       └──────────────────── ready ───────────────────┘

  ┌─────────┐   start command
  │ Stopped │────────────────────────────────────────► Recovery
  └─────────┘
```

**What happens during a Fault:**
- Availability collapses; OEE follows
- Flow rate and speed drop to zero
- Motor current spikes; vibration rises
- Power drops to ~12% (standby only)
- All accumulators pause

**What happens during Recovery:**
- Availability and performance climb back gradually
- Power ramps up
- On completion: corrective work order closes, RUL may reset (simulating a PM event)

**Per-division parameters** seed realistic base values per division — a FrostLine frozen frites plant (820 kW base, 28 t/h infeed) naturally behaves differently from a SugarWorks beet processing plant (1185 kW base, 95 t/h infeed).

---

## 📁 Project Structure

```
virtual-uns-simulator/
│
├── factory.py            # OPC-UA server + stateful simulation engine
├── bridge.py             # OPC-UA → MQTT / NATS bridge
├── app.py                # Flask web application + REST API
├── recipe.py             # Product recipe data per division
├── client.py             # Optional CLI client for direct OPC-UA access
│
├── uns_config.json       # ISA-95 namespace definition (editable via UI)
├── sim_state.json        # Runtime plant running/stopped state
├── asset_library.json    # Predefined asset tag bundles
├── payload_schemas.json  # MQTT/NATS payload format definitions
├── bridge_config.json    # Bridge connection settings
├── server_config.json    # OPC-UA server endpoint configuration
│
├── templates/
│   ├── index.html            # Main dashboard
│   ├── uns_editor.html       # UNS Topic Designer
│   └── payload_schemas.html  # Payload Schema Designer
│
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh         # First-boot config seeding + symlinks
└── requirements.txt
```

---

## ⚙️ Configuration Reference

### `server_config.json`

```json
{
  "opc_bind_ip":     "0.0.0.0",
  "opc_port":        4840,
  "opc_client_host": "127.0.0.1",
  "tcp_port":        9999,
  "host_ip":         "127.0.0.1"
}
```

> Set `host_ip` to your Docker host's LAN IP to allow OPC-UA clients on other machines to connect.

### `bridge_config.json`

```json
{
  "protocol":     "mqtt",
  "broker_host":  "127.0.0.1",
  "broker_port":  1883,
  "topic_prefix": "",
  "interval":     2
}
```

> Set `protocol` to `"nats"` and `broker_port` to `4222` for NATS mode.

### Persistent volume

On first boot, `entrypoint.sh` seeds all JSON config files into the `uns-data` Docker volume. Subsequent container rebuilds do not overwrite your customised namespace or schemas.

---

## 🔧 Running Without Docker

```bash
pip install -r requirements.txt
```

```bash
# Terminal 1 — OPC-UA simulator
python factory.py

# Terminal 2 — Dashboard
python app.py

# Terminal 3 — Bridge (optional)
python bridge.py
```

Dashboard available at `http://localhost:5000`.

---

## 📦 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/status` | Server status, plant states, bridge stats, enterprise name |
| `GET` | `/api/uns` | Current UNS namespace configuration |
| `POST` | `/api/uns` | Save UNS config (triggers factory restart) |
| `GET` | `/api/asset-library` | Full asset template library |
| `GET` | `/api/simulation-profiles` | Grouped simulation profile catalogue |
| `GET` | `/api/payload-schemas` | Payload schema definitions |
| `POST` | `/api/payload-schemas` | Save payload schemas |
| `POST` | `/api/server/start` | Start OPC-UA factory server |
| `POST` | `/api/server/stop` | Stop OPC-UA factory server |
| `POST` | `/api/bridge/start` | Start MQTT/NATS bridge |
| `POST` | `/api/bridge/stop` | Stop bridge |
| `GET` | `/api/bridge/config` | Get bridge configuration |
| `POST` | `/api/bridge/config` | Save bridge configuration |
| `POST` | `/api/plant/start` | Start a specific plant |
| `POST` | `/api/plant/stop` | Stop a specific plant |
| `GET` | `/api/opc/test` | Diagnose OPC-UA connectivity |

---

## 🗂️ Release Notes

### v3.0 — Stateful Profile Engine *(current)*

- **Complete rewrite of the simulation engine** — replaced independent random walks with a coherent per-plant state machine (Running / Fault / Recovery / Stopped)
- **44 simulation profiles** — all plant-state-aware, covering OT, CMMS, quality, logistics, ERP and energy
- **16-asset library** — predefined bundles with profiles pre-wired, insertable from the UNS designer in one click
- **Dynamic enterprise name** — dashboard header reads the UNS tree root name live
- **Profile dropdown** dynamically loaded from the factory engine — always in sync, grouped by domain with contextual hints
- **New API endpoints** — `/api/asset-library`, `/api/simulation-profiles`
- **OEE always `A × P × Q / 10000`** — never independently randomised
- **String tags publish meaningful values** — truck IDs, batch IDs, lot IDs, order statuses, ERP numbers
- **Accumulators gate on plant state** — pause during fault and stop
- **Silo auto-refill** on simulated truck arrival when level drops below 20%
- **Finance accumulators** — revenue, production cost, waste cost and margin track coherently from output rates
- **Backward compatible** — existing profile names (`oee`, `percent`, `temperature`, `accumulator`, `boolean`, `truck_id`) continue to work via legacy aliases

### v2.0 — Dynamic Address Space

- `uns_config.json`-driven OPC-UA address space — no hardcoded tag names
- Visual UNS Topic Designer with full ISA-95 node type support
- Payload Schema Designer with Standard, Sparkplug B-like, ISA-95 Extended, PI-like and InfluxDB-like presets
- Canonical tag inheritance — all plants in a division share the reference tag set automatically
- Per-plant start/stop control via `sim_state.json`
- NATS native mode added to the bridge
- Anomaly injection via TCP socket

### v1.0 — Initial Release

- OPC-UA server with static address space
- MQTT bridge with configurable polling interval
- Flask dashboard with factory status overview
- Basic Gaussian walk simulation for all tags
- Docker support

---

## 🤝 Contributing

1. Fork the repo and create a feature branch: `git checkout -b feature/my-improvement`
2. Commit your changes: `git commit -m 'Add XYZ'`
3. Push and open a pull request

**Adding a simulation profile:** add the profile to both `_profile_value()` in `factory.py` and the `SIMULATION_PROFILES` dict — the dict populates the UNS designer dropdown automatically.

**Adding an asset template:** add an entry to `asset_library.json` following the existing structure. It appears in the asset picker immediately on next page load.

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">

*GlobalFoodCo and all associated divisions, factories and products are entirely fictional.*
*Built to make UNS concepts tangible for engineers who learn by doing.*

</div>
