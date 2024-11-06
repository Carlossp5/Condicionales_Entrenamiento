# **SELECTOR DE PARAMETROS**

##### Deseamos crear una herramienta en la que le decimos la tarea que deseamos realizar y el tiempo que queremos que dure y
##### el programa nos devuelve los parametros

## 0. CARGA DE REQUERIMIENTOS

import pandas as pd
import streamlit as st

pd.set_option('display.max_rows', None)

## 1. CARGAR DATASETS

GUADALAJARA_FISICOS_AGO24 = pd.read_csv("https://raw.githubusercontent.com/Carlossp5/Condicionales_Entrenamiento/main/GUADALAJARA24-25.csv", sep=',', index_col=False)

## 2. SELECCION DE VARIABLES
df_entrenos_sel_vbles = GUADALAJARA_FISICOS_AGO24[['Player Name','Total Time','Player Position','Drill Title','Distance Total','High Speed Running (Absolute)','High Speed Running (Relative)',
                                     'HSR Per Minute (Absolute)','Sprint Distance','Sprints','Fatigue Index','HML Distance','HML Distance Per Minute','HML Efforts',
                                     'Accelerations','Max Acceleration','Decelerations','Distance Per Min','Max Speed','Dynamic Stress Load','HSR Per Minute (Relative)',
                                     'Session Type','Total Loading']]

df_entrenos_sel_vbles_sin_part = df_entrenos_sel_vbles[~df_entrenos_sel_vbles['Drill Title'].isin(['Entire Session','SEGUNDA PARTE','PRIMERA PARTE'])]

### Calculo los segundos que ha durado cada tarea
df_entrenos_sel_vbles_sin_part['Segundos_Time'] = df_entrenos_sel_vbles_sin_part['Total Time'].astype(str).str.split(':').apply(lambda x: int(x[0])*3600 + int(x[1])*60 + int(x[2]))

### Calculo el valor de cada variable por segundo
columns_to_multiply = ['Distance Total', 'High Speed Running (Absolute)', 'High Speed Running (Relative)', 
                       'HSR Per Minute (Absolute)', 'Sprint Distance', 'Sprints', 'Fatigue Index', 'HML Distance',
                       'HML Distance Per Minute', 'HML Efforts', 'Accelerations', 'Max Acceleration', 
                       'Decelerations', 'Distance Per Min', 'Max Speed', 'Dynamic Stress Load', 
                       'HSR Per Minute (Relative)', 'Total Loading']

# Iterar sobre cada columna y crear la nueva columna multiplicada
for col in columns_to_multiply:
    new_col_name = col + '_s'  # Crear el nuevo nombre con el sufijo _s
    df_entrenos_sel_vbles_sin_part[new_col_name] = df_entrenos_sel_vbles_sin_part[col] / df_entrenos_sel_vbles_sin_part['Segundos_Time']

## 3. ALGORITMO DE SELECCION DE TAREAS
df_entreno_x_tareas = df_entrenos_sel_vbles_sin_part.groupby('Drill Title').agg({
                          'Distance Total_s':'mean', 'High Speed Running (Absolute)_s':'mean','High Speed Running (Relative)_s':'mean',
                          'HSR Per Minute (Absolute)_s':'mean', 'Sprint Distance_s':'mean', 'Sprints_s':'mean',
                          'Fatigue Index_s':'mean', 'HML Distance_s':'mean', 'HML Distance Per Minute_s':'mean',
                          'HML Efforts_s':'mean', 'Accelerations_s':'mean', 'Max Acceleration_s':'mean', 'Decelerations_s':'mean',
                          'Distance Per Min_s':'mean', 'Max Speed_s':'mean', 'Dynamic Stress Load_s':'mean',
                          'HSR Per Minute (Relative)_s':'mean',
                          'Total Loading_s':'mean'
                          })

# Reseteo el indice para Drill Title sea una variable
df_entreno_x_tareas.reset_index(inplace=True)

# Inicializamos el DataFrame acumulativo
if 'acumulado' not in st.session_state:
    st.session_state.acumulado = pd.DataFrame()

def Parametros(Tarea, Tiempo):
    # Cálculo de Tiempo_s y Tiempo_m
    df_entreno_x_tareas_selec = df_entreno_x_tareas[df_entreno_x_tareas['Drill Title']==Tarea]
    Tiempo_s = Tiempo*60
    
    # Definir las columnas que quieres extraer (excepto 'Drill Title')
    columnas = [
        'Distance Total_s', 'High Speed Running (Absolute)_s', 'High Speed Running (Relative)_s',
        'HSR Per Minute (Absolute)_s', 'Sprint Distance_s', 'Sprints_s', 'Fatigue Index_s', 'HML Distance_s',
        'HML Distance Per Minute_s', 'HML Efforts_s', 'Accelerations_s', 'Max Acceleration_s', 'Decelerations_s',
        'Distance Per Min_s', 'Max Speed_s', 'Dynamic Stress Load_s'
    ]
    
    # Extraer los valores de esas columnas y multiplicarlos por Tiempo_s
    valores_multiplicados = df_entreno_x_tareas_selec[columnas] * Tiempo_s

        # Añadir las columnas 'Drill Title', 'Tiempo_s' y 'Tiempo_m'
    valores_multiplicados['Drill Title'] = Tarea
    valores_multiplicados['Tiempo'] = Tiempo
    valores_multiplicados['Tiempo_s'] = Tiempo_s
    
    # Reordenar las columnas para que 'Drill Title', 'Tiempo_s' y 'Tiempo_m' sean las primeras
    columnas_finales = ['Drill Title', 'Tiempo', 'Tiempo_s'] + columnas
    valores_multiplicados = valores_multiplicados[columnas_finales]
    valores_multiplicados.rename(columns={'Drill Title':'Tarea'}, inplace=True)

    return valores_multiplicados

## 4. Widgets de la app
# Intorduzco titulo del dashboard
def show():
    st.write("<h1 style='text-align: center;'>SELECTOR DE PARAMETROS</h1>", unsafe_allow_html=True)

    # Titulo de la barra lateral de la app
    st.sidebar.header("SELECTOR")
    
    # Crear widgets para seleccionar los parametros
    lista_variables = ['Distance Total_s', 'High Speed Running (Absolute)_s','High Speed Running (Relative)_s',
                    'HSR Per Minute (Absolute)_s', 'Sprint Distance_s', 'Sprints_s',
                    'Fatigue Index_s', 'HML Distance_s','HML Efforts_s', 'Accelerations_s', 
                    'Decelerations_s','Dynamic Stress Load_s','Total Loading_s']
    Media_vbles = ['HSR Per Minute (Absolute)_s', 'HML Distance Per Minute_s','Distance Per Min_s','HSR Per Minute (Relative)_s']
    Max_vbles = ['Max Acceleration_s', 'Max Speed_s']
    
    Tarea_1 = st.sidebar.selectbox('Selecciona la tarea:', df_entreno_x_tareas['Drill Title'].to_list())
    Tiempo_seleccion = st.sidebar.number_input('Selecciona el tiempo en minutos:', min_value=0.5, max_value=120.0, value=5.0, step=0.5)
    
    
    # # Widgets de la app para seleccionar los parametros
    if st.sidebar.button('Resultado'):
        valores_multiplicados = Parametros(Tarea_1, Tiempo_seleccion)
    
        # Mostrar el DataFrame en la interfaz de Streamlit
        st.write("Los parámetros físicos segun los ejercicios y la duración elegida son:")
        st.write(valores_multiplicados)
    
        # Acumular el resultado en el DataFrame acumulado
        st.session_state.acumulado = pd.concat([st.session_state.acumulado, valores_multiplicados], ignore_index=True)
    
    if not st.session_state.acumulado.empty:
        total_fila = {}  # Diccionario para almacenar el total por columna
    
        # Iteramos por cada columna del DataFrame acumulado
        for column in st.session_state.acumulado.columns:
            if column in Media_vbles:
                total_fila[column] = st.session_state.acumulado[column].mean()  # Calcular la media para estas variables
            elif column in Max_vbles:
                total_fila[column] = st.session_state.acumulado[column].max()   # Calcular el máximo para estas variables
            elif column not in ['Drill Title']:  # Excluir columnas no numéricas
                total_fila[column] = st.session_state.acumulado[column].sum()  # Sumar el resto de variables
            else:
                total_fila[column] = 'TOTAL'  # Colocar "TOTAL" en las columnas no numéricas
    
        # Convertimos el total en DataFrame y lo concatenamos al acumulado
        total_fila_df = pd.DataFrame([total_fila])
        acumulado_con_total = pd.concat([st.session_state.acumulado, total_fila_df], ignore_index=True)
    
        # Mostrar el DataFrame acumulado
        st.write("ENTRENAMIENTO TOTAL:")
        
        total_fila['Drill Title'] = 'TOTAL'
        total_fila_df = pd.DataFrame([total_fila])
        acumulado_con_total = pd.concat([st.session_state.acumulado, total_fila_df], ignore_index=True)
    
        st.write(acumulado_con_total)
    
    # Botón para resetear los datos acumulados
    if st.sidebar.button('Resetear acumulado'):
        st.session_state.acumulado = pd.DataFrame()  # Reinicia el acumulado
        st.write("El dataset acumulado ha sido reseteado.")
