from cyclingEfficiency import CyclingEfficiency, Model
from config import *

def run():
    model: Model = Model(
        hr_max=HR_MAX,
        bike_weight=BIKE_WEIGHT,
        cad_min=CAD_MIN,
        cad_max=CAD_MAX,
        cad_step=CAD_STEP,
        kph_greater=KPH_GREATER,
        hr_grater=HR_GRATER,
        slope_greater_than_equal=SLOPE_GREATER_THAN_EQUAL,
        zone_grater_than_equal=ZONE_GRATER_THAN_EQUAL,
        body_weight=BODY_WEIGHT,
        previous_weight=PREVIOUS_WEIGHT,
        bash_size=BASH_SIZE,
        margen_result=MARGEN_RESULT,
        with_watts=WITH_WATTS
    )
    model.fit_plain(degree=DEGREE_PLAIN)
    model.fit_hill(degree=DEGREE_HILL)


if __name__ == "__main__":
    run()