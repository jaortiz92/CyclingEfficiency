import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
from .clean import Clean
from .eda import Eda

class CyclingEfficiency:
    def __init__(
            self, hr_max: int, bike_weight: float,
            cad_min: int = 40, cad_max: int = 120, cad_step: int = 5,
            kph_greater: float = 0, hr_grater: float = 0, 
            slope_greater_than_equal: float = 0, 
            zone_grater_than_equal: int = 1, before: bool = False
        ) -> None:
        """
        This class processes the file and to generate the data to use

        Parameters:
        -----------

        hr_max (int):
            heart frequency max
        bike_weight (float):
            Total mass, it must have the weight
            of a cyclist and his bicycle.
        cad_min (float):
            Filter to cadence greater than
        cad_max (float):
            Filter to cadence less than
        cad_step (int):
            Step to range in cadence zone
        kph_greater (float):
            Filter to kliometers per hour greater than
        hr_grater (float):
            Filter to heart rate greater than
        slope_greater_than_equal (float):
            Filter to slope greater than equal
        zone_grater_than_equal (int):
            Filter to zone greater than equal
        before (bool): 
            Select if you want to search with dates before to 
            the activity, for default it searchs dates next 
        """
        self.hr_max = hr_max
        self.bike_weight: float = bike_weight
        self.cad_min: int = cad_min
        self.cad_max: int = cad_max
        self.cad_step: int = cad_step
        self.kph_greater: float = kph_greater
        self.hr_grater: float = hr_grater
        self.slope_greater_than_equal: float = slope_greater_than_equal
        self.zone_grater_than_equal: int = zone_grater_than_equal
        self.before: bool = before

    def fit(self)-> None:
        """
        This method processes the data to use

        Parameters:
        -----------
        None 
        
        Returns:
        --------
        None
        """
        data: DataFrame = Clean(
            hr_max=self.hr_max,
            kph_greater=self.kph_greater,
            cad_greater_than_equal=self.cad_min,
            hr_grater=self.hr_grater,
            slope_greater_than_equal=self.slope_greater_than_equal,
            zone_grater_than_equal=self.zone_grater_than_equal,
            before=self.before            
        ).data

        data = Eda(
            data=data,
            bike_weight=self.bike_weight,
            cad_min=self.cad_min,
            cad_max=self.cad_max,
            cad_step=self.cad_step
        ).data

