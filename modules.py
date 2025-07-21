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

def graph_years(responses,df):
   

   por_tiendas = False
   por_tipo_de_productos = False
   fig, ax = plt.subplots() 
   ax.set_xlabel('Year', fontweight ='bold', fontsize = 15)
   ax.set_ylabel('Total sales', fontweight ='bold', fontsize = 15)   
   if "tiendas" in responses:

       por_tiendas = True
       options_tiendas = responses["tiendas"]
   elif "productos" in responses:
       por_tipo_de_productos = True 
       options_productos = responses["productos"]
   elif "tiendas_productos" in responses:
       por_tiendas = True            
       por_tipo_de_productos = True 
       options_tiendas_productos = responses["tiendas_productos"]

   if (por_tiendas == False) and (por_tipo_de_productos == False):
      df_year = df.groupby("year")["sales"].sum().to_frame().reset_index().sort_values("year")
      years = df_year.year.tolist()
      sales = df_year.sales.tolist()
      ax.plot(years,sales)
      ax.set_xticks(ticks=years)
      for year,sale in zip(years,sales):
      
         ax.scatter(year,sale,c="blue")
      downloadExcel(df_year.rename(columns = {"sales":"ventas","year":"año"}),"resultados_por_A.xlsx")


   elif por_tipo_de_productos == False:
      df_toexcel = pd.DataFrame(columns = ['year','sales','tienda'])
      for store in options_tiendas:
            nb_store = int(store.split(" ")[1])  
            df_store = df[df.store_nbr == nb_store]
            df_store_year = df_store.groupby("year")["sales"].sum().to_frame().reset_index().sort_values("year")
            years = df_store_year.year.tolist()
            sales = df_store_year.sales.tolist()            
            ax.plot(years,sales,label = str(store))
            for year,sale in zip(years,sales):
               ax.scatter(year,sale,c="blue")
            ax.set_xticks(ticks=years)
            df_store_year['tienda'] = store
            df_toexcel = pd.concat([df_toexcel,df_store_year])
      df_toexcel = df_toexcel[['tienda','year','sales']]
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","year":"año"}),"resultados_por_anio_AyT.xlsx")         

   elif por_tiendas == False:
      df_toexcel = pd.DataFrame(columns = ['year','sales','producto'])
      for producto in options_productos:
            df_producto = df[df.family == producto]
            df_producto_year = df_producto.groupby("year")["sales"].sum().to_frame().reset_index().sort_values("year")
            years = df_producto_year.year.tolist()
            sales = df_producto_year.sales.tolist()            
            ax.plot(years,sales,label = producto)
            for year,sale in zip(years,sales):
               ax.scatter(year,sale,c="blue")
            ax.set_xticks(ticks=years)
            df_producto["producto"] = producto
            df_toexcel = pd.concat([df_toexcel,df_producto])
      df_toexcel = df_toexcel[['producto','year','sales']]
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","year":"año"}),"resultados_por_anio_AyP.xlsx")       
   else:
      df_toexcel = pd.DataFrame(columns = ['year','sales','tienda','producto'])
      for tienda_producto in options_tiendas_productos:
            tienda,producto = tienda_producto
            nb_tienda = int(tienda.split(" ")[1])
            df_tienda_producto = df[(df.family == producto)&(df.store_nbr == nb_tienda)]
            df_tienda_producto_year = df_tienda_producto.groupby("year")["sales"].sum().to_frame().reset_index().sort_values("year")
            years = df_tienda_producto_year.year.tolist()
            sales = df_tienda_producto_year.sales.tolist()            
            ax.plot(years,sales,label = tienda_producto)
            for year,sale in zip(years,sales):
               ax.scatter(year,sale,c="blue")
            ax.set_xticks(ticks=years)
            df_tienda_producto_year["tienda"] = tienda
            df_tienda_producto_year["producto"] = producto
            df_toexcel = pd.concat([df_toexcel,df_tienda_producto_year])
      df_toexcel = df_toexcel[["tienda",'producto','year','sales']]
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","year":"año"}),"resultados_por_anio_AyTyP.xlsx")       

   ax.legend()
   ax.grid(True) 
   st.pyplot(fig)

def graph_monthly(responses,df_years):

   por_tiendas = False
   por_tipo_de_productos = False
   fig, ax = plt.subplots() 
   ax.set_xlabel('Month', fontweight ='bold', fontsize = 15)
   ax.set_ylabel('Total sales', fontweight ='bold', fontsize = 15)   
   if "tiendas" in responses:

       por_tiendas = True
       options_tiendas = responses["tiendas"]
   elif "productos" in responses:
       por_tipo_de_productos = True 
       options_productos = responses["productos"]
   elif "tiendas_productos" in responses:
       por_tiendas = True            
       por_tipo_de_productos = True 
       options_tiendas_productos = responses["tiendas_productos"]    

   if (por_tiendas == False) and (por_tipo_de_productos == False):
      df_month_year = df_years.groupby(["year","month"])["sales"].sum().to_frame().reset_index().sort_values("month")
      df_month = df_month_year.groupby("month")["sales"].mean().to_frame().reset_index().sort_values("month")
      months = df_month.month.tolist()
      sales = df_month.sales.tolist() 
      ax.plot(months,sales)
      ax.set_xticks(ticks=months)
      for month,sale in zip(months,sales):
      
         ax.scatter(month,sale,c="blue")

   elif por_tipo_de_productos == False:
      for store in options_tiendas:
            nb_store = int(store.split(" ")[1])  
            df_store = df_years[df_years.store_nbr == nb_store]
            df_store_year_month = df_store.groupby(["year","month"])["sales"].sum().to_frame().reset_index().sort_values("month")
            df_store_month = df_store_year_month.groupby("month")["sales"].mean().to_frame().reset_index().sort_values("month")
            months = df_store_month.month.tolist()
            sales = df_store_month.sales.tolist()            
            ax.plot(months,sales,label = str(store))
            for month,sale in zip(months,sales):
               ax.scatter(month,sale,c="blue")
            ax.set_xticks(ticks=months)   

   elif por_tiendas == False:
      for producto in options_productos:
            df_producto = df_years[df_years.family == producto]
            df_producto_year_month = df_producto.groupby(["year","month"])["sales"].sum().to_frame().reset_index().sort_values("month")
            df_producto_month = df_producto_year_month.groupby("month")["sales"].mean().to_frame().reset_index().sort_values("month")
            months = df_producto_month.month.tolist()
            sales = df_producto_month.sales.tolist()            
            ax.plot(months,sales,label = producto)
            for month,sale in zip(months,sales):
               ax.scatter(month,sale,c="blue")
            ax.set_xticks(ticks=months)   
   else:
      for tienda_producto in options_tiendas_productos:
            tienda,producto = tienda_producto
            nb_tienda = int(tienda.split(" ")[1])
            df_tienda_producto = df_years[(df_years.family == producto)&(df_years.store_nbr == nb_tienda)]
            df_tienda_producto_year_month = df_tienda_producto.groupby(["year","month"])["sales"].sum().to_frame().reset_index().sort_values("month")
            df_tienda_producto_month = df_tienda_producto_year_month.groupby("month")["sales"].mean().to_frame().reset_index().sort_values("month")
            months = df_tienda_producto_month.month.tolist()
            sales = df_tienda_producto_month.sales.tolist()            
            ax.plot(months,sales,label = tienda_producto)
            for month,sale in zip(months,sales):
               ax.scatter(month,sale,c="blue")
            ax.set_xticks(ticks=months)   
   ax.legend()
   ax.grid()
   st.pyplot(fig)               

def graph_monthly_by_year(responses,df):

   por_tiendas = False
   por_tipo_de_productos = False
   fig, ax = plt.subplots() 
   ax.set_xlabel('Month', fontweight ='bold', fontsize = 15)
   ax.set_ylabel('Total sales', fontweight ='bold', fontsize = 15)   
   if "tiendas" in responses:

       por_tiendas = True
       options_tiendas = responses["tiendas"]
   elif "productos" in responses:
       por_tipo_de_productos = True 
       options_productos = responses["productos"]
   elif "tiendas_productos" in responses:
       por_tiendas = True            
       por_tipo_de_productos = True 
       options_tiendas_productos = responses["tiendas_productos"]

   years = df.sort_values("year")["year"].unique()

   for year in years:
      df_years = df[df.year == year]
      if (por_tiendas == False) and (por_tipo_de_productos == False):
         df_month = df_years.groupby("month")["sales"].sum().to_frame().reset_index().sort_values("month")
         months = df_month.month.tolist()
         sales = df_month.sales.tolist() 
         ax.plot(months,sales,label=str(year))
         ax.set_xticks(ticks=months)
         for month,sale in zip(months,sales):
            ax.scatter(month,sale,c="blue")

      elif por_tipo_de_productos == False:
         for store in options_tiendas:
            nb_store = int(store.split(" ")[1])  
            df_store = df_years[df_years.store_nbr == nb_store]
            df_store_month = df_store.groupby("month")["sales"].sum().to_frame().reset_index().sort_values("month")
            months = df_store_month.month.tolist()
            sales = df_store_month.sales.tolist()            
            ax.plot(months,sales,label = str(store)+ " " + str(year))
            for month,sale in zip(months,sales):
               ax.scatter(month,sale,c="blue")
            ax.set_xticks(ticks=months)   

      elif por_tiendas == False:
         for producto in options_productos:
            df_producto = df_years[df_years.family == producto]
            df_producto_month = df_producto.groupby("month")["sales"].sum().to_frame().reset_index().sort_values("month")
            months = df_producto_month.month.tolist()
            sales = df_producto_month.sales.tolist()            
            ax.plot(months,sales,label = producto + " " + str(year))
            for month,sale in zip(months,sales):
               ax.scatter(month,sale,c="blue")
            ax.set_xticks(ticks=months)   
      else:
         for tienda_producto in options_tiendas_productos:
            tienda,producto = tienda_producto
            nb_tienda = int(tienda.split(" ")[1])
            df_tienda_producto = df_years[(df_years.family == producto)&(df_years.store_nbr == nb_tienda)]
            df_tienda_producto_month = df_tienda_producto.groupby("month")["sales"].sum().to_frame().reset_index().sort_values("month")
            months = df_tienda_producto_month.month.tolist()
            sales = df_tienda_producto_month.sales.tolist()            
            ax.plot(months,sales,label = tienda_producto + " " + str(year))
            for month,sale in zip(months,sales):
               ax.scatter(month,sale,c="blue")
            ax.set_xticks(ticks=months)   
   ax.legend()
   ax.grid()
   st.pyplot(fig)                  