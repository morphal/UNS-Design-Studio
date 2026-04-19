# recipe.py
# Royal Farmers Collective – fictief Europees agrifood concern (parodie)
# Productnamen en receptgegevens zijn volledig fictief.
#
# Concern:  Royal Farmers Collective
# Divisies:
#   KnappertjesBV   – chips & snacks          (parodie op Duynie)
#   Vlokkenheim     – aardappelvlokken         (parodie op Rixona)
#   FritoMaxx       – diepvriesfrites          (parodie op Aviko)
#   Wortelkracht    – cichorei & inuline       (parodie op Sensus)
#   DeBietenBende   – suikerbieten & suiker    (parodie op Cosun Beet Company)

from enum import Enum

class Recipe(Enum):
    # ── KnappertjesBV – chips & snacks ──────────────────────────────────────
    KNAPPER_NATUREL      = "Knappertjes Naturel Kettle"
    KNAPPER_PAPRIKA      = "Knappertjes Paprika Crunch"
    KNAPPER_ZEEZOUT      = "Knappertjes Zeezout & Azijn"

    # ── Vlokkenheim – aardappelvlokken ───────────────────────────────────────
    VLOK_KLASSIEK        = "Vlokkenheim Klassieke Pureevlok"
    VLOK_INSTANT         = "Vlokkenheim Instantvlok Fijn"

    # ── FritoMaxx – diepvriesfrites ──────────────────────────────────────────
    FRITO_CLASSIC        = "FritoMaxx Huisfrites 10mm"
    FRITO_STEAKHOUSE     = "FritoMaxx Steakhouse 14mm"
    FRITO_WEDGE          = "FritoMaxx Potato Wedge Gekruid"

    # ── Wortelkracht – cichorei & inuline ────────────────────────────────────
    INULINE_STANDAARD    = "Wortelkracht Inuline Standaard"
    INULINE_HP           = "Wortelkracht Inuline HP (Lange Keten)"

    # ── De BietenBende – suiker ───────────────────────────────────────────────
    BIET_KRISTAL         = "BietenBende Kristalsuiker Wit"
    BIET_BASTERD         = "BietenBende Basterdsuiker Fijn"


def get_enum_by_value(value):
    for recipe in Recipe:
        if recipe.value == value:
            return recipe
    return None


recipe_data = {

    # ════════════════════════════════════════════════════════════════════════
    # KnappertjesBV – chips & snacks
    # Fabrieken: FactoryTerneuzen (kettle-lijn), FactoryBergenOpZoom (flats)
    # Grondstof: verse consumptieaardappelen → snijden → frituren → kruiden
    # ════════════════════════════════════════════════════════════════════════
    Recipe.KNAPPER_NATUREL: {
        'group': 'KnappertjesBV',
        'infeed_rate': 25.0,            # t/h verse aardappelen
        'good_ratio': 0.90,
        'cutter_speed_sp': 0.9,         # m/s snijblad
        'blancher_temp_sp': 78.0,       # °C blancheren
        'fryer_temp_sp': 172.0,         # °C frituurolietemperatuur
        'freezer_temp_sp': -30.0,       # °C koelingtunnel
        'outbound_rate': 8.5,           # t/h chips uit
        'base_power_kw': 720.0,
        'quality_targets': {
            'metric1': 21.0,            # droogstofgehalte %
            'metric2': 0.55,            # vrij vet g/kg
            'metric3': 64.0,            # kleur L* waarde
        },
    },
    Recipe.KNAPPER_PAPRIKA: {
        'group': 'KnappertjesBV',
        'infeed_rate': 23.0,
        'good_ratio': 0.91,
        'cutter_speed_sp': 0.85,
        'blancher_temp_sp': 80.0,
        'fryer_temp_sp': 175.0,
        'freezer_temp_sp': -30.0,
        'outbound_rate': 8.0,
        'base_power_kw': 730.0,
        'quality_targets': {
            'metric1': 22.0,
            'metric2': 0.50,
            'metric3': 62.0,
        },
    },
    Recipe.KNAPPER_ZEEZOUT: {
        'group': 'KnappertjesBV',
        'infeed_rate': 24.0,
        'good_ratio': 0.89,
        'cutter_speed_sp': 0.88,
        'blancher_temp_sp': 79.0,
        'fryer_temp_sp': 173.0,
        'freezer_temp_sp': -30.0,
        'outbound_rate': 8.2,
        'base_power_kw': 710.0,
        'quality_targets': {
            'metric1': 21.5,
            'metric2': 0.58,
            'metric3': 63.0,
        },
    },

    # ════════════════════════════════════════════════════════════════════════
    # Vlokkenheim – aardappelvlokken
    # Fabrieken: FactoryEmmeloord, FactoryVeendam
    # Grondstof: stoomgekookte aardappelen → pureren → trommeldroog → vlokken
    # ════════════════════════════════════════════════════════════════════════
    Recipe.VLOK_KLASSIEK: {
        'group': 'Vlokkenheim',
        'infeed_rate': 35.0,            # t/h gekookte aardappelmassa
        'good_ratio': 0.96,
        'drum_dryer_speed_sp': 0.8,     # RPM trommel
        'drum_temp_sp': 158.0,          # °C trommeloppervlak
        'outbound_rate': 8.2,           # t/h droge vlokken
        'base_power_kw': 610.0,
        'quality_targets': {
            'metric1': 91.5,            # droogstof %
        },
    },
    Recipe.VLOK_INSTANT: {
        'group': 'Vlokkenheim',
        'infeed_rate': 32.0,
        'good_ratio': 0.97,
        'drum_dryer_speed_sp': 0.7,
        'drum_temp_sp': 153.0,
        'outbound_rate': 7.8,
        'base_power_kw': 585.0,
        'quality_targets': {
            'metric1': 93.0,
        },
    },

    # ════════════════════════════════════════════════════════════════════════
    # FritoMaxx – diepvriesfrites
    # Fabrieken: FactoryHeerenveen, FactoryHarlingen, FactoryMeppel,
    #            FactoryHardenberg, FactoryHoogeveen, FactoryCoevorden
    # Grondstof: frites-aardappelen → schillen → snijden → blancheren →
    #            voorfrituren → invriezen (IQF-tunnel)
    # ════════════════════════════════════════════════════════════════════════
    Recipe.FRITO_CLASSIC: {
        'group': 'FritoMaxx',
        'infeed_rate': 30.0,            # t/h rauwe frites-aardappelen
        'good_ratio': 0.93,
        'cutter_speed_sp': 1.2,         # m/s snijblad
        'blancher_temp_sp': 85.0,       # °C blancher
        'fryer_temp_sp': 180.0,         # °C voorfrituurtemperatuur
        'freezer_temp_sp': -35.0,       # °C IQF-tunnel
        'outbound_rate': 26.0,          # t/h diepvriesfrites
        'base_power_kw': 820.0,
        'quality_targets': {
            'metric1': 23.0,            # droogstof %
            'metric2': 0.40,            # vrij vet g/kg
            'metric3': 68.0,            # kleur L* waarde
        },
    },
    Recipe.FRITO_STEAKHOUSE: {
        'group': 'FritoMaxx',
        'infeed_rate': 28.0,
        'good_ratio': 0.95,
        'cutter_speed_sp': 1.1,
        'blancher_temp_sp': 88.0,
        'fryer_temp_sp': 185.0,
        'freezer_temp_sp': -38.0,
        'outbound_rate': 24.5,
        'base_power_kw': 860.0,
        'quality_targets': {
            'metric1': 24.0,
            'metric2': 0.32,
            'metric3': 70.0,
        },
    },
    Recipe.FRITO_WEDGE: {
        'group': 'FritoMaxx',
        'infeed_rate': 26.0,
        'good_ratio': 0.91,
        'cutter_speed_sp': 0.8,
        'blancher_temp_sp': 82.0,
        'fryer_temp_sp': 178.0,
        'freezer_temp_sp': -36.0,
        'outbound_rate': 22.0,
        'base_power_kw': 780.0,
        'quality_targets': {
            'metric1': 22.5,
            'metric2': 0.48,
            'metric3': 65.0,
        },
    },

    # ════════════════════════════════════════════════════════════════════════
    # Wortelkracht – cichorei & inuline
    # Fabriek: FactoryRoosendaal
    # Grondstof: cichoreiwortels → extractie → zuivering → sproeidroging
    # ════════════════════════════════════════════════════════════════════════
    Recipe.INULINE_STANDAARD: {
        'group': 'Wortelkracht',
        'infeed_rate': 40.0,            # t/h cichoreisap
        'good_ratio': 0.88,
        'extraction_temp_sp': 80.0,     # °C extractietemperatuur
        'outbound_rate': 6.2,           # t/h inulinepoeder
        'base_power_kw': 710.0,
        'quality_targets': {
            'metric1': 94.5,            # zuiverheid %
        },
    },
    Recipe.INULINE_HP: {
        'group': 'Wortelkracht',
        'infeed_rate': 35.0,
        'good_ratio': 0.90,
        'extraction_temp_sp': 75.0,
        'outbound_rate': 5.2,
        'base_power_kw': 660.0,
        'quality_targets': {
            'metric1': 96.5,
        },
    },

    # ════════════════════════════════════════════════════════════════════════
    # De BietenBende – suikerbieten & suiker
    # Fabrieken: FactoryZevenbergen, FactoryStadskanaal
    # Grondstof: suikerbieten → diffusie → verdamping → kristallisatie
    # ════════════════════════════════════════════════════════════════════════
    Recipe.BIET_KRISTAL: {
        'group': 'DeBietenBende',
        'infeed_rate': 100.0,           # t/h bietensap
        'good_ratio': 0.85,
        'diffusion_temp_sp': 70.0,      # °C diffusietoren
        'evaporator_temp_sp': 120.0,    # °C verdamper
        'crystallizer_temp_sp': 80.0,   # °C kristallisator
        'outbound_rate': 15.0,          # t/h kristalsuiker
        'base_power_kw': 1250.0,
        'quality_targets': {
            'metric1': 99.7,            # polarisatie (zuiverheid %)
            'metric2': 45.0,            # kleur ICUMSA
        },
    },
    Recipe.BIET_BASTERD: {
        'group': 'DeBietenBende',
        'infeed_rate': 90.0,
        'good_ratio': 0.82,
        'diffusion_temp_sp': 68.0,
        'evaporator_temp_sp': 118.0,
        'crystallizer_temp_sp': 77.0,
        'outbound_rate': 13.5,
        'base_power_kw': 1120.0,
        'quality_targets': {
            'metric1': 98.5,
            'metric2': 200.0,
        },
    },
}
