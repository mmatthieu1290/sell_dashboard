import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from toExcel import downloadExcel



def graph_monthly(responses,df_years):
   dict_month = {1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",7:"Julio",8:"Agosto",9:"Septiembre",
                 10:"Octubre",11:"Noviembre",12:"Diciembre"}
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

      df_month["month"] = df_month["month"].replace(dict_month)
      downloadExcel(df_month.rename(columns = {"sales":"ventas","month":"mes"}),"resultados_por_mes.xlsx")
   elif por_tipo_de_productos == False:
      df_toexcel = pd.DataFrame(columns = ['month','sales','tienda'])
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
            df_store_month["tienda"] = store
            df_toexcel = pd.concat([df_toexcel,df_store_month])
      df_toexcel = df_toexcel[['tienda','month','sales']]
      df_toexcel = df_toexcel.sort_values(['tienda','month'])
      df_toexcel["month"] = df_toexcel["month"].replace(dict_month)
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","month":"mes"}),"resultados_por_mes_tienda.xlsx")         

   elif por_tiendas == False:
      df_toexcel = pd.DataFrame(columns = ['month','sales','producto'])
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
            df_producto_month["producto"] = producto
            df_toexcel = pd.concat([df_toexcel,df_producto_month])
      df_toexcel = df_toexcel[['producto','month','sales']]
      df_toexcel = df_toexcel.sort_values(['producto','month'])
      df_toexcel["month"] = df_toexcel["month"].replace(dict_month)
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","month":"mes"}),"resultados_por_mes_producto.xlsx")                    
   else:
      df_toexcel = pd.DataFrame(columns = ['month','sales','tienda','producto'])
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
            df_tienda_producto_month["tienda"] = tienda
            df_tienda_producto_month["producto"] = producto
            df_toexcel = pd.concat([df_toexcel,df_tienda_producto_month])
      df_toexcel = df_toexcel[['tienda','producto','month','sales']]
      df_toexcel = df_toexcel.sort_values(['tienda','producto','month'])
      df_toexcel["month"] = df_toexcel["month"].replace(dict_month)
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","month":"mes"}),"resultados_por_mes_tienda_producto.xlsx")         
   ax.legend()
   ax.grid()
   st.pyplot(fig)               

def graph_monthly_by_year(responses,df):

   dict_month = {1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",7:"Julio",8:"Agosto",9:"Septiembre",
                 10:"Octubre",11:"Noviembre",12:"Diciembre"}
   por_tiendas = False
   por_tipo_de_productos = False
   fig, ax = plt.subplots() 
   ax.set_xlabel('Month', fontweight ='bold', fontsize = 15)
   ax.set_ylabel('Total sales', fontweight ='bold', fontsize = 15)   
   if "tiendas" in responses:

       por_tiendas = True
       options_tiendas = responses["tiendas"]
       df_toexcel = pd.DataFrame(columns = ["month","sales","tienda","año"])
   elif "productos" in responses:
       por_tipo_de_productos = True 
       options_productos = responses["productos"]
       df_toexcel = pd.DataFrame(columns = ["month","sales","producto","año"])
   elif "tiendas_productos" in responses:
       por_tiendas = True            
       por_tipo_de_productos = True 
       options_tiendas_productos = responses["tiendas_productos"]
       df_toexcel = pd.DataFrame(columns = ["month","sales","tienda","producto","año"])
   else:
       df_toexcel = pd.DataFrame(columns = ["month","sales","año"])   

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
         df_month["año"] = year
         df_toexcel = pd.concat([df_toexcel,df_month])
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
            df_store_month["año"] = year
            df_store_month["tienda"] = store
            df_toexcel = pd.concat([df_toexcel,df_store_month])   

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
            df_producto_month["año"] = year
            df_producto_month["producto"] = producto
            df_toexcel = pd.concat([df_toexcel,df_producto_month])            
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
            df_tienda_producto_month["año"] = year
            df_tienda_producto_month["tienda"] = tienda
            df_tienda_producto_month["producto"] = producto
            df_toexcel = pd.concat([df_toexcel,df_tienda_producto_month])         
   if (por_tiendas == False) and (por_tipo_de_productos == False):
      df_toexcel = df_toexcel[["año","month","sales"]].sort_values(["año","month"])
      df_toexcel["month"] = df_toexcel["month"].replace(dict_month)
      df_toexcel["año"] = df_toexcel["año"].astype(int)
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","month":"mes"}),"resultados_por_mes_año_producto.xlsx")
   elif por_tipo_de_productos == False:
      df_toexcel = df_toexcel[["tienda","año","month","sales"]].sort_values(["tienda","año","month"])
      df_toexcel["month"] = df_toexcel["month"].replace(dict_month)
      df_toexcel["año"] = df_toexcel["año"].astype(int)
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","month":"mes"}),"resultados_por_tienda_mes_año_producto.xlsx")      
   elif por_tiendas == False:
      df_toexcel = df_toexcel[["producto","año","month","sales"]].sort_values(["producto","año","month"])
      df_toexcel["month"] = df_toexcel["month"].replace(dict_month)
      df_toexcel["año"] = df_toexcel["año"].astype(int)
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","month":"mes"}),"resultados_por_producto_mes_año_producto.xlsx")    
   else:
      df_toexcel = df_toexcel[["tienda","producto","año","month","sales"]].sort_values(["tienda","producto","año","month"])
      df_toexcel["month"] = df_toexcel["month"].replace(dict_month)
      df_toexcel["año"] = df_toexcel["año"].astype(int)
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","month":"mes"}),"resultados_por_tienda_producto_mes_año_producto.xlsx")    

   ax.legend()
   ax.grid()
   st.pyplot(fig)                  