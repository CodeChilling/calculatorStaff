from io import BytesIO
from dotenv import load_dotenv
import pandas as pd
import requests
from enum import Enum
from os import getenv

from helpers.transformColumn import transform_column

load_dotenv()

class Paths(Enum):
    DATA = "Data"
    MATRIZ = "Matriz"


def get_Data(path: Paths) -> pd.DataFrame:

    response = requests.get(getenv("EXCEL_URL"))
    response.raise_for_status()
    
    excel_data = BytesIO(response.content)

    df = pd.read_excel(excel_data, engine="openpyxl", sheet_name=path.value)
    
    return df


def get_elements(data: pd.DataFrame, column: str, isCapitalize: bool = False, isLower: bool = False, isUpper: bool = False) -> list[str]:
    elements: list[str] = data[column].dropna().drop_duplicates().tolist()

    # elements = [position.strip() for position in elements]
    # if isCapitalize:
    #     elements = [position.capitalize() for position in elements]
    # elif isLower:
    #     elements = [position.lower() for position in elements]
    # elif isUpper:
    #     elements = [position.upper() for position in elements]

    elements = list(set(elements))

    if column != "Years Experience":
        elements.sort()
    else:
        elements.sort(key=lambda x: int(x.split(" ")[0]))

    return elements


def get_technologies(data: pd.DataFrame) -> list[str]:
    column1 = get_elements(data, "Nombre Lenguaje Principal", isCapitalize=True)
    column2 = get_elements(data, "Nombre Lenguaje Secundario", isCapitalize=True)

    # column1 = transform_column(column1, [",", " y ", ". ", "  ", ":", "/"])
    # column2 = transform_column(column2, [",", " y ", ". ", "  ", ":", "/"])

    elements: list[str] = []

    for element in column1:
        elements.append(element)
    for element in column2:
        elements.append(element)

    # elements = [element.strip() for element in elements]
    # elements = [element.capitalize() for element in elements]
    elements = list(set(elements))

    elements.sort()
    return elements


def get_english_level(data: pd.DataFrame, column) -> list[str]:
    elements = get_elements(data, column)
    elements = [element.split(" ")[0] for element in elements]
    elements = list(set(elements))

    elements.sort()
    return elements


