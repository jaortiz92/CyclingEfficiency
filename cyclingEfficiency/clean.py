import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
from pandas._libs.tslibs.timestamps import Timestamp
from .reader import Reader


class Clean:
    def __init__(
            self, kph_greater: float = 0, cad_greater: float = 0,
            hr_grater: float = 0, slope_greater_than_equal: float = 0,
            before: bool = False
        ) -> None:
        """
        This class cleans the data

        Parameters:

        kph_greater (float):
            Filter to kliometers per hour greater than
        cad_greater (float):
            Filter to cadence greater than
        hr_grater (float):
            Filter to heart rate greater than
        slope_greater_than_equal (float):
            Filter to slope greater than equal
        before (bool): 
            Select if you want to search with dates before to 
            the activity, for default it searchs dates next 
        """
        self.kph_greater: float = kph_greater
        self.cad_greater: float = cad_greater
        self.hr_grater: float = hr_grater
        self.slope_greater_than_equal: float = slope_greater_than_equal
        self.before: bool = before
        self.fit()


    def fit(self)-> None:
        """
        This method use the data added like parameters in the class
        and create the new clean data

        Parameters:
        
        None 
        
        Returns:
        
        None
        """
        data: dict[str, DataFrame] =  Reader().data

        date_min: Timestamp = data['activities']['date'].min()
        date_max: Timestamp = data['activities']['date'].max()

        weight: DataFrame = pd.DataFrame(
            pd.date_range(
                start=date_min,
                end=date_max,
                freq='d'
            ),
            columns=['date']
        )

        weight['weight'] = weight['date'].apply(
            self.search_weight, df_weight=data['weight'], 
            before=self.before
        )

        df: DataFrame = pd.merge(
            left=data['activities'],
            right=weight,
            on='date',
            how='left'
        )

        self.data: DataFrame = df[
            (df['kph'] > self.kph_greater) &
            (df['cad'] > self.cad_greater) &
            (df['hr'] > self.hr_grater) &
            (df['slope'] >= self.slope_greater_than_equal) &
            (~df['weight'].isna())
        ].reset_index()


    def search_weight(
        sefl,
        date_to_search: Timestamp, df_weight: DataFrame,
        before: bool
    ) -> float:
        """
        This method search the weight to the date closer to the
        date objetive.

        ### Parameters:
        
        date_to_search (Timestamp): 
            Date to search in df
        df_weight (DataFrame):
            DateFrame with information of weight and its date
        before (bool): 
            Select if you want to search with dates before to
            the activity
        
        ### Returns:
        
        float: Weight found in dataframe
        """
        result: float = np.nan
        if before:
            df_result: DataFrame = df_weight[
                df_weight['date']<=date_to_search
            ]
            if df_result.shape[0] > 0:
                result = df_result.iloc[-1,1]    
        else: 
            df_result: DataFrame = df_weight[
                df_weight['date']>=date_to_search
            ]
            result = df_result.iloc[-1,1]
        return result