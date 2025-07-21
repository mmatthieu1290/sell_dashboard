import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from toExcel import downloadExcel

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
      downloadExcel(df_year.rename(columns = {"sales":"ventas","year":"año"}),"resultados_por_año.xlsx")


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
      df_toexcel = df_toexcel[['tienda','year','sales']].sort_values(["tienda","year"])
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","year":"año"}),"resultados_por_año_tienda.xlsx")         

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
      df_toexcel = df_toexcel[['producto','year','sales']].sort_values(["producto","year"])
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","year":"año"}),"resultados_por_año_producto.xlsx")       
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
      df_toexcel = df_toexcel.sort_values(["tienda","producto","year"])
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","year":"año"}),"resultados_por_año_tienda_producto.xlsx")       

   ax.legend()
   ax.grid(True) 
   st.pyplot(fig)

