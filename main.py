# Laboratorio N°4.2 - Informática II
# Alumnos: Eberle Javier - Iñiguez Agustin
# Repositorio: [ LINK DE GITHUB] JAVO NO SE COMO SE PONE

import pandas as pd
import numpy as np

def analizar_telemetria(ruta_archivo):
    # ==========================================
    # 1. LECTURA Y PREPARACIÓN DE DATOS
    # ==========================================
    print("Cargando el archivo CSV...")
    
    # Pandas lee el CSV. 
    # parse_dates convierte la columna a formato de fecha/hora real.
    # index_col la establece como el índice (las "filas" se llamarán según la fecha).
    try:
        df = pd.read_csv(ruta_archivo, parse_dates=['timestamp'], index_col='timestamp')# aca 
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta_archivo}'. Asegúrese de que esté en la misma carpeta.")
        return None

    print("\n--- Primeras filas del dataset ---")
    print(df.head()) # Muestra los primeros 5 registros para comprobar que cargó bien
    
    # ==========================================
    # 2. ESTADÍSTICAS DESCRIPTIVAS
    # ==========================================
    print("\n--- Estadísticas Descriptivas (Pandas + Numpy) ---")
    
    # El método describe() de Pandas calcula todo automáticamente.
    # Usamos .loc para filtrar solo las filas que pide el enunciado: media, mínimo, máximo y desvío estándar.
    estadisticas = df.describe().loc[['mean', 'min', 'max', 'std']]
    
    # Redondeamos a 2 decimales para que sea legible
    print(estadisticas.round(2))
    
    return df

# Bloque principal de ejecución
if __name__ == "__main__":
    archivo_csv = "telemetria_nodo_iot.csv"
    df_nodo = analizar_telemetria(archivo_csv)
    
    if df_nodo is not None:
        print("\n¡Primer paso completado con éxito! Dataset listo en memoria.")