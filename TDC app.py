import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from Scraping2 import ejecutar_scraping
from Scraping2 import to_excel
from io import BytesIO

st.set_page_config(page_title="TDC App",layout="centered")


años = ["2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023", "2024","2025"]

municipios = {
    "Administración Central":"1",
    "Ciudad de Mendoza":"52",
    "General Alvear":"53",
    "Godoy Cruz":"54",
    "Guaymallén":"55",
    "Junín":"56",
    "La Paz":"57",
    "Las Heras":"58",
    "Lavalle":"59",
    "Luján de Cuyo":"60",
    "Maipú":"61",
    "Malargüe":"62",
    "Rivadavia":"63",
    "San Carlos":"64",
    "San Martín":"65",
    "San Rafael":"66",
    "Santa Rosa":"67",
    "Tunuyán":"68",
    "Tupungato":"69"
}

trimestres = ["1", "2", "3", "4"]

anexos = {
    "2 - DE LA EJECUCION DEL PRESUPUESTO CON RELACION A LOS CREDITOS ACUMULADA AL FIN DEL TRIMESTRE": "EjePreCreAcu",
    "2 bis - DE LA EJECUCION DEL PRESUPUESTO CON RELACION A LOS CREDITOS CORRESPONDIENTE AL TRIMESTRE": "EjePreRelCre",
    "3 - DE LA EJECUCION DEL PRESUPUESTO CON RELACION AL CALCULO DE RECURSOS Y FINANCIAMIENTO ACUMULAD...": "EjePreCalRecFinAcu",
    "5 - EVOLUCION DE LA DEUDA PÚBLICA CONSOLIDADA ACUMULADA AL FIN DEL TRIMESTRE": "EvoDeuConAcu",
    "6 - EVOLUCION DE LA DEUDA FLOTANTE ACUMULADA AL FIN DEL TRIMESTRE": "EvoDeuFloAcu",
    "17 - DETALLE DE JUICIOS EN EJECUCION Según Art 30 inc a) y Art 34 inc f)": "DetJuiEjec",
    "19 - DETALLE DE LA PLANTA DE PERSONAL Y CONTRATOS DE LOCACION. IMPORTES LIQUIDADOS ACUMULADOS AL …": "DetPerPlaLocImpLiqAcu",
    "22 - INFORME CINCUENTA PRINCIPALES CONTRIBUYENTES CON DEUDA Según Art 34 inc d) por cada uno de l...": "InfContDeuDerTasRee",
    "23 - INFORME DE MOROSIDAD Según Art 34 inc d) por cada uno de los Derechos, Tasas Municipales y R...": "InfMorDerTasRee"
}

st.header("Bienvenido a uno de mis proyectos")

st.write("""
Esta aplicación mejora la experiencia del usuario para navegar y consultar la página del Tribunal de Cuentas de Mendoza, 
facilitando la extracción de los datos. Permite la consulta de varios años y trimestres al mismo tiempo, junto con la opción de poder exportar los datos en formato Excel.

Podés acceder a la página original del Tribunal de Cuentas [aquí](http://app.tribunaldecuentas.mendoza.gov.ar/leyrespfiscal/Consultas.php) para comparar la experiencia.

""")

with st.form("formulario_consulta"):
    st.header("Tribunal de cuentas - Mendoza")
    st.subheader("Realiza tu consulta:")# título dentro del formulario

    lista_municipio = st.selectbox("Selecciona el Municipio:", list(municipios.keys()))
    municipio_numero = municipios[lista_municipio]

    lista_año = st.multiselect("Selecciona uno o más años:", sorted(años, reverse=True), default=["2024"])
    lista_trimestre = st.multiselect("Selecciona uno o más trimestres:", trimestres, default=["4"])
    lista_anexo = st.selectbox("Selecciona el Informe:", list(anexos.keys()))
    anexo_codigo = anexos[lista_anexo]

    submitted = st.form_submit_button("Realizar consulta")

if submitted:
    try:
        funcion = ejecutar_scraping(lista_año, lista_trimestre, municipio_numero, anexo_codigo)
        funcion["Municipio"] = lista_municipio
        
        st.markdown('<p style="color:green; font-weight:bold;">Finalizado ✅</p>', unsafe_allow_html=True)
        st.dataframe(funcion)
        excel_data = to_excel(funcion)
    
        st.download_button(
            label="Descargar el archivo en formato Excel",
            data=excel_data,
            file_name=f"{lista_municipio}_datos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except ValueError as e:
        st.warning(f"Error durante la consulta: {e}. Por favor verificá que los años y trimestres seleccionados sean válidos.")
