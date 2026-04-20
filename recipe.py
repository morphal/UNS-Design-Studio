# recipe.py
# Virtual UNS Enterprise Simulator – fictional food manufacturing concern
# Productnamen en receptgegevens zijn volledig fictief.
#
# Concern:  GlobalFoodCo
# Divisies:
#   CrispCraft   – chips & snacks          (fictional chips division)
#   FlakeMill     – aardappelvlokken         (fictional flakes division)
#   FrostLine       – diepvriesfrites          (fictional frites division)
#   RootCore    – cichorei & inuline       (fictional inulin division)
#   SugarWorks   – suikerbieten & suiker    (fictional sugar division)

from enum import Enum

class Recipe(Enum):
    # ── CrispCraft – chips & snacks ──────────────────────────────────────
    KNAPPER_NATUREL      = "Knappertjes Naturel Kettle"
    KNAPPER_PAPRIKA      = "Knappertjes Paprika Crunch"
    KNAPPER_ZEEZOUT      = "Knappertjes Zeezout & Azijn"

    # ── FlakeMill – aardappelvlokken ───────────────────────────────────────
    VLOK_KLASSIEK        = "FlakeMill Klassieke Pureevlok"
    VLOK_INSTANT         = "FlakeMill Instantvlok Fijn"

    # ── FrostLine – diepvriesfrites ──────────────────────────────────────────
    FRITO_CLASSIC        = "FrostLine Huisfrites 10mm"
    FRITO_STEAKHOUSE     = "FrostLine Steakhouse 14mm"
    FRITO_WEDGE          = "FrostLine Potato Wedge Gekruid"

    # ── RootCore – cichorei & inuline ────────────────────────────────────
    INULINE_STANDAARD    = "RootCore Inuline Standaard"
    INULINE_HP           = "RootCore Inuline HP (Lange Keten)"

    # ── SugarWorks – suiker ───────────────────────────────────────────────
    BIET_KRISTAL         = "BietenBende Kristalsuiker Wit"
    BIET_BASTERD         = "BietenBende Basterdsuiker Fijn"


def get_enum_by_value(value):
    for recipe in Recipe:
        if recipe.value == value:
            return recipe
    return None


recipe_data = {

    # ════════════════════════════════════════════════════════════════════════
    # CrispCraft – chips & snacks
    # Fabrieken: FactoryAntwerp (kettle-lijn), FactoryGhent (flats)
    # Grondstof: verse consumptieaardappelen → snijden → frituren → kruiden
    # ════════════════════════════════════════════════════════════════════════
    Recipe.KNAPPER_NATUREL: {
        'group': 'CrispCraft',
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
        'group': 'CrispCraft',
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
        'group': 'CrispCraft',
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
    # FlakeMill – aardappelvlokken
    # Fabrieken: FactoryLeiden, FactoryGroningen
    # Grondstof: stoomgekookte aardappelen → pureren → trommeldroog → vlokken
    # ════════════════════════════════════════════════════════════════════════
    Recipe.VLOK_KLASSIEK: {
        'group': 'FlakeMill',
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
        'group': 'FlakeMill',
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
    # FrostLine – diepvriesfrites
    # Fabrieken: FactoryDortmund, FactoryBremen, FactoryHanover,
    #            FactoryLeipzig, FactoryCologne, FactoryDresden
    # Grondstof: frites-aardappelen → schillen → snijden → blancheren →
    #            voorfrituren → invriezen (IQF-tunnel)
    # ════════════════════════════════════════════════════════════════════════
    Recipe.FRITO_CLASSIC: {
        'group': 'FrostLine',
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
        'group': 'FrostLine',
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
        'group': 'FrostLine',
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
    # RootCore – cichorei & inuline
    # Fabriek: FactoryLille
    # Grondstof: cichoreiwortels → extractie → zuivering → sproeidroging
    # ════════════════════════════════════════════════════════════════════════
    Recipe.INULINE_STANDAARD: {
        'group': 'RootCore',
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
        'group': 'RootCore',
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
    # SugarWorks – suikerbieten & suiker
    # Fabrieken: FactoryBruges, FactoryLiege
    # Grondstof: suikerbieten → diffusie → verdamping → kristallisatie
    # ════════════════════════════════════════════════════════════════════════
    Recipe.BIET_KRISTAL: {
        'group': 'SugarWorks',
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
        'group': 'SugarWorks',
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
