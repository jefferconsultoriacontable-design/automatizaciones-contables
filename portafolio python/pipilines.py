import pandas as pd
import numpy as np

def extraer_datos(ruta_archivo):
    # Forzar formato texto en columnas clave para evitar truncar ceros
    df = pd.read_csv(ruta_archivo, dtype={'cuenta': str, 'tercero': str})
    return df

def transformar_datos(df):
    # Limpieza de espacios y conversión de saldos a numéricos
    df['debito'] = pd.to_numeric(df['debito'], errors='coerce').fillna(0)
    df['credito'] = pd.to_numeric(df['credito'], errors='coerce').fillna(0)
    
    # Operación vectorizada para saldo neto contable
    df['saldo_neto'] = df['debito'] - df['credito']
    return df

def cargar_resultados(df, ruta_salida):
    df.to_excel(ruta_salida, index=False)
    print(f"Pipeline ejecutado con éxito. Archivo optimizado en: {ruta_salida}")

# Ejecución principal del Pipeline
if __name__ == "__main__":
    # Sustituir con tus rutas locales o del repositorio
    archivo_origen = "datos/balance_prueba.csv"
    archivo_destino = "datos/balance_procesado.xlsx"
    
    # df_raw = extraer_datos(archivo_origen)
    # df_clean = transformar_datos(df_raw)
    # cargar_resultados(df_clean, archivo_destino)
    pass

if __name__ == "__main__":
    archivo_origen = "datos/balance_prueba.csv"
    archivo_destino = "datos/balance_procesado.xlsx"
    
    # Descomenta y ajusta según tus funciones:
    # df_raw = extraer_datos(archivo_origen)
    # df_clean = transformar_datos(df_raw)
    # cargar_resultados(df_clean, archivo_destino)
    
    print("¡Pipeline ejecutado correctamente!")



    print("Mi primer archivo versionado con Git")


