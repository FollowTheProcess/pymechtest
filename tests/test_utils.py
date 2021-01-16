"""
Collection of fixture-like data structures and other helpful
things for testing that can't easily be fixtures.

Placed here so as not to clutter main test files.

Author: Tom Fleet
Created: 16/01/2021
"""

from pathlib import Path

import pandas as pd

# Data for testing & development only
TENS_NO_YIELD = Path(__file__).parent.resolve().joinpath("data/Tens_No_Yield")
TENS_YIELD = Path(__file__).parent.resolve().joinpath("data/Tens_Yield")
# Same as TENS_YIELD but with specimen ID removed to test exception handling
NO_IDS = Path(__file__).parent.resolve().joinpath("data/No_IDs")

paths = [f for f in TENS_YIELD.rglob("*.csv")] + [
    f for f in TENS_NO_YIELD.rglob("*.csv")
]

paths_and_specimen_ids = [
    (TENS_NO_YIELD.joinpath("Specimen_RawData_1.csv"), "0038"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_2.csv"), "0031"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_3.csv"), "0040"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_4.csv"), "0032"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_5.csv"), "0033"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_6.csv"), "0034"),
    (TENS_YIELD.joinpath("Specimen_RawData_1.csv"), "009"),
    (TENS_YIELD.joinpath("Specimen_RawData_2.csv"), "008"),
    (TENS_YIELD.joinpath("Specimen_RawData_3.csv"), "007"),
    (TENS_YIELD.joinpath("Specimen_RawData_4.csv"), "006"),
    (TENS_YIELD.joinpath("Specimen_RawData_5.csv"), "005"),
    (TENS_YIELD.joinpath("Specimen_RawData_6.csv"), "004"),
]

paths_and_filenames = [
    (TENS_NO_YIELD.joinpath("Specimen_RawData_1.csv"), "Specimen_RawData_1.csv"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_2.csv"), "Specimen_RawData_2.csv"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_3.csv"), "Specimen_RawData_3.csv"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_4.csv"), "Specimen_RawData_4.csv"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_5.csv"), "Specimen_RawData_5.csv"),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_6.csv"), "Specimen_RawData_6.csv"),
    (TENS_YIELD.joinpath("Specimen_RawData_1.csv"), "Specimen_RawData_1.csv"),
    (TENS_YIELD.joinpath("Specimen_RawData_2.csv"), "Specimen_RawData_2.csv"),
    (TENS_YIELD.joinpath("Specimen_RawData_3.csv"), "Specimen_RawData_3.csv"),
    (TENS_YIELD.joinpath("Specimen_RawData_4.csv"), "Specimen_RawData_4.csv"),
    (TENS_YIELD.joinpath("Specimen_RawData_5.csv"), "Specimen_RawData_5.csv"),
    (TENS_YIELD.joinpath("Specimen_RawData_6.csv"), "Specimen_RawData_6.csv"),
]

paths_for_no_id_test = [
    (NO_IDS.joinpath("Specimen_RawData_1.csv")),
    (NO_IDS.joinpath("Specimen_RawData_2.csv")),
    (NO_IDS.joinpath("Specimen_RawData_3.csv")),
    (NO_IDS.joinpath("Specimen_RawData_4.csv")),
    (NO_IDS.joinpath("Specimen_RawData_5.csv")),
    (NO_IDS.joinpath("Specimen_RawData_6.csv")),
    (NO_IDS.joinpath("Specimen_RawData_7.csv")),
    (NO_IDS.joinpath("Specimen_RawData_8.csv")),
    (NO_IDS.joinpath("Specimen_RawData_9.csv")),
    (NO_IDS.joinpath("Specimen_RawData_10.csv")),
]

paths_and_moduli_no_yield = [
    (TENS_NO_YIELD.joinpath("Specimen_RawData_1.csv"), 214.74),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_10.csv"), 227.93),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_2.csv"), 222.73),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_3.csv"), 226.24),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_4.csv"), 227.21),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_5.csv"), 237.50),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_6.csv"), 230.00),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_7.csv"), 210.58),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_8.csv"), 201.60),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_9.csv"), 222.34),
]

paths_and_moduli_yield = [
    (TENS_YIELD.joinpath("Specimen_RawData_10.csv"), 171.04),
    (TENS_YIELD.joinpath("Specimen_RawData_1.csv"), 177.04),
    (TENS_YIELD.joinpath("Specimen_RawData_2.csv"), 190.01),
    (TENS_YIELD.joinpath("Specimen_RawData_3.csv"), 174.27),
    (TENS_YIELD.joinpath("Specimen_RawData_4.csv"), 154.95),
    (TENS_YIELD.joinpath("Specimen_RawData_5.csv"), 178.21),
    (TENS_YIELD.joinpath("Specimen_RawData_6.csv"), 152.58),
    (TENS_YIELD.joinpath("Specimen_RawData_7.csv"), 145.25),
    (TENS_YIELD.joinpath("Specimen_RawData_8.csv"), 186.87),
    (TENS_YIELD.joinpath("Specimen_RawData_9.csv"), 182.95),
]

paths_and_df_shapes_no_yield = [
    (TENS_NO_YIELD.joinpath("Specimen_RawData_1.csv"), (1467, 6)),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_10.csv"), (1299, 6)),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_2.csv"), (1066, 6)),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_3.csv"), (1177, 6)),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_4.csv"), (1214, 6)),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_5.csv"), (1228, 6)),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_6.csv"), (1238, 6)),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_7.csv"), (1303, 6)),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_8.csv"), (1245, 6)),
    (TENS_NO_YIELD.joinpath("Specimen_RawData_9.csv"), (1237, 6)),
]

paths_and_df_shapes_yield = [
    (TENS_YIELD.joinpath("Specimen_RawData_1.csv"), (279, 6)),
    (TENS_YIELD.joinpath("Specimen_RawData_10.csv"), (319, 6)),
    (TENS_YIELD.joinpath("Specimen_RawData_2.csv"), (309, 6)),
    (TENS_YIELD.joinpath("Specimen_RawData_3.csv"), (185, 6)),
    (TENS_YIELD.joinpath("Specimen_RawData_4.csv"), (288, 6)),
    (TENS_YIELD.joinpath("Specimen_RawData_5.csv"), (269, 6)),
    (TENS_YIELD.joinpath("Specimen_RawData_6.csv"), (469, 6)),
    (TENS_YIELD.joinpath("Specimen_RawData_7.csv"), (331, 6)),
    (TENS_YIELD.joinpath("Specimen_RawData_8.csv"), (297, 6)),
    (TENS_YIELD.joinpath("Specimen_RawData_9.csv"), (219, 6)),
]

paths_and_yield_strengths = [
    (TENS_YIELD.joinpath("Specimen_RawData_10.csv"), 83.77),
    (TENS_YIELD.joinpath("Specimen_RawData_1.csv"), 90.12),
    (TENS_YIELD.joinpath("Specimen_RawData_2.csv"), 85.97),
    (TENS_YIELD.joinpath("Specimen_RawData_3.csv"), 89.16),
    (TENS_YIELD.joinpath("Specimen_RawData_4.csv"), 87.15),
    (TENS_YIELD.joinpath("Specimen_RawData_5.csv"), 90.52),
    (TENS_YIELD.joinpath("Specimen_RawData_6.csv"), 78.27),
    (TENS_YIELD.joinpath("Specimen_RawData_7.csv"), 87.79),
    (TENS_YIELD.joinpath("Specimen_RawData_8.csv"), 90.77),
    (TENS_YIELD.joinpath("Specimen_RawData_9.csv"), 91.00),
]

paths_and_extract_values_series_no_yield = [
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_1.csv"),
        pd.Series(
            data={
                "Specimen ID": "0038",
                "Strength": 739.33,
                "Modulus": 214.74,
            }
        ),
    ),
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_10.csv"),
        pd.Series(
            data={
                "Specimen ID": "0039",
                "Strength": 805.48,
                "Modulus": 227.93,
            }
        ),
    ),
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_2.csv"),
        pd.Series(
            data={
                "Specimen ID": "0031",
                "Strength": 720.63,
                "Modulus": 222.73,
            }
        ),
    ),
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_3.csv"),
        pd.Series(
            data={
                "Specimen ID": "0040",
                "Strength": 806.69,
                "Modulus": 226.24,
            }
        ),
    ),
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_4.csv"),
        pd.Series(
            data={
                "Specimen ID": "0032",
                "Strength": 782.97,
                "Modulus": 227.21,
            }
        ),
    ),
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_5.csv"),
        pd.Series(
            data={
                "Specimen ID": "0033",
                "Strength": 764.47,
                "Modulus": 237.50,
            }
        ),
    ),
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_6.csv"),
        pd.Series(
            data={
                "Specimen ID": "0034",
                "Strength": 784.49,
                "Modulus": 230.00,
            }
        ),
    ),
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_7.csv"),
        pd.Series(
            data={
                "Specimen ID": "0036",
                "Strength": 784.17,
                "Modulus": 210.58,
            }
        ),
    ),
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_8.csv"),
        pd.Series(
            data={
                "Specimen ID": "0035",
                "Strength": 809.76,
                "Modulus": 201.60,
            }
        ),
    ),
    (
        TENS_NO_YIELD.joinpath("Specimen_RawData_9.csv"),
        pd.Series(
            data={
                "Specimen ID": "0037",
                "Strength": 778.89,
                "Modulus": 222.34,
            }
        ),
    ),
]

paths_and_extract_values_series_yield = [
    (
        TENS_YIELD.joinpath("Specimen_RawData_10.csv"),
        pd.Series(
            data={
                "Specimen ID": "010",
                "Strength": 180.30,
                "Modulus": 171.04,
                "Yield Strength": 83.77,
            }
        ),
    ),
    (
        TENS_YIELD.joinpath("Specimen_RawData_1.csv"),
        pd.Series(
            data={
                "Specimen ID": "009",
                "Strength": 188.44,
                "Modulus": 177.04,
                "Yield Strength": 90.12,
            }
        ),
    ),
    (
        TENS_YIELD.joinpath("Specimen_RawData_2.csv"),
        pd.Series(
            data={
                "Specimen ID": "008",
                "Strength": 183.73,
                "Modulus": 190.01,
                "Yield Strength": 85.97,
            }
        ),
    ),
    (
        TENS_YIELD.joinpath("Specimen_RawData_3.csv"),
        pd.Series(
            data={
                "Specimen ID": "007",
                "Strength": 151.36,
                "Modulus": 174.27,
                "Yield Strength": 89.16,
            }
        ),
    ),
    (
        TENS_YIELD.joinpath("Specimen_RawData_4.csv"),
        pd.Series(
            data={
                "Specimen ID": "006",
                "Strength": 180.86,
                "Modulus": 154.95,
                "Yield Strength": 87.15,
            }
        ),
    ),
    (
        TENS_YIELD.joinpath("Specimen_RawData_5.csv"),
        pd.Series(
            data={
                "Specimen ID": "005",
                "Strength": 184.76,
                "Modulus": 178.21,
                "Yield Strength": 90.52,
            }
        ),
    ),
    (
        TENS_YIELD.joinpath("Specimen_RawData_6.csv"),
        pd.Series(
            data={
                "Specimen ID": "004",
                "Strength": 190.41,
                "Modulus": 152.58,
                "Yield Strength": 78.27,
            }
        ),
    ),
    (
        TENS_YIELD.joinpath("Specimen_RawData_7.csv"),
        pd.Series(
            data={
                "Specimen ID": "003",
                "Strength": 194.31,
                "Modulus": 145.25,
                "Yield Strength": 87.79,
            }
        ),
    ),
    (
        TENS_YIELD.joinpath("Specimen_RawData_8.csv"),
        pd.Series(
            data={
                "Specimen ID": "002",
                "Strength": 191.43,
                "Modulus": 186.87,
                "Yield Strength": 90.77,
            }
        ),
    ),
    (
        TENS_YIELD.joinpath("Specimen_RawData_9.csv"),
        pd.Series(
            data={
                "Specimen ID": "001",
                "Strength": 168.06,
                "Modulus": 182.95,
                "Yield Strength": 91.00,
            }
        ),
    ),
]
