import pandas as pd

def cruzar_nomina_y_novedades(ruta_nomina: str, ruta_novedades: str, ruta_salida: str):
    """
    Lee los archivos de nómina y novedades, realiza un merge por Cédula
    y calcula las diferencias en días/horas reportadas.
    """
    # 1. Cargar archivos de Excel
    df_nomina = pd.read_excel(ruta_nomina)
    df_novedades = pd.read_excel(ruta_novedades)

    # 2. Limpieza básica de nombres de columnas y eliminación de espacios
    df_nomina.columns = df_nomina.columns.str.strip()
    df_novedades.columns = df_novedades.columns.str.strip()

    # Asegurar que la Cédula se trate como texto para evitar errores de formato
    df_nomina['Cedula'] = df_nomina['Cedula'].astype(str).str.strip()
    df_novedades['Cedula'] = df_novedades['Cedula'].astype(str).str.strip()

    # 3. Consolidar o agrupar novedades si un empleado tiene múltiples registros
    novedades_agrupadas = df_novedades.groupby('Cedula', as_index=False).agg({
        'Dias_Novedad': 'sum',
        'Horas_Extra': 'sum'
    })

    # 4. Cruzar información (Outer join para detectar empleados faltantes en alguno de los dos lados)
    df_cruce = pd.merge(
        df_nomina, 
        novedades_agrupadas, 
        on='Cedula', 
        how='outer', 
        suffixes=('_nomina', '_novedades')
    )

    # Rellenar valores nulos con 0 para realizar operaciones matemáticas
    df_cruce['Dias_Pagados'] = df_cruce['Dias_Pagados'].fillna(0)
    df_cruce['Dias_Novedad'] = df_cruce['Dias_Novedad'].fillna(0)

    # 5. Cálculo de discrepancias
    # Ejemplo: Días pagados vs (Días base del periodo - Días de novedad)
    DIAS_BASE_QUINCENA = 15
    df_cruce['Dias_Esperados'] = DIAS_BASE_QUINCENA - df_cruce['Dias_Novedad']
    df_cruce['Diferencia_Dias'] = df_cruce['Dias_Pagados'] - df_cruce['Dias_Esperados']

    # Clasificación del hallazgo
    df_cruce['Estado_Revision'] = df_cruce['Diferencia_Dias'].apply(
        lambda x: 'Correcto' if x == 0 else ('Pago en exceso' if x > 0 else 'Pago faltante')
    )

    # 6. Exportar resultados a Excel
    with pd.ExcelWriter(ruta_salida, engine='openpyxl') as writer:
        df_cruce.to_excel(writer, sheet_name='Cruce_Consolidado', index=False)
        # Filtrar solo las inconsistencias en una pestaña independiente
        df_cruce[df_cruce['Estado_Revision'] != 'Correcto'].to_excel(
            writer, sheet_name='Discrepancias', index=False
        )

    print(f"Proceso finalizado con éxito. Reporte guardado en: {ruta_salida}")

# Ejemplo de ejecución
if __name__ == "__main__":
    cruzar_nomina_y_novedades(
        ruta_nomina="Acumulados_Nomina.xlsx",
        ruta_novedades="Reporte_Novedades.xlsx",
        ruta_salida="Resultado_Cruce_Nomina.xlsx"
    )