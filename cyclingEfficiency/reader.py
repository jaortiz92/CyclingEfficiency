import pandas as pd
from datetime import datetime
from pandas.core.frame import DataFrame
from pathlib import Path
from .utils import Paths

class Reader():
    def __init__(self) -> None:
        '''
        This class read all files csv in
        folder raw
        '''
        self.files: list[Path] = list(
            Paths.ACTIVITIES_FOLDER.iterdir()
        )

        self.dfs: list[DataFrame] = [
            self.read_a_activity(file) for file in self.files
        ]

        self.data: dict[str, DataFrame] = {
            'activities': 
                pd.concat(
                    self.dfs, ignore_index=False
                ),
            'weight': self.read_weight_file()
        }



    def read_a_activity(self, file: Path) -> DataFrame:
        """
        This method read a file and add columns if it needs.

        ### Parameters:
        file (Path):
            File's path to read
        
        ### Returns:
        DataFrame: Data like dataframe with new columns
        """
        df: DataFrame = pd.read_csv(file)
        date_time: datetime = datetime.strptime(file.stem , '%Y_%m_%d_%H_%M_%S')
        df['datetime'] = date_time
        date: datetime = datetime.strptime(file.stem[:10] , '%Y_%m_%d')
        df['date'] = date
        return df
    
    def read_weight_file(self) -> DataFrame:
        """
        This method read file about weight and prepare the data.

        Parameters:

        Returns:
        DataFrame: Data like dataframe with new columns
        """
        df: DataFrame = pd.read_csv(
            Paths.WEIGHT_FILE,
            header=0,
            names=['date', 'weight', 'weight_unit']
        )
        df['date'] = df['date'].apply(
            lambda x: datetime.strptime(x[:10], '%Y-%m-%d')
        )
        return df