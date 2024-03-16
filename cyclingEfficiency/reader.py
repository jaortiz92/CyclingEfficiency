import pandas as pd
import numpy as np
import os
from datetime import datetime
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from pathlib import Path
from .utils import Constants

class Reader():
    def __init__(self) -> None:
        '''
        This class read all files csv in
        folder raw
        '''
        self.files: list[Path] = list(
            Constants.RAW_FOLDER.iterdir()
        )

        self.dfs: list[DataFrame] = [
            self.read_a_df(file) for file in self.files
        ]

        self.data: DataFrame = pd.concat(
            self.dfs, ignore_index=False
        )

    def read_a_df(self, file: Path) -> DataFrame:
        """
        This method read a file and add columns if it needs.

        Parameters:
        file (Path): File's path to read
        
        Returns:
        DataFrame: Data like dataframe with new columns
        """
        df: DataFrame = pd.read_csv(file)
        date: datetime = datetime.strptime(file.stem , '%Y_%m_%d_%H_%M_%S')
        df['date'] = date
        return df