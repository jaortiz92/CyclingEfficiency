import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
from pandas._libs.tslibs.timestamps import Timestamp
from .utils import Constants, Utils


class Eda:
    def __init__(
            self, data: DataFrame, bike_weight: float,
            cad_min: int, cad_max: int, cad_step: int,
            with_watts: bool
        ) -> None:
        """
        This class add and transform information

        Parameters:
        -----------

        data (DataFrame):
            DataFrame with information
        bike_weight (float):
            Total mass, it must have the weight
            of a cyclist and his bicycle.
        cad_min (int):
            Value lower to use in the cadence
        cad_max (int):
            Value upper to use in the cadence
        cad_step (int):
            Step to range in cadence zone
        with_watts (bool):
            If you want to use the variable watts to use in de model 
        """
        self.data: DataFrame = data
        self.bike_weight: float = bike_weight
        self.cad_min: int = cad_min
        self.cad_max: int = cad_max
        self.cad_step: int = cad_step
        self.with_watts: bool = with_watts
        self.add_variables()


    def add_variables(self)-> None:
        """
        This method use add variables to the data

        Parameters:
        -----------
        None 
        
        Returns:
        --------
        None
        """
        data: DataFrame = self.data.copy()
        # mechanical work
        data['w'] = data.apply(
            lambda x: Utils.generate_w(
                slope=x['slope'],
                mass=x['weight'] + self.bike_weight,
                velocity_km_h=x['kph']
            ),
            axis=1
        )

        if self.with_watts:
            data['dif_w'] = data[['watts', 'w']].apply(
                lambda x: (x[0] - x[1]) / x[1] if x[0] != x[1] else 0,
                axis=1
            )

            data = data[
                (data['dif_w'] >= -1) &
                (data['dif_w'] <= 1)
            ].reset_index()

            data['w'] = data['watts']

        data['w_hr'] = data['w'] / data['hr']
        data['w_kg'] = data['w'] / data['weight']
        data['w_kg_hr'] = data['w_kg'] / data['hr']

        # Indicator
        data['performance_indicator'] = data['w_kg'] / data['zones']
        
        # Cad
        data['cad_zone'] = Utils.generate_cad_zone(
            data['cad'], self.cad_min,
            self.cad_max, self.cad_step
        )
        data = data[
            ~data['cad_zone'].isna()
        ].reset_index(drop=True)

        data['cad_zone_num'] = data['cad_zone'].map(
            lambda x: int(x[:2])
        )

        self.data = data.copy()