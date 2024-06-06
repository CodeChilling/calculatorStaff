from fastapi import FastAPI, HTTPException
import requests
import pandas as pd
from io import BytesIO

app = FastAPI()

@app.get("/positions")
def get_options():
    url = "https://exsissoftwareysoluciones-my.sharepoint.com/:x:/g/personal/automate_exsis_com_co/EQR6KcjXCd5HsfiXWzploa0BE17iXR0thEyv81FQ6UORgQ?download=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data)

        datos = df.to_dict(orient="records")
        print(datos)
        return {"datos": datos}
    
    except requests.exceptions.HTTPError as errh:
        raise HTTPException(status_code=500, detail=f"Error HTTP: {errh}")
    except requests.exceptions.ConnectionError as errc:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {errc}")
    except requests.exceptions.Timeout as errt:
        raise HTTPException(status_code=500, detail=f"Timeout: {errt}")
    except requests.exceptions.RequestException as err:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando el archivo Excel: {e}")
