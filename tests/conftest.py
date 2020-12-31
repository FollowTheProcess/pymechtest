"""
Fixtures and other test configuration.

Author: Tom Fleet
Created: 31/12/2020
"""

import pytest


@pytest.fixture
def tensile_long():
    """
    Equivalent to calling Tensile pointing at the
    longitudinal test data.
    """
    from pathlib import Path

    from pymechtest import Tensile

    return Tensile(
        folder=Path(__file__).parents[1].resolve().joinpath("tests/data/Long"),
        stress_col="Tensile stress",
        strain_col="Tensile strain (Strain 1)",
        id_row=3,
        skip_rows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )


@pytest.fixture
def tensile_trans():
    """
    Equivalent to calling Tensile pointing at the
    transverse test data.
    """
    from pathlib import Path

    from pymechtest import Tensile

    return Tensile(
        folder=Path(__file__).parents[1].resolve().joinpath("tests/data/Trans"),
        stress_col="Tensile stress",
        strain_col="Tensile strain (Strain 1)",
        id_row=3,
        skip_rows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
        strain1=0.005,
        strain2=0.015,
        expect_yield=True,
    )
