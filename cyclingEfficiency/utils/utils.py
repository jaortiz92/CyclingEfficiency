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
        velocity_km_h: float, crr: float= 0.021
    ) -> float:
        
        gravity: float = 9.8
        if slope > 0:
            angle_radians: float = np.arctan(slope/100)
            f_g: float = mass * gravity * np.sin(angle_radians)
        else:
            f_g: float = 0
        f_r: float = mass * gravity * crr
        d: float = velocity_km_h * 1000 / (60 * 60)
        return d * (f_r + f_g)