import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from toExcel import downloadExcel

def first_page():
    
    # Cargar datos
   sales_by_date = pd.read_csv("sales_by_date.csv", parse_dates=["date"])
   sales_by_store = pd.read_csv("sales_by_store.csv")
   sales_by_family = pd.read_csv("sales_by_family.csv")

   # Sección 1: Evolución de ventas en el tiempo
   st.header("Evolución de ventas en el tiempo")
   fig, ax = plt.subplots()
   ax.plot(sales_by_date["date"], sales_by_date["sales"], label="Ventas diarias")
   ax.set_xlabel("Fecha")
   ax.set_ylabel("Ventas")
   ax.set_title("Ventas totales por día")
   st.pyplot(fig)

   # Sección 2: Ventas por tienda
   st.header("Ventas por tienda")
   st.bar_chart(data=sales_by_store, x="store_nbr", y="sales")

   # Sección 3: Ventas por familia de productos
   st.header("Ventas por familia de productos")
   top_families = sales_by_family.head(15)
   st.bar_chart(data=top_families, x="family", y="sales")

def first_questions(por_tiendas,por_tipo_de_productos,df):

    responses = {}

    if por_tiendas and por_tipo_de_productos == False:
      opt = [f"Tienda {tienda}" for tienda in df.sort_values("store_nbr").store_nbr.astype(str).unique()]
      options_tiendas = st.multiselect(
       "Qué tiendas quieres analizar",
        default=[],
        options=opt
        )
      responses.update({"tiendas":options_tiendas}) 

    if por_tipo_de_productos and por_tiendas == False:
      options_productos = st.multiselect(
       "Qué tipo de productos quieres analizar",
        default=[],
        options=list(df.sort_values("family").family.unique())
        )  
      responses.update({"productos":options_productos})     
    if por_tiendas and por_tipo_de_productos:
      opt = df[["store_nbr","family"]].value_counts().to_frame().reset_index()[["store_nbr","family"]].sort_values(["store_nbr","family"]).values
      opt = [(f"Tienda {elt[0]}",elt[1]) for elt in opt]
      options_tiendas_productos = st.multiselect(
       "Qué tiendas y productos quieres analizar",
        default=[],
        options=opt
        )    
      responses.update({"tiendas_productos":options_tiendas_productos})

    return responses

