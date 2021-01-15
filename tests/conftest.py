"""
Fixtures and other test configuration.

Author: Tom Fleet
Created: 31/12/2020
"""

from pathlib import Path

import pandas as pd
import pytest

from pymechtest.base import BaseMechanicalTest


@pytest.fixture
def base_no_yield():
    """
    Equivalent to calling BaseMechanicalTest pointing at the
    elastic to failure test data.

    Stress and strain col refer to Tensile because
    the data I'm using for testing is from a static tensile test.
    """

    return BaseMechanicalTest(
        folder=Path(__file__).parents[1].resolve().joinpath("tests/data/Tens_No_Yield"),
        header=8,
        stress_col="Tensile stress",
        strain_col="Tensile strain (Strain 1)",
        id_row=3,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )


@pytest.fixture
def base_no_yield_no_id():
    """
    Same as base long but without specifying an ID row.
    """

    return BaseMechanicalTest(
        folder=Path(__file__).parents[1].resolve().joinpath("tests/data/Tens_No_Yield"),
        header=8,
        stress_col="Tensile stress",
        strain_col="Tensile strain (Strain 1)",
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )


@pytest.fixture
def base_yield():
    """
    Equivalent to calling BaseMechanicalTest pointing at the
    yield test data.

    Stress and strain col refer to Tensile because
    the data I'm using for testing is from a static tensile test.
    """

    return BaseMechanicalTest(
        folder=Path(__file__).parents[1].resolve().joinpath("tests/data/Tens_Yield"),
        header=8,
        stress_col="Tensile stress",
        strain_col="Tensile strain (Strain 1)",
        id_row=3,
        strain1=0.005,
        strain2=0.015,
        expect_yield=True,
    )


@pytest.fixture
def base_no_yield_no_stress_strain_cols():
    """
    Like above but not specifying stress and strain col
    names to test the auto-detection.
    """

    return BaseMechanicalTest(
        folder=Path(__file__).parents[1].resolve().joinpath("tests/data/Tens_No_Yield"),
        header=8,
        id_row=3,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )


@pytest.fixture
def base_yield_no_stress_strain_cols():
    """
    Like above but not specifying stress and strain col
    names to test the auto-detection.
    """

    return BaseMechanicalTest(
        folder=Path(__file__).parents[1].resolve().joinpath("tests/data/Tens_Yield"),
        header=8,
        id_row=3,
        strain1=0.005,
        strain2=0.015,
        expect_yield=True,
    )


@pytest.fixture
def df_with_good_stress_and_strain_cols():
    """
    Simple dataframe with both a stress and a strain column.
    """

    return pd.DataFrame(
        {
            "This one has stress in it": [1, 2, 3, 4, 5, 6],
            "This one has strain in it": [10, 20, 30, 40, 50, 60],
        }
    )


@pytest.fixture
def df_with_bad_stress_col():
    """
    Simple dataframe without a stress col.
    """

    return pd.DataFrame(
        {"Column 1": [1, 2, 3, 4, 5, 6], "Strain": [10, 20, 30, 40, 50, 60]}
    )


@pytest.fixture
def df_with_bad_strain_col():
    """
    As above but with no strain col.
    """

    return pd.DataFrame(
        {"Stress": [1, 2, 3, 4, 5, 6], "Column 2": [10, 20, 30, 40, 50, 60]}
    )


@pytest.fixture
def df_with_bad_stress_and_strain_cols():
    """
    Simple dataframe without either a stress or strain col.
    """

    return pd.DataFrame(
        {"Column 1": [1, 2, 3, 4, 5, 6], "Column 2": [10, 20, 30, 40, 50, 60]}
    )
