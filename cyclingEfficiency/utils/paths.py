import pathlib
import os
import sys
from pathlib import Path
sys.path.append('../../')
from config import PATH_MAIN_FOLDER

class Paths():
    MAIN_FOLDER: Path = ( 
        pathlib.Path().joinpath(PATH_MAIN_FOLDER)
        if pathlib.Path().joinpath(PATH_MAIN_FOLDER).exists()
        else pathlib.Path().joinpath('..', PATH_MAIN_FOLDER)
        )
    RAW_FOLDER: Path = MAIN_FOLDER.joinpath('raw')
    INTERIM_FOLDER: Path = MAIN_FOLDER.joinpath('interim')
    PROCESSED_FOLDER: Path = MAIN_FOLDER.joinpath('processed')
    EXTERNAL_FOLDER: Path = MAIN_FOLDER.joinpath('external')
    
    ACTIVITIES_FOLDER: Path = RAW_FOLDER.joinpath('activities')
    WEIGHT_FILE: Path = RAW_FOLDER.joinpath('WeightFit.csv')