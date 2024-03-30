import pandas as pd
import numpy as np
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from pandas.core.frame import DataFrame
from ..cyclingEfficiency import CyclingEfficiency
from ..visualization import Visualize

class Model:
    def __init__(
            self, hr_max: int, bike_weight: float,
            cad_min: int = 40, cad_max: int = 120, cad_step: int = 5,
            kph_greater: float = 0, hr_grater: float = 0, 
            slope_greater_than_equal: float = 0, 
            zone_grater_than_equal: int = 1, before: bool = False,
            bash_size: float = 60 * 5, margen_result: float = 0.05
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
        margen_result (float):
            Config percentage to marge in the dataframe final sample
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
        self.bash_size: int = bash_size
        self.margen_result: float = margen_result

        self.cyclingEfficiency: CyclingEfficiency = CyclingEfficiency(
            hr_max=hr_max,
            bike_weight=bike_weight,
            cad_min=cad_min,
            cad_max=cad_max,
            cad_step=cad_step,
            kph_greater=kph_greater,
            hr_grater=hr_grater,
            slope_greater_than_equal=slope_greater_than_equal,
            zone_grater_than_equal=zone_grater_than_equal,
            before=before,
            bash_size=bash_size
        )

    def fit_plain(self, degree: int = 1)-> None:
        """
        This method fit model plain and save results
        
        Parameters:
        -----------
        degree (int):
            Config the gegree to add to the model
        
        Returns:
        --------
        None
        """
        variable: str = 'plain'
        x_variables: list[str] = ['cad_zone_num',]

        for i in range(2, degree + 1):
            var_name: str = 'cad_zone_num_' + str(i)
            self.cyclingEfficiency.samples[
                var_name
            ] = self.cyclingEfficiency.samples['cad_zone_num'] ** i
            x_variables.append(var_name)

        formula_x = ' + '.join(x_variables)
        
        x_train, x_test, y_train, y_test = train_test_split(
            self.cyclingEfficiency.samples[x_variables],
            self.cyclingEfficiency.samples[variable],
        )

        self.data_train_plain: DataFrame = pd.concat([x_train, y_train],axis=1)
        self.data_test_plain: DataFrame = pd.concat([x_test, y_test],axis=1)

        self.model_plain = (
            smf.ols(
                formula=variable + ' ~ ' + formula_x,
                data=self.data_train_plain
            ).fit()
        )

        max_value: int = self.data_train_plain['cad_zone_num'].max()
        
        x: list[int] = [
            [i ** j for j in range(1, degree + 1)]
                for i in range(1, max_value + 1)
        ]

        self.X_plain: DataFrame = pd.DataFrame(
            x,
            columns=x_variables
        )

        self.y_pred_plain: ndarray = self.model_plain.predict(self.X_plain)
        self.r2_score_plain = r2_score(
            y_test, self.model_plain.predict(x_test)
        )
        self.cad_zone_max_name_plain: str = self.cyclingEfficiency.cad_zones[
            np.argmax(self.y_pred_plain)
        ]
        self.cad_zone_max_plain: int = np.max(self.y_pred_plain)

        self.data_plain: DataFrame = self.cyclingEfficiency.data[
            (self.cyclingEfficiency.data['is_plain'] == 0) &
            (self.cyclingEfficiency.data['cad_zone'] == self.cad_zone_max_name_plain) &
            (self.cyclingEfficiency.data['performance_indicator'] > (self.cad_zone_max_plain * (1 - self.margen_result))) &
            (self.cyclingEfficiency.data['performance_indicator'] < (self.cad_zone_max_plain * (1 + self.margen_result)))
        ]

        print(
            'El rango de cadencia promedio mas eficiente en llano es',
            '{} y puede generar un promedio de eficiencia de {:.4f}'.format(
                self.cad_zone_max_name_plain[4:],
                self.cad_zone_max_plain,
        ))

        Visualize.graph_model(
            self.data_test_plain, 
            self.X_plain, 
            self.y_pred_plain, 
            variable, 
            self.cyclingEfficiency.cad_zones
        )

    def fit_hill(self, degree: int = 1)-> None:
        """
        This method fit model hill and save results
        
        Parameters:
        -----------
        degree (int):
            Config the gegree to add to the model
        
        Returns:
        --------
        None
        """
        variable: str = 'hill'
        x_variables: list[str] = ['cad_zone_num',]

        for i in range(2, degree + 1):
            var_name: str = 'cad_zone_num_' + str(i)
            self.cyclingEfficiency.samples[
                var_name
            ] = self.cyclingEfficiency.samples['cad_zone_num'] ** i
            x_variables.append(var_name)

        #formula_x = ' + '.join(x_variables)
        
        x_train, x_test, y_train, y_test = train_test_split(
            self.cyclingEfficiency.samples[x_variables],
            self.cyclingEfficiency.samples[variable],
        )

        self.data_train_hill: DataFrame = pd.concat([x_train, y_train],axis=1)
        self.data_test_hill: DataFrame = pd.concat([x_test, y_test],axis=1)

        self.model_hill = RandomForestRegressor(n_estimators=1000, max_depth=4)

        max_value: int = self.data_train_hill['cad_zone_num'].max()
        
        x: list[int] = [
            [i ** j for j in range(1, degree + 1)]
                for i in range(1, max_value + 1)
        ]

        self.X_hill: DataFrame = pd.DataFrame(
            x,
            columns=x_variables
        )

        self.model_hill.fit(x_train, y_train)
        self.y_pred_hill: ndarray = self.model_hill.predict(self.X_hill)
        self.r2_score_hill = r2_score(
            y_test, self.model_hill.predict(x_test)
        )
        
        self.cad_zone_max_name_hill: str = self.cyclingEfficiency.cad_zones[
            np.argmax(self.y_pred_hill)
        ]
        self.cad_zone_max_hill: int = np.max(self.y_pred_hill)

        self.data_hill: DataFrame = self.cyclingEfficiency.data[
            (self.cyclingEfficiency.data['is_plain'] == 0) &
            (self.cyclingEfficiency.data['cad_zone'] == self.cad_zone_max_name_hill) &
            (self.cyclingEfficiency.data['performance_indicator'] > (self.cad_zone_max_hill * (1 - self.margen_result))) &
            (self.cyclingEfficiency.data['performance_indicator'] < (self.cad_zone_max_hill * (1 + self.margen_result)))
        ]

        print(
            'El rango de cadencia promedio mas eficiente en montaña es',
            '{} y puede generar un promedio de eficiencia de {:.4f}'.format(
                self.cad_zone_max_name_hill[4:],
                self.cad_zone_max_hill,
        ))

        Visualize.graph_model(
            self.data_test_hill, 
            self.X_hill, 
            self.y_pred_hill, 
            variable, 
            self.cyclingEfficiency.cad_zones
        )