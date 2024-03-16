import pathlib
import os
from pathlib import Path


class Paths():
    MAIN_FOLDER: Path = ( 
        pathlib.Path().joinpath('data') 
        if pathlib.Path().joinpath('data').exists()
         else pathlib.Path().joinpath('..', 'data')
        )
    RAW_FOLDER: Path = MAIN_FOLDER.joinpath('raw')
    INTERIM_FOLDER: Path = MAIN_FOLDER.joinpath('interim')
    PROCESSED_FOLDER: Path = MAIN_FOLDER.joinpath('processed')
    EXTERNAL_FOLDER: Path = MAIN_FOLDER.joinpath('external')
    
    ACTIVITIES_FOLDER: Path = RAW_FOLDER.joinpath('activities')
    WEIGHT_FILE: Path = RAW_FOLDER.joinpath('WeightFit.csv')