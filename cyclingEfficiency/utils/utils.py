import re
from re import Match
from typing import List
from datetime import datetime
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
from pandas.core.series import Series
import os


class Utils():
    @classmethod
    def generate_w(
        cls, slope: float, mass: float, 
        velocity_km_h: float, crr: float= 0.02
    ) -> float:
        """
        This function estimates the mechanical
        work for each instant

        Parameters:
        -----------
        slope (float):
            Value slope
        mass (float):
            Total mass, it must have the weight
            of a cyclist and his bicycle.
        velocity_km_h (float):
            Value velocity in kilometers per hour
        crr (float): = 0.02
            Value Rolling resistance coefficient
        
        Returns:
        --------
        float: mechanical work in joules
        """        
        gravity: float = 9.8
        if slope > 0:
            angle_radians: float = np.arctan(slope/100)
            f_g: float = mass * gravity * np.sin(angle_radians)
        else:
            f_g: float = 0
        f_r: float = mass * gravity * crr
        d: float = velocity_km_h * 1000 / (60 * 60)
        return d * (f_r + f_g)
    
    @classmethod
    def generate_cad_zone(
            self, data: Series | list[int], cad_min: int, 
            cad_max: int, cad_step: int
        ) -> list[str]:
        """
        This function transform values in intervals

        Parameters:
        -----------
        data (Series | list[int]):
            Values to transform
        cad_min (int):
            Value lower 
        cad_max (int):
            Value upper
        cad_step (int):
            Step to range
        
        Returns:
        --------
        list[str]: List with strings and its range
        """ 
        cad_zones: list[int] = list(
            range(cad_min, cad_max + 1, cad_step)
        )

        cad_zones_name: list[str] = [
            '{}) {}-{}'.format(
                str(i+1).zfill(2), lower, 
                lower + cad_step - 1
            ) 
            for i, lower in enumerate(cad_zones)
        ]

        size: int = len(cad_zones)
        result_cad_zones: list[int] = []

        for cad in data:
            flag: bool = True
            index: int = size - 1
            result: int = np.nan
            while flag and 0 <= index:
                if cad_zones[index] <= cad:
                    if index == size - 1:
                        flag = False
                    else:
                        result = cad_zones_name[index]
                        flag = False
                index -= 1  
            result_cad_zones.append(result)
        return result_cad_zones