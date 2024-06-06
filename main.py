from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
from os import getenv


app = FastAPI()

load_dotenv()

base_url = getenv("EXCEL_URL")

@app.get("/positions")
async def get_options():
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        
        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data)
        
        positions = df["Positions"].dropna().tolist()
        technologies = df["Technologies"].dropna().tolist()
        ubication = df["Ubication"].dropna().tolist()
        english_level = df["Level English"].dropna().tolist()
        years_experience = df["Years Experience"].dropna().tolist()

        return JSONResponse(
            content={
                "datos": {
                    "positions": positions,
                    "technologies": technologies,
                    "ubication": ubication,
                    "english_level": english_level,
                    "years_experience": years_experience
                }
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

