import pandas as pd
import warnings

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

# Cargar el archivo CSV en un DataFrame
df = pd.read_excel(r"C:\Users\Jackson Bonilla\Documents\Exsis\Calculadora-Staff\fastapi-calc-backend\calc-env\calculatorStaff\Rates flujo.xlsx")

print(df.columns)

experiencia_minima = 1.0  # años de experiencia
tecnologia = 'Java'
nivel_ingles = 'B1'
perfil_profesional = 'Desarrollador Java'
ubicacion = 'Bogota'

# Aplicar los filtros al DataFrame
df_filtrado = df[
    (df['Experience'] >= experiencia_minima)
]
promedio_salario = df_filtrado['Pretension Salarial '].mean()

print(f'El promedio de la pretensión salarial es: {promedio_salario}')