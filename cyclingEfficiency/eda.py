import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
from pandas._libs.tslibs.timestamps import Timestamp
from .utils import Constants, Utils


class Eda:
    def __init__(
            self, data: DataFrame, bike_weight: float
        ) -> None:
        """
        This class add and transform information

        Parameters:

        data (DataFrame):
            DataFrame with information
        """
        self.data: DataFrame = data
        self.bike_weight: float = bike_weight
        self.add_variable()


    def add_variable(self)-> None:
        """
        This method use add variables to the data

        Parameters:
        
        None 
        
        Returns:
        
        None
        """
        self.data['w'] = self.data.apply(
            lambda x: Utils.generate_w(
                slope=x['slope'],
                mass=x['weight'] + self.bike_weight,
                velocity_km_h=x['kph']
            ),
            axis=1
        )

        self.data['w_hr'] = self.data['w'] / self.data['hr']
        