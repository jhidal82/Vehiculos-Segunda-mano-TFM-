


def prediccion_precio():
    import streamlit as st
    import pandas as pd
    import pickle
    from datetime import datetime

    df = pd.read_csv("df_streamlit.csv",sep=",") # lo usamos para generar los campos 
    
    with open("modelo.pkl2", 'rb') as f: # cargamos modelo de prediccion
        modelo_cargado = pickle.load(f)
 

    # interfaz de usuario
    st.title('Predicción de precios de vehículos')
    st.write('Introduce los siguientes datos para obtener la predicción del precio del vehículo:')
    
    col1, col2 = st.columns(2)

    #INTERVALOS PARA LOS CAMPOS
    
    marcas_unicas = df['make'].unique().tolist()
    transmision_unicas = df["shift"].unique().tolist()
    potencias_unicas= df['power'].unique().tolist()
    fuel_unicas = df['fuel'].unique().tolist()
    list_year = list(range(1996, 2024))
    default_index = list_year.index(2020)
    
    # CAMPOS DE ENTRADA
    col1, col2 = st.columns(2)
    with col1:
        #seleccionamos marca
        Marca = st.selectbox('MARCA:', options=marcas_unicas)

        # Una vez que el usuario elige la marca, filtramos por los modelos sólo de esa marca

        df_filtrado = df[df['make'] == Marca]
        modelos_Unicos = df_filtrado['model'].unique().tolist()

        # seleccionamos modelo
        Modelo  = st.selectbox('MODELO:',options = modelos_Unicos)
        
        # Aplicamos filtros
        
        df_filtrado2 = df[(df['make'] == Marca) & (df['model'] == Modelo)]
        fuel_unicas=df_filtrado2['fuel'].unique().tolist()
        potencias_unicas=df_filtrado2['power'].unique().tolist()
        transmision_unicas=df_filtrado2['shift'].unique().tolist()
        kms = st.number_input('Kilómetros recorridos:')
        transmision = st.selectbox('Tipo de transmisión:', options=transmision_unicas)
        
    with col2:  
        power = st.selectbox('Potencia del vehículo:',options = potencias_unicas)  
        fuel = st.selectbox('Tipo de combustible :',options = fuel_unicas)    
        año_vehiculo = st.selectbox('Año del vehículo:',options = list_year,index=default_index)


    #TRANSFORMAR LOS DATOS SELECCIONADOS POR EL USUARIO:

    #Transformar Marca y modelo
    # cargamos el diccionario utilizado para la codificacion para hacer la conversion de marca_modelo a numero.
    with open('precio_numerico_dict2.pkl', 'rb') as f:
        precio_numerico_dict = pickle.load(f)

    marca_modelo_seleccionado = Marca + ' ' + Modelo
    marca_modelo_transformado = precio_numerico_dict.get(marca_modelo_seleccionado)
    
    # transformar la transmisión seleccionada
    mapeo_transmision = {'manual': 0, 'automatic': 1}
    transmision_transformada = mapeo_transmision[transmision]

   

    # transformar fuel
    mapeo_fuel = {'Diésel': 1, 'Gasolina': 0, 'Eléctrico': 2} 
    fuel_transformada=mapeo_fuel[fuel]

    # transformar año el vehiculo:
    año_actual = datetime.now().year
    antiguedad = año_actual - año_vehiculo

 
    # Crear un DataFrame con los datos introducidos por el usuario

    nuevos_datos = pd.DataFrame({
        'marca_modelo_codificada': [marca_modelo_transformado],
        'kms': [kms],
        'shift_codificada': [transmision_transformada],
        'power': [power],
        'fuel_codificada': [fuel_transformada],
        'years_old': [antiguedad]
    })

    # Realizar la predicción utilizando el modelo cargado
    prediccion_precio = modelo_cargado.predict(nuevos_datos)
    import numpy as np

    # Redondear los valores a dos decimales
    prediccion_precio_redondeado = np.round(prediccion_precio, decimals=2)

    # Formatear los valores con el símbolo de € y separador de miles
    precios_formateados = ["{:,.2f} €".format(valor) for valor in prediccion_precio_redondeado]

    st.subheader('Predicción del precio:')
    for precio_formateado in precios_formateados:
        st.success(f"**PRECIO:** {precio_formateado}")

   
   
   
    
def mostrar_dataframe(df):    
    import streamlit as st
    import pandas as pd
    
    st.write('A continuación mostramos el conjunto de vehiculos de segunda mano disponibles,\
                puedes seleccionar y filtrar según tus preferencias:')
    marcas_unicas = df['make'].unique()
    marcas_unicas = df['make'].unique()

    # Filtrar el dataframe por marca seleccionada
    marca_seleccionada = st.selectbox('Selecciona una marca', marcas_unicas)
    df_filtrado = df[df['make'] == marca_seleccionada]

    # Obtener los modelos correspondientes a la marca seleccionada
    modelos_unicos = df_filtrado['model'].unique()

    # Filtrar por modelo seleccionado
    modelo_seleccionado = st.selectbox('Selecciona un modelo', modelos_unicos)
    st.write(df_filtrado[df_filtrado['model'] == modelo_seleccionado])








def histograma_precios(df):
    import streamlit as st
    import matplotlib.pyplot as plt
    st.write('Selecciona un rango de precios y te mostramos el nº de vehiculos de nuestro conjunto de datos que se encuentran dentro\
              de ese intervalo:')
    # Obtener el rango de precios mínimo y máximo en el dataframe
    precio_min = df['price'].min()
    precio_max = 50000#df['price'].max()

    # Agregar un control deslizante para que el usuario seleccione el rango de precios
    rango_precios = st.slider('Rango de precios', float(precio_min), float(precio_max), (float(precio_min), float(precio_max)))

    # Filtrar el dataframe en base al rango de precios seleccionado por el usuario
    df_filtrado = df[(df['price'] >= rango_precios[0]) & (df['price'] <= rango_precios[1])]

    # Crear un histograma de precios con el dataframe filtrado
    fig, ax = plt.subplots()
    ax.hist(df_filtrado['price'], bins=30)

    # Configurar el título y etiquetas de los ejes
    ax.set_title('Distribución de precios de los coches')
    ax.set_xlabel('Precio')
    ax.set_ylabel('Frecuencia')

    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)



def grafico_evolucion_precio(df):
    import streamlit as st
    import matplotlib.pyplot as plt
    st.write('Selecciona  marca y modelo y obtendrás el precio medio por años de ese vehiculo según\
              el conjunto de datos de vehiculos que tenemos:')
     # Obtener la lista de marcas únicas en el dataframe
    marcas = df['make'].unique()

    # Agregar un selectbox para que el usuario elija una marca
    marca_seleccionada = st.selectbox('Selecciona una marca', marcas)

    # Filtrar el dataframe por la marca seleccionada
    df_filtrado_marca = df[df['make'] == marca_seleccionada]

    # Obtener la lista de modelos únicos para la marca seleccionada
    modelos = df_filtrado_marca['model'].unique()

    # Agregar un selectbox para que el usuario elija un modelo de la marca seleccionada
    modelo_seleccionado = st.selectbox('Selecciona un modelo', modelos)

    # Filtrar el dataframe por la marca y modelo seleccionados
    df_filtrado_modelo = df_filtrado_marca[df_filtrado_marca['model'] == modelo_seleccionado]

    # Calcular el precio medio para la marca y modelo seleccionados en cada año
    precio_medio_por_año = df_filtrado_modelo.groupby('year')['price'].mean()

    # Crear el gráfico de línea con el precio medio en cada año
    fig, ax = plt.subplots()
    ax.plot(precio_medio_por_año.index, precio_medio_por_año.values)
    ax.set_xlabel('Año')
    ax.set_ylabel('Precio Medio')
    ax.set_title(f'Evolución del precio medio para {marca_seleccionada} {modelo_seleccionado}')

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)
    
    





def mapa_ubicacion(df):
    import pandas as pd
    import streamlit as st
    import folium
    from streamlit_folium import st_folium
    st.write('Te ayudamos a localizar, dónde se encuentran nuestros vehiculos, navega por el mapa \
             y obtendrás la ubicación exacta:')
    df = pd.read_csv("location_df.csv", sep=",")

    # Obtener las opciones únicas de marca y modelo
    unique_makes = df['make'].unique()

    # Widget para seleccionar marca
    selected_make = st.selectbox("Selecciona la marca:", unique_makes)

    # Filtrar el dataframe por la marca seleccionada
    filtered_df = df[df['make'] == selected_make]

    # Obtener las opciones únicas de modelo correspondientes a la marca seleccionada
    unique_models = filtered_df['model'].unique()

    # Widget para seleccionar modelo
    selected_model = st.selectbox("Selecciona el modelo:", unique_models)

    # Filtrar aún más el dataframe por la marca y el modelo seleccionados
    filtered_df = filtered_df[filtered_df['model'] == selected_model]

    # Crear el mapa utilizando Folium
    mapa = folium.Map()

    # Agregar marcadores al mapa para cada registro en el dataframe filtrado
    for _, row in filtered_df.iterrows():
        lat = row['latitude']
        lon = row['longitude']
        localizacion= row['location']
        folium.Marker(location=[lat, lon],tooltip=localizacion).add_to(mapa)

    # Mostrar el mapa en Streamlit
    st_folium(mapa)



def menu_principal():
    import streamlit as st

    
    with open("coches4.jpg", "rb") as file:
        imagen_data = file.read()
        st.image(imagen_data)



def analisis_datos(df):
    import streamlit as st
    import pandas_profiling
    from streamlit_pandas_profiling import st_profile_report
    st.write("ANALISIS DEL CONJUNTO DE VEHICULOS:")

    pr = df.profile_report()

    st_profile_report(pr)