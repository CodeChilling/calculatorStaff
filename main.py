from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import requests
import pandas as pd
import math
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
    'https://dev.d1m5iwwmoe1hji.amplifyapp.com'
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

        df["Aspiración Salarial"] = df["Aspiración Salarial"].str.replace("$", "")
        df["Aspiración Salarial"] = df["Aspiración Salarial"].str.replace(",", "")
        df["Aspiración Salarial"] = df["Aspiración Salarial"].str.replace(".", "")
        df["Aspiración Salarial"] = pd.to_numeric(df["Aspiración Salarial"], errors="coerce")
        
        position = currentData.position
        technology = currentData.technology
        city = currentData.city
        country = currentData.country
        english_level = currentData.english_level
        years_experience = currentData.years_experience
        
        if years_experience == 0:
            experience_start = 1
            experience_end = 2
        elif years_experience == 1:
            experience_start = 3
            experience_end = 4
        elif years_experience == 2:
            experience_start = 5
            experience_end = None
        
        print(currentData)
     
        if experience_end != None:
            salary = df[(df["Position"] == position) & 
                    (df["Lenguaje Principal"] == technology) & 
                    (df["Country Location of Consultant"] == country) &
                    (df["Ciudad"] == city) & 
                    (df["English Proficiency"] == english_level) & 
                    (df["Años de Experiencia"] >= float(experience_start))& 
                    (df["Años de Experiencia"] <= float(experience_end))]["Pretension Salarial"].median()
        else:
            salary = df[(df["Position"] == position) & 
                    (df["Nombre Lenguaje Principal"] == technology) & 
                    (df["Country Location of Consultant"] == country) &
                    (df["City Location of Consultant"] == city) &
                    (df["English Proficiency"] == english_level) & 
                    (df["Experience"] >= float(experience_start))]["Pretension Salarial "].median()
        
        if(not(math.isnan(salary))):
        
            print(salary)
            return JSONResponse(
                content={
                    "salary": salary,
                    "found":True
                }
            )
        else:
            return JSONResponse(
                content={
                    "salary": 0,
                    "found":False
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
