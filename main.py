from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import requests
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
from os import getenv
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from helpers.clear_up import Paths, get_Data, get_elements, get_english_level, get_technologies
from helpers.createListObj import create_list_objects
from helpers.get_cities import get_cities_api
from models.cotization import Cotization

app = FastAPI()
handler = Mangum(app)

load_dotenv()

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
      years_experience = df["Years Experience"].dropna().to_list()
      salaries = df["Salaries"].dropna().tolist()
      categories = df["Category"].dropna().tolist()
      promedios = df["Salaries"].groupby(df["Category"]).median().to_dict()
      finalExperienceList = create_list_objects(years_experience)
      finalEnglishLevelList = create_list_objects(english_level)

      return JSONResponse(
          content={
              "positions": positions,
              "technologies": technologies,
              "ubication": ubication,
              "english_level": finalEnglishLevelList,
              "years_experience": finalExperienceList,
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


@app.get("/getCities", response_model=list[str])
def get_cities(country: str = Query(..., title="Country", description="El país del que se desea obtener las ciudades", example="Colombia", alias="country", min_length=5, max_length=20)):
    try:
      result = get_Data(Paths.MATRIZ)
      cities = get_cities_api(result, country)
      
      return JSONResponse(
          status_code=200,
          content={
              "cities": cities
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

        ubication = get_elements(dfDATA, "Country Location of Consultant", isCapitalize=True)

        citiesByCountry = []
        for i in range(len(ubication)):
            country = ubication[i]
            ubication[i]= dfDATA[dfDATA["Country Location of Consultant"] == ubication[i]]["City Location of Consultant"].fillna("No city").unique().tolist()
            temp = {
                country: ubication[i]
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

    
