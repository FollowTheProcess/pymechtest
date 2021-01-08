"""
Tests for the fatigue implementation.

Author: Tom Fleet
Created: 08/01/2021
"""

from pathlib import Path

from pymechtest import Fatigue


def test_fatigue_init():

    obj = Fatigue(
        folder="made/up/directory",
        header=0,
        stress_col="Fatigue stress",
        strain_col="Fatigue strain (Strain 1)",
    )

    assert obj.folder == "made/up/directory"
    assert obj.header == 0
    assert obj.stress_col == "Fatigue stress"
    assert obj.strain_col == "Fatigue strain (Strain 1)"


def test_fatigue_repr():

    obj = Fatigue(
        folder="made/up/directory",
        stress_col="Fatigue stress",
        strain_col="Fatigue strain (Strain 1)",
        header=0,
    )

    assert (
        obj.__repr__() == "Fatigue(folder='made/up/directory', "
        "stress_col='Fatigue stress', "
        "strain_col='Fatigue strain (Strain 1)', "
        "header=0)"
    )


def test_fatigue_eq():

    obj = Fatigue(
        folder="made/up/directory",
        header=0,
        stress_col="Fatigue stress",
        strain_col="Fatigue strain (Strain 1)",
    )

    same = Fatigue(
        folder="made/up/directory",
        header=0,
        stress_col="Fatigue stress",
        strain_col="Fatigue strain (Strain 1)",
    )

    diff = Fatigue(
        folder="different/made/up/directory",
        header=6,
        stress_col="Different stress col",
        strain_col="This doesn't match either",
    )

    # Random different class, in this case a pathlib.Path
    different_class = Path(__file__)

    assert obj.__eq__(same) is True
    assert obj.__eq__(diff) is False
    assert obj.__eq__(different_class) is NotImplemented
