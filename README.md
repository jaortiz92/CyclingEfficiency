# Cycling efficiency
By: John Alexander Ortiz

Email: jaortiz92@hotmail.com

I am an amateur cyclist, and I want to answer the next question: ¿Am I more efficient in the use of my energy, pedaling with high or low cadence?¿Is there a difference if the terrain is flat or hilly?

Soy ciclista amateur, siempre he querido responder la siguiente pregunta: ¿Soy mas eficiente en el uso de mi energia, pedaleando con alta o baja cadencia?¿Es diferente si estoy en terreno llano o en montaña?

## Installation and Configuration

1. Clone the repository

    ```bash
    git clone https://github.com/jaortiz92/CyclingEfficiency.git

    cd CyclingEfficiency

    pip install -r requirements. txt

    ```

2. Add data
    - Copy the activities of Strava in the folder "data/raw/activities/"
    - Copy csv with your weight history to folder "data/raw/", its name should be "WeightFit.csv"
        - Format the data is:
            - Column one -> Weight Date: 2024-04-01T23:00:00.488Z
            - Column two -> Weight Measurement: 64.1
            - Column three -> Weight Unit: kg
3. Configure parameters
    ```bash
    vim config.py
    ```
    Open file "config.py", In this file you can to configure main parameters
    - HR_MAX=190 -> heart frequency max
    - BIKE_WEIGHT=11 -> Total mass, it must have the weight of a cyclist and his bicycle.
    - CAD_MIN=55 -> Filter to cadence greater than
    - CAD_MAX=100 -> Filter to cadence less than
    - CAD_STEP=5 -> Step to range in cadence zone
    - KPH_GREATER=2 -> Filter to kilometers per hour greater than
    - HR_GRATER=0 -> Filter to heart rate greater than
    - SLOPE_GREATER_THAN_EQUAL=0 -> Filter to slope greater than equal
    - ZONE_GRATER_THAN_EQUAL=1 -> Filter to zone greater than equal
    - BEFORE=False -> Select if you want to search with dates before to the activity, for default it searchs dates next
    - BASH_SIZE=300 -> Select size tu bash for sample
    - MARGEN_RESULT=0.05 -> Config percentage to marge in the dataframe final sample
    - DEGREE_HILL=1 -> Degree to model hill
    - DEGREE_PLAIN=2 -> -> Degree to model plain
## Run model
```bash
python main.py
```
After you ran the last code, you must wait a few secounds while it analyzes the information. when it finishes, it will show you a graph with one of the models and in the terminal the result. When you close that graph, the program will show the result of the other model
### Example
```bash
El rango de cadencia promedio mas eficiente en llano es 85-89 y puede generar un promedio de eficiencia de 1.3521
```
![Graph Plain](./reports/model_plain_graph)

```bash
El rango de cadencia promedio mas eficiente en montaña es 60-64 y puede generar un promedio de eficiencia de 1.4317
```
![Graph Plain](./reports/model_hill_graph)
