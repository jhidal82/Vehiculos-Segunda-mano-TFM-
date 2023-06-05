
import streamlit as st
from funciones import prediccion_precio,mostrar_dataframe,histograma_precios,\
                      grafico_evolucion_precio,mapa_ubicacion,menu_principal,\
                      analisis_datos    
                          
import pandas as pd
df_streamlit = pd.read_csv("df_streamlit.csv",sep=",")
# Configuración de la página


# Configuración de la página
st.set_page_config(page_title="Coches Segunda mano")


st.image("coches1.jpg", use_column_width=True)


st.title("COCHES DE SEGUNDA MANO")

# Opciones de funciones
st.sidebar.write("En esta Web, podras obtener toda la información necesaria\
                              de nuestro conjunto de vehiculos de segunda mano.")

opcion = st.sidebar.selectbox("SELECCIONA UNA FUNCIÓN:"                              
                              ,("MENU PRINCIPAL", "CONJUNTO DE VEHICULOS","CALCULAR PRECIO DE UN VEHICULO", "RELACION KMS PRECIO", 
                                "DISTRIBUCIÓN POR PRECIOS","UBICACION DE VEHICULOS","ANALISIS DE DATOS " ))

st.sidebar.image("coches2.jpg", use_column_width=True)


# Ejecutar función seleccionada
if opcion == "MENU PRINCIPAL":
    menu_principal()

elif opcion == "CALCULAR PRECIO DE UN VEHICULO":
    prediccion_precio()
elif opcion == "RELACION KMS PRECIO":
    grafico_evolucion_precio(df_streamlit)
elif opcion == "CONJUNTO DE VEHICULOS":
    mostrar_dataframe(df_streamlit)
elif opcion == "DISTRIBUCIÓN POR PRECIOS":
    histograma_precios(df_streamlit)
elif opcion == "UBICACION DE VEHICULOS":
    mapa_ubicacion (df_streamlit)   
elif opcion == "ANALISIS DE DATOS ":
    analisis_datos (df_streamlit)  

