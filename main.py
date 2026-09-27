# Laboratorio N°4.2 - Informática II
# Alumnos: Eberle Javier - Iñiguez Agustin
# Repositorio: [PEGA AQUÍ TU LINK DE GITHUB]

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analizar_telemetria(ruta_archivo):
    # ==========================================
    # 1. LECTURA Y PREPARACIÓN DE DATOS
    # ==========================================
    print("Cargando el archivo CSV...")
    
    try:
        df = pd.read_csv(ruta_archivo, parse_dates=['timestamp'], index_col='timestamp')
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta_archivo}'. Asegúrese de que esté en la misma carpeta.")
        return None

    print("\n--- Primeras filas del dataset ---")
    print(df.head())
    
    # ==========================================
    # 2. ESTADÍSTICAS DESCRIPTIVAS
    # ==========================================
    print("\n--- Estadísticas Descriptivas (Pandas + Numpy) ---")
    
    estadisticas = df.describe().loc[['mean', 'min', 'max', 'std']]
    print(estadisticas.round(2))
    
    # ==========================================
    # 3. DETECCIÓN DE ALERTAS (Numpy)
    # ==========================================
    print("\n--- Detección de Alertas ---")
    voltaje_np = df['voltaje_bateria_V'].to_numpy()
    rssi_np = df['rssi_dbm'].to_numpy()
    
    alerta_bateria = voltaje_np < 3.5
    alerta_rssi = rssi_np < -85
    alerta_cualquiera = alerta_bateria | alerta_rssi 
    
    print(f"Registros con batería baja (< 3.5V): {np.sum(alerta_bateria)}")
    print(f"Registros con señal débil (< -85 dBm): {np.sum(alerta_rssi)}")
    print(f"Registros con al menos una alerta: {np.sum(alerta_cualquiera)}")
    
    # Guardamos el resultado en el DataFrame para usarlo luego
    df['alerta'] = alerta_cualquiera
    
    # ==========================================
    # 4. VISUALIZACIÓN (Matplotlib)
    # ==========================================
    print("\nGenerando gráfico de evolución temporal...")
    fig, ax1 = plt.subplots(figsize=(10, 5))
    
    color1 = 'tab:red'
    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('Temperatura (°C)', color=color1)
    ax1.plot(df.index, df['temperatura_C'], color=color1, label='Temperatura')
    ax1.tick_params(axis='y', labelcolor=color1)
    
    ax2 = ax1.twinx()
    color2 = 'tab:blue'
    ax2.set_ylabel('Voltaje Batería (V)', color=color2)
    ax2.plot(df.index, df['voltaje_bateria_V'], color=color2, label='Voltaje')
    ax2.tick_params(axis='y', labelcolor=color2)
    
    fechas_alertas = df[df['alerta']].index
    voltajes_alertas = df[df['alerta']]['voltaje_bateria_V']
    ax2.scatter(fechas_alertas, voltajes_alertas, color='black', marker='X', s=50, label='Alerta', zorder=5)
    
    plt.title('Evolución de Temperatura y Voltaje con Alertas')
    fig.tight_layout()
    plt.show(block=False)
    
    # ==========================================
    # 5. AGRUPACIÓN POR DÍA (Resumen)
    # ==========================================
    print("\n--- Generando Resumen Diario ---")
    resumen_diario = df.resample('D').agg({
        'temperatura_C': ['mean', 'max', 'min'],
        'voltaje_bateria_V': ['mean', 'min'],
        'alerta': 'sum' 
    })
    
    resumen_diario.columns = [
        'Temp_Promedio', 'Temp_Max', 'Temp_Min', 
        'Voltaje_Promedio', 'Voltaje_Min', 
        'Cantidad_Alertas'
    ]
    print(resumen_diario.head())

    # ==========================================
    # 6. EXPORTAR A EXCEL
    # ==========================================
    print("\n--- Exportando a Excel ---")
    nombre_excel = "resumen_diario_nodo.xlsx"
    try:
        resumen_diario.to_excel(nombre_excel, sheet_name="Resumen diario")
        print(f"¡Éxito! El resumen ha sido exportado a '{nombre_excel}'.")
    except Exception as e:
        print(f"Error al exportar a Excel: {e}")
        print("Recuerda que debes tener instalada la librería openpyxl (pip install openpyxl).")

    # ¡El error de indentación está arreglado aquí!
    return df

# Bloque principal de ejecución
if __name__ == "__main__":
    archivo_csv = "telemetria_nodo_iot.csv"
    df_nodo = analizar_telemetria(archivo_csv)
    
    if df_nodo is not None:
        # Esto mantiene la ventana del gráfico abierta
        plt.show()