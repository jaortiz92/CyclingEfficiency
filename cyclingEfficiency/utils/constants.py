import pathlib
from pathlib import Path

class Constants():
    MAIN_FOLDER: Path = ( 
        pathlib.Path().joinpath('data') 
        if pathlib.Path().joinpath('data').exists()
         else pathlib.Path().joinpath('..', 'data')
        )
    RAW_FOLDER: Path = MAIN_FOLDER.joinpath('raw')
    INTERIM_FOLDER: Path = MAIN_FOLDER.joinpath('interim')
    PROCESSED_FOLDER: Path = MAIN_FOLDER.joinpath('processed')
    EXTERNAL_FOLDER: Path = MAIN_FOLDER.joinpath('external')
    