import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from toExcel import downloadExcel



def graph_monthly(responses,df_years):
   dict_month = {1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",7:"Julio",8:"Agosto",9:"Septiembre",
                 10:"Octubre",11:"Noviembre",12:"Diciembre"}
   por_tiendas = False
   por_tipo_de_productos = False 
   if "tiendas" in responses:

       por_tiendas = True
       options_tiendas = responses["tiendas"]
       numeros_tiendas = [int(store.split(" ")[1]) for store in options_tiendas]
       numeros_tiendas.sort()
       options_tiendas = ["Tienda" + " " + str(numero_tienda) for numero_tienda in numeros_tiendas]       
   elif "productos" in responses:
       por_tipo_de_productos = True 
       options_productos = responses["productos"]
       options_productos.sort()
   elif "tiendas_productos" in responses:
       por_tiendas = True            
       por_tipo_de_productos = True 
       options_tiendas_productos = responses["tiendas_productos"]
       options_tiendas_productos_num = [(int(elt[0].split(" ")[1]),elt[1]) for elt in options_tiendas_productos]
       options_tiendas_productos_num.sort()
       options_tiendas_productos = [("Tienda " + str(elt[0]),elt[1]) for elt in options_tiendas_productos_num]           

   if (por_tiendas == False) and (por_tipo_de_productos == False):
      fig = go.Figure()
      df_month_year = df_years.groupby(["year","month"])["sales"].sum().to_frame().reset_index().sort_values("month")
      df_month = df_month_year.groupby("month")["sales"].mean().to_frame().reset_index().sort_values("month")
      months = df_month.month.tolist()
      sales = df_month.sales.tolist() 
      fig.add_trace(go.Scatter(x=months,y=sales,mode = "lines+markers",marker=dict(size=8)))
      df_month["month"] = df_month["month"].replace(dict_month)
      downloadExcel(df_month.rename(columns = {"sales":"ventas","month":"mes"}),"resultados_por_mes.xlsx")
   elif por_tipo_de_productos == False:
      months = df_years.month.tolist()
      df_toexcel = pd.DataFrame(columns = ['month','sales','tienda'])
      fig = go.Figure()
      for store in options_tiendas:
            nb_store = int(store.split(" ")[1])  
            df_store = df_years[df_years.store_nbr == nb_store]
            df_store_year_month = df_store.groupby(["year","month"])["sales"].sum().to_frame().reset_index().sort_values("month")
            df_store_month = df_store_year_month.groupby("month")["sales"].mean().to_frame().reset_index().sort_values("month")
            sales = df_store_month.sales.tolist() 
            months = df_store_month.month.tolist()           
            fig.add_trace(go.Scatter(x=months,y=sales,name=str(store),mode = "lines+markers",marker=dict(size=8)))
            df_store_month["tienda"] = store
            df_toexcel = pd.concat([df_toexcel,df_store_month])
      df_toexcel = df_toexcel[['tienda','month','sales']]
      df_toexcel = df_toexcel.sort_values(['tienda','month'])
      df_toexcel["month"] = df_toexcel["month"].replace(dict_month)
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","month":"mes"}),"resultados_por_mes_tienda.xlsx")         

   elif por_tiendas == False:
      df_toexcel = pd.DataFrame(columns = ['month','sales','producto'])
      fig = go.Figure()
      months = df_years.month.tolist()
      for producto in options_productos:
            df_producto = df_years[df_years.family == producto]
            df_producto_year_month = df_producto.groupby(["year","month"])["sales"].sum().to_frame().reset_index().sort_values("month")
            df_producto_month = df_producto_year_month.groupby("month")["sales"].mean().to_frame().reset_index().sort_values("month")
            months = df_producto_month.month.tolist()
            sales = df_producto_month.sales.tolist()            
            fig.add_trace(go.Scatter(x=months,y=sales,name=str(producto),mode = "lines+markers",marker=dict(size=8)))
            df_producto_month["producto"] = producto
            df_toexcel = pd.concat([df_toexcel,df_producto_month])
      df_toexcel = df_toexcel[['producto','month','sales']]
      df_toexcel = df_toexcel.sort_values(['producto','month'])
      df_toexcel["month"] = df_toexcel["month"].replace(dict_month)
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","month":"mes"}),"resultados_por_mes_producto.xlsx")                    
   else:
      df_toexcel = pd.DataFrame(columns = ['month','sales','tienda','producto'])
      fig = go.Figure()
      months = df_years.month.tolist()      
      for tienda_producto in options_tiendas_productos:
            tienda,producto = tienda_producto
            nb_tienda = int(tienda.split(" ")[1])
            df_tienda_producto = df_years[(df_years.family == producto)&(df_years.store_nbr == nb_tienda)]
            df_tienda_producto_year_month = df_tienda_producto.groupby(["year","month"])["sales"].sum().to_frame().reset_index().sort_values("month")
            df_tienda_producto_month = df_tienda_producto_year_month.groupby("month")["sales"].mean().to_frame().reset_index().sort_values("month")
            months = df_tienda_producto_month.month.tolist()
            sales = df_tienda_producto_month.sales.tolist()            
            df_tienda_producto_month["tienda"] = tienda
            df_tienda_producto_month["producto"] = producto
            df_toexcel = pd.concat([df_toexcel,df_tienda_producto_month])
            fig.add_trace(go.Scatter(x=months,y=sales,name=tienda + " " +str(producto) ,mode = "lines+markers",marker=dict(size=8)))
      df_toexcel = df_toexcel[['tienda','producto','month','sales']]
      df_toexcel = df_toexcel.sort_values(['tienda','producto','month'])
      df_toexcel["month"] = df_toexcel["month"].replace(dict_month)
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","month":"mes"}),"resultados_por_mes_tienda_producto.xlsx") 
   fig.update_xaxes(title_text = "mes",title_font = {"size": 20},
        title_standoff = 25,ticktext=months,tickvals=months,)
   fig.update_yaxes(title_text = "ventas",title_font = {"size": 20},
        title_standoff = 25)
   st.plotly_chart(fig, config = {'scrollZoom': False})                           

def graph_monthly_by_year(responses,df):

   dict_month = {1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",7:"Julio",8:"Agosto",9:"Septiembre",
                 10:"Octubre",11:"Noviembre",12:"Diciembre"}
   por_tiendas = False
   por_tipo_de_productos = False 
   if "tiendas" in responses:

       por_tiendas = True
       options_tiendas = responses["tiendas"]
       numeros_tiendas = [int(store.split(" ")[1]) for store in options_tiendas]
       numeros_tiendas.sort()
       options_tiendas = ["Tienda" + " " + str(numero_tienda) for numero_tienda in numeros_tiendas]           
       df_toexcel = pd.DataFrame(columns = ["month","sales","tienda","año"])
   elif "productos" in responses:
       por_tipo_de_productos = True 
       options_productos = responses["productos"]
       options_productos.sort()
       df_toexcel = pd.DataFrame(columns = ["month","sales","producto","año"])
   elif "tiendas_productos" in responses:
       por_tiendas = True            
       por_tipo_de_productos = True 
       options_tiendas_productos = responses["tiendas_productos"]
       options_tiendas_productos_num = [(int(elt[0].split(" ")[1]),elt[1]) for elt in options_tiendas_productos]
       options_tiendas_productos_num.sort()
       options_tiendas_productos = [("Tienda " + str(elt[0]),elt[1]) for elt in options_tiendas_productos_num]       
       df_toexcel = pd.DataFrame(columns = ["month","sales","tienda","producto","año"])
   else:
       df_toexcel = pd.DataFrame(columns = ["month","sales","año"])   

   years = df.sort_values("year")["year"].unique()
   months = df.sort_values("month")["month"].unique()   


   
   if (por_tiendas == False) and (por_tipo_de_productos == False):
      fig = go.Figure()
      for year in years:
         df_years = df[df.year == year]   
         df_month = df_years.groupby("month")["sales"].sum().to_frame().reset_index().sort_values("month")
         months = df_month.month.tolist()
         sales = df_month.sales.tolist() 
         fig.add_trace(go.Scatter(x=months,y=sales,name=str(year),mode = "lines+markers",marker=dict(size=8))) 
         df_month["año"] = year
         df_toexcel = pd.concat([df_toexcel,df_month])
   elif por_tipo_de_productos == False:
      fig = go.Figure()
      for store in options_tiendas:
         for year in years:
            df_years = df[df.year == year]   
            nb_store = int(store.split(" ")[1])  
            df_store = df_years[df_years.store_nbr == nb_store]
            df_store_month = df_store.groupby("month")["sales"].sum().to_frame().reset_index().sort_values("month")
            months = df_store_month.month.tolist()
            sales = df_store_month.sales.tolist()           
            fig.add_trace(go.Scatter(x=months,y=sales,name=str(store)+ " " +str(year),mode = "lines+markers",marker=dict(size=8))) 
            df_store_month["año"] = year
            df_store_month["tienda"] = store
            df_toexcel = pd.concat([df_toexcel,df_store_month])   

   elif por_tiendas == False:
      fig = go.Figure()
      for producto in options_productos:
         for year in years:
            df_years = df[df.year == year]      
            df_producto = df_years[df_years.family == producto]
            df_producto_month = df_producto.groupby("month")["sales"].sum().to_frame().reset_index().sort_values("month")
            months = df_producto_month.month.tolist()
            sales = df_producto_month.sales.tolist()    
            fig.add_trace(go.Scatter(x=months,y=sales,name=producto+ " " +str(year),mode = "lines+markers",marker=dict(size=8)))        
            df_producto_month["año"] = year
            df_producto_month["producto"] = producto
            df_toexcel = pd.concat([df_toexcel,df_producto_month])            
   else:
      fig = go.Figure()
      for tienda_producto in options_tiendas_productos:
         for year in years:
            df_years = df[df.year == year]      
            tienda,producto = tienda_producto
            nb_tienda = int(tienda.split(" ")[1])
            df_tienda_producto = df_years[(df_years.family == producto)&(df_years.store_nbr == nb_tienda)]
            df_tienda_producto_month = df_tienda_producto.groupby("month")["sales"].sum().to_frame().reset_index().sort_values("month")
            months = df_tienda_producto_month.month.tolist()
            sales = df_tienda_producto_month.sales.tolist()
            fig.add_trace(go.Scatter(x=months,y=sales,name=tienda + " " +str(producto)+ " "+str(year),mode = "lines+markers",marker=dict(size=8)))            
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

   fig.update_xaxes(title_text = "mes",title_font = {"size": 20},
        title_standoff = 25,ticktext=months,tickvals=months,)
   fig.update_yaxes(title_text = "ventas",title_font = {"size": 20},
        title_standoff = 25)
   st.plotly_chart(fig, config = {'scrollZoom': False})               