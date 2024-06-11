import pandas as pd

def get_cities_api(data: pd.DataFrame, country: str) -> list[str]:
    elements = data[data['País'] ==  country]["Ciudad"].to_list()

    return elements