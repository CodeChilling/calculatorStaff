from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import requests
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
from os import getenv
from fastapi.middleware.cors import CORSMiddleware

from helpers.clear_up import Paths, get_Data, get_elements, get_english_level, get_technologies
from helpers.createListObj import create_list_objects
from helpers.get_cities import get_cities_api
from models.cotization import Cotization

app = FastAPI()

load_dotenv()

origin = {
    'http://localhost:5173',
    'https://nicolas.d3p6mab7kaial0.amplifyapp.com/'
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/cotization")
def get_current_info(currentData: Cotization):
    try:
        df = get_Data(Paths.DATA)

        df["Pretension Salarial "] = df["Pretension Salarial "].str.replace("$", "")
        df["Pretension Salarial "] = df["Pretension Salarial "].str.replace(",", "")
        df["Pretension Salarial "] = df["Pretension Salarial "].str.replace(".", "")
        df["Pretension Salarial "] = pd.to_numeric(df["Pretension Salarial "], errors="coerce")
        
        position = currentData.position
        technology = currentData.technology
        ubication = currentData.ubication
        english_level = currentData.english_level
        years_experience = currentData.years_experience
        
        salary = df[(df["Position"] == position) & 
                    (df["Nombre Lenguaje Principal"] == technology) & 
                    (df["Country Location of Consultant"] == ubication) & 
                    (df["English Proficiency"] == english_level) & 
                    (df["Experience"] >= years_experience)]["Pretension Salarial "].median()
        
        print({salary})
        return JSONResponse(
            content={
                "salary": salary
            }
        )
    
    except requests.exceptions.HTTPError as errh:
        raise HTTPException(status_code=500, detail=f"HTTP error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        raise HTTPException(status_code=405, detail=f"Connection error: {errc}")
    except requests.exceptions.Timeout as errt:
        raise HTTPException(status_code=401, detail=f"Timeout: {errt}")
    except requests.exceptions.RequestException as err:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {err}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing the Excel file: {e}")
    

@app.get("/replica")
async def get_info_total():
    try:
        dfDATA = get_Data(path=Paths.DATA)
        dfMATRIZ = get_Data(path=Paths.MATRIZ)

        positions = get_elements(dfDATA, "Position", isCapitalize=True)

        EnglishLevelList = get_english_level(dfDATA, "English Proficiency")
        finalEnglishLevelList = create_list_objects(EnglishLevelList)

        technologies = get_technologies(dfDATA)

        years_experience = get_elements(dfMATRIZ, "Years Experience")
        finalExperienceList = create_list_objects(years_experience)

        countries = get_elements(dfDATA, "Country Location of Consultant", isCapitalize=True)

        citiesByCountry = []
        for i in range(len(countries)):
            country = countries[i]
            countries[i]= dfDATA[dfDATA["Country Location of Consultant"] == countries[i]]["Ciudad"].fillna("No city").unique().tolist()
            temp = {
                country: countries[i]
            }
            citiesByCountry.append(temp)


        return JSONResponse(
          status_code=200,
          content={
            "positions": positions,
            "technologies": technologies,
            "ubication": citiesByCountry,
            "english_level": finalEnglishLevelList,
            "years_experience": finalExperienceList,
          }
        )

    except requests.exceptions.HTTPError as errh:
        raise HTTPException(status_code=500, detail=f"HTTP error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        raise HTTPException(status_code=405, detail=f"Connection error: {errc}")
    except requests.exceptions.Timeout as errt:
        raise HTTPException(status_code=401, detail=f"Timeout: {errt}")
    except requests.exceptions.RequestException as err:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {err}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing the Excel file: {e}")

    
