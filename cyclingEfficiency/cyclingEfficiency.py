import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
from numpy import ndarray
from .clean import Clean
from .eda import Eda
from .utils import Utils

class CyclingEfficiency:
    def __init__(
            self, hr_max: int, bike_weight: float,
            cad_min: int = 40, cad_max: int = 120, cad_step: int = 5,
            kph_greater: float = 0, hr_grater: float = 0, 
            slope_greater_than_equal: float = 0, 
            zone_grater_than_equal: int = 1, before: bool = False,
            bash_size: float = 60 * 5
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
        bash_size (float):
            Select size tu bash for sample
        """
        self.hr_max: int = hr_max
        self.bike_weight: float = bike_weight
        self.cad_min: int = cad_min
        self.cad_max: int = cad_max
        self.cad_step: int = cad_step
        self.kph_greater: float = kph_greater
        self.hr_grater: float = hr_grater
        self.slope_greater_than_equal: float = slope_greater_than_equal
        self.zone_grater_than_equal: int = zone_grater_than_equal
        self.before: bool = before
        self.bash_size: int = bash_size
        self.fit()

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

        samples_list: list = []
        zones: ndarray = data['cad_zone'].unique()
        zones.sort()
        bash_size: int = self.bash_size

        for i, zone_name in enumerate(zones):
            zone_num: int = i + 1
            sample_all: list[float] = Utils.generate_sample_data(
                data=data[
                        data['cad_zone_num'] == zone_num
                    ]['performance_indicator'],
                bash_size=bash_size,
            )

            sample_pĺain: list[float] = Utils.generate_sample_data(
                data=data[
                        (data['cad_zone_num'] == zone_num) &
                        (data['is_plain'] == 1)
                    ]['performance_indicator'],
                bash_size=bash_size,
            )

            sample_hill: list[float] = Utils.generate_sample_data(
                data=data[
                        (data['cad_zone_num'] == zone_num) &
                        (data['is_plain'] == 0)
                    ]['performance_indicator'],
                bash_size=bash_size,
            )

            samples_list.extend(
                [
                    (
                        zone_num , zone_name, all_value, plain, hill
                    ) for all_value, plain, hill in zip(
                        sample_all, sample_pĺain, sample_hill
                    ) 
                ]
            )

        self.samples: DataFrame = pd.DataFrame(
            samples_list,
            columns=[
                'cad_zone_num', 'cad_zone', 
                'all', 'plain', 'hill'
            ]
        )
        self.data: DataFrame = data.copy()
        self.cad_zones: ndarray = self.samples['cad_zone'].unique()
        