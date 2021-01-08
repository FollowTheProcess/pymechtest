"""
Fatigue test class definition.

Author: Tom Fleet
Created: 08/01/2021
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Union

import pandas as pd


@dataclass
class Fatigue:

    folder: Union[Path, str]
    stress_col: str
    strain_col: str
    header: int = 0

    def _load(self, fp: Path) -> pd.DataFrame:
        """
        Method to load individual data csv file into a pandas DataFrame.

        Args:
            fp (Path): csv file to load. Exclusively pathlib.Path as files
                are discovered with an rglob in load_all.

        Returns:
            pd.DataFrame: DataFrame containing single sample's data.
        """

        # Incase there are any non-numerics below header
        df = (
            (pd.read_csv(fp, header=self.header))
            .applymap(lambda x: x.strip().replace(",", "") if isinstance(x, str) else x)
            .apply(pd.to_numeric, errors="coerce")
            .dropna(how="all")
            .assign(filename=[f"{fp.name}"])
        )

        return df

    def load_all(self) -> pd.DataFrame:
        """
        Loads all the found files in 'folder' into a dataframe.

        Recursively searches 'folder' for all csv files.

        Returns:
            pd.DataFrame: All found test data
        """

        fp = Path(self.folder).resolve()

        df = pd.concat([self._load(f) for f in sorted(fp.rglob("*.csv"))])

        return df
