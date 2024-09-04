import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from st_aggrid import AgGrid, GridOptionsBuilder

# Configurar la página para tener un layout amplio
st.set_page_config(layout="wide")

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener las credenciales desde las variables de entorno
USERNAME = os.getenv("USER")
PASSWORD = os.getenv("PASS")

# Inicializar el estado de la sesión para la autenticación
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Inicializar claves para los selectboxes de los gráficos
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'password' not in st.session_state:
    st.session_state.password = ''
if 'x_col' not in st.session_state:
    st.session_state.x_col = ''
if 'y_col' not in st.session_state:
    st.session_state.y_col = ''
if 'hist_col' not in st.session_state:
    st.session_state.hist_col = ''


# Función para manejar el inicio de sesión
def login():
    if st.session_state.username == USERNAME and st.session_state.password == PASSWORD:
        st.session_state.authenticated = True
        st.sidebar.success("¡Autenticación exitosa!")
    else:
        st.sidebar.error("Usuario o clave incorrectos")


# Función para manejar el cierre de sesión
def logout():
    st.session_state.authenticated = False


# Barra lateral de la aplicación
with st.sidebar:
    st.title("Barra Lateral")
    if not st.session_state.authenticated:
        st.text_input("Usuario", key="username")
        st.text_input("Clave", type="password", key="password")
        st.button("Iniciar sesión", on_click=login)
    else:
        st.button("Cerrar sesión", on_click=logout)
        st.write("---")
        st.write("Navegación")
        page = st.selectbox("Selecciona una página", ["Dotación", "CAI", "Jerarquía"])

# Contenido principal de la aplicación
if not st.session_state.authenticated:
    st.title("Autenticación Simple")
    st.write("Por favor, inicia sesión para continuar.")
else:
    if page == "Dotación":
        st.title("Inicio")
        tab1, tab2, tab3 = st.tabs(["Resumen", "Detalles", "Estadísticas"])

        with tab1:
            st.header("Resumen")
            st.write("Contenido del Resumen")

        with tab2:
            st.header("Detalles")
            st.write("Contenido de los Detalles")

        with tab3:
            st.header("Estadísticas")
            st.write("Contenido de las Estadísticas")

    elif page == "CAI":
        st.title("Análisis de Datos")
        tab1, tab2, tab3 = st.tabs(["Carga de Datos", "Visualización", "Resultados"])

        with tab1:
            st.header("Carga de Datos")


            # Cargar el dataset mtcars desde la carpeta raíz
            @st.cache_data
            def load_data():
                df = pd.read_parquet('DIM.FT_GRADO_ACADEMICO_DOCENTE.parquet', engine='pyarrow')
                #df = pd.read_csv('mtcars.csv')
                return df


            df = load_data()

            # Mostrar estadísticas clave
            st.subheader("Estadísticas Clave")

            # Crear columnas para tarjetas informativas horizontales
            col1, col2, col3 = st.columns(3)

            # Número de casos
            num_cases = len(df)
            col1.markdown(f"""
            <div style="background-color:#36C2CE; padding: 10px; border-radius: 5px; color: white; text-align: center;">
                <h4>Número de Casos</h4>
                <p style="font-size: 24px; margin: 0;">{num_cases}</p>
            </div>
            """, unsafe_allow_html=True)

            # Promedio de mpg
            avg_mpg = df['ID_GRADO_ACADEMICO'].mean()
            col2.markdown(f"""
            <div style="background-color:#36C2CE; padding: 10px; border-radius: 5px; color: white; text-align: center;">
                <h4>Promedio de mpg</h4>
                <p style="font-size: 24px; margin: 0;">{avg_mpg:.2f}</p>
            </div>
            """, unsafe_allow_html=True)

            # Promedio de cyl
            avg_cyl = df['ID_INSTITUCION_ESTUDIO'].mean()
            col3.markdown(f"""
            <div style="background-color:#36C2CE; padding: 10px; border-radius: 5px; color: white; text-align: center;">
                <h4>Promedio de cyl</h4>
                <p style="font-size: 24px; margin: 0;">{avg_cyl:.2f}</p>
            </div>
            """, unsafe_allow_html=True)

            # Mostrar el dataset con funcionalidades de búsqueda
            st.write("GRADO ACADËMICO:")


        with tab2:
            st.header("Visualización")

            # Crear gráficos
            st.subheader("Gráfico de dispersión")
            x_col = st.selectbox("Selecciona la variable X", df.columns, key="x_col")
            y_col = st.selectbox("Selecciona la variable Y", df.columns, key="y_col")

            if x_col and y_col:
                fig, ax = plt.subplots()
                sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
                st.pyplot(fig)

            st.subheader("Histograma")
            hist_col = st.selectbox("Selecciona la variable para el histograma", df.columns, key="hist_col")

            if hist_col:
                fig, ax = plt.subplots()
                sns.histplot(df[hist_col], kde=True, ax=ax)
                st.pyplot(fig)

        with tab3:
            st.header("Resultados")
            st.write("Contenido de los Resultados")

    elif page == "Jerarquía":
        st.title("Configuración")
        tab1, tab2, tab3 = st.tabs(["Perfil", "Preferencias", "Seguridad"])

        with tab1:
            st.header("Perfil")
            st.write("Contenido del Perfil")

        with tab2:
            st.header("Preferencias")
            st.write("Contenido de las Preferencias")

        with tab3:
            st.header("Seguridad")
            st.write("Contenido de la Seguridad")
