from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
from os import getenv
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from models.cotization import Cotization

app = FastAPI()
handler = Mangum(app)

load_dotenv()

# base_url = getenv("EXCEL_URL")

origin = {
    'http://localhost:5173',
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/positions")
async def get_options():
    try:
        response = requests.get(getenv("EXCEL_URL"))
        response.raise_for_status()
        
        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data)
        
        positions = df["Positions"].dropna().tolist()
        technologies = df["Technologies"].dropna().tolist()
        ubication = df["Ubication"].dropna().tolist()
        english_level = df["Level English"].dropna().tolist()
        years_experience = df["Years Experience"].dropna().tolist()
        salaries = df["Salaries"].dropna().tolist()
        categories = df["Category"].dropna().tolist()
        promedios = df["Salaries"].groupby(df["Category"]).median().to_dict()

        return JSONResponse(
            content={
                    "positions": positions,
                    "technologies": technologies,
                    "ubication": ubication,
                    "english_level": english_level,
                    "years_experience": years_experience,
                    "salaries": salaries,
                    "categories": categories,
                    "despDesarrolladores": promedios
                }
        )
    
    except requests.exceptions.HTTPError as errh:
        raise HTTPException(status_code=500, detail=f"HTTP error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        raise HTTPException(status_code=500, detail=f"Connection error: {errc}")
    except requests.exceptions.Timeout as errt:
        raise HTTPException(status_code=500, detail=f"Timeout: {errt}")
    except requests.exceptions.RequestException as err:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the Excel file: {e}")


@app.get("/getCities/{country}")
def get_cities(country):
    if country == "Colombia":
        url = "https://api-colombia.com/api/v1/City"
    else:
        return "Country not found"
    try:
        response = requests.get(url)
        response = response.json()
        placeNames = []
        [place["name"] for place in response if placeNames.append(place["name"])]
        # myDf = pd.DataFrame(placeNames, columns=["Cities"])
        # myDf.to_excel('output.xlsx', index=False)
        return JSONResponse(
            content={
                "cities": placeNames
            }
        )

    except requests.exceptions.HTTPError as errh:
        raise HTTPException(status_code=500, detail=f"HTTP error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        raise HTTPException(status_code=500, detail=f"Connection error: {errc}")
    except requests.exceptions.Timeout as errt:
        raise HTTPException(status_code=500, detail=f"Timeout: {errt}")
    except requests.exceptions.RequestException as err:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the Excel file: {e}")


@app.post("/cotization")
def get_current_info(currentData: Cotization):
    try:
        response = requests.get(getenv("EXCEL_URL"))
        response.raise_for_status()
        
        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data)
        
        position = currentData.position
        technology = currentData.technology
        ubication = currentData.ubication
        english_level = currentData.english_level
        years_experience = currentData.years_experience
        
        salary = df[(df["Positions"] == position) & 
                    (df["Technologies"] == technology) & 
                    (df["Ubication"] == ubication) & 
                    (df["Level English"] == english_level) & 
                    (df["Years Experience"] == years_experience)]["Salaries"].values[0]
        
        return JSONResponse(
            content={
                "salary": salary
            }
        )
    
    except requests.exceptions.HTTPError as errh:
        raise HTTPException(status_code=500, detail=f"HTTP error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        raise HTTPException(status_code=500, detail=f"Connection error: {errc}")
    except requests.exceptions.Timeout as errt:
        raise HTTPException(status_code=500, detail=f"Timeout: {errt}")
    except requests.exceptions.RequestException as err:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the Excel file: {e}")
