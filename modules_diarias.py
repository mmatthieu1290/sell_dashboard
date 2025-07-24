import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from toExcel import downloadExcel

def graph_daily(responses,df):

   dict_dias = {1 : "Lunes", 2 : "Martes" , 3 : "Miercoles" , 4 : "Jueves" , 5 : "Viernes" , 6 : "Sabado" , 7 : "Domingo"}
   por_tiendas = False
   por_tipo_de_productos = False
   fig, ax = plt.subplots() 
   ax.set_xlabel('Day in week', fontweight ='bold', fontsize = 15)
   ax.set_ylabel('Total sales', fontweight ='bold', fontsize = 15)   
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
      df_day_month_year = df.groupby(["year","month","day"])["sales"].sum().to_frame().reset_index()
      df_day = df_day_month_year.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
      days = df_day.day.tolist()
      sales = df_day.sales.tolist() 
      ax.plot(days,sales)
      ax.set_xticks(ticks=days)
      fig.add_trace(go.Scatter(x=days,y=sales,mode = "lines+markers",marker=dict(size=8)))
      df_day["day"] = df_day["day"].replace(dict_dias)
      downloadExcel(df_day.rename(columns = {"sales":"ventas","day":"dia"}),"resultados_por_dia.xlsx")    

   elif por_tipo_de_productos == False:
      days = df.day.tolist()
      df_toexcel = pd.DataFrame(columns = ['day','sales','tienda'])
      fig = go.Figure()
      for store in options_tiendas:
            nb_store = int(store.split(" ")[1])  
            df_store = df[df.store_nbr == nb_store]
            df_store_year_month_day = df_store.groupby(["year","month","day"])["sales"].sum().to_frame().reset_index()
            df_store_day = df_store_year_month_day.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
            days = df_store_day.day.tolist()
            sales = df_store_day.sales.tolist()            
            ax.plot(days,sales,label = str(store))
            fig.add_trace(go.Scatter(x=days,y=sales,name=str(store),mode = "lines+markers",marker=dict(size=8)))
            df_store_day["tienda"] = store
            df_toexcel = pd.concat([df_toexcel,df_store_day])
      df_toexcel = df_toexcel[['tienda','day','sales']]
      df_toexcel = df_toexcel.sort_values(['tienda','day'])
      df_toexcel["day"] = df_toexcel["day"].replace(dict_dias)
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","day":"dia"}),"resultados_por_dia_tienda.xlsx")              


   elif por_tiendas == False:
      days = df.day.tolist()
      df_toexcel = pd.DataFrame(columns = ['day','sales','producto'])
      fig = go.Figure()
      for producto in options_productos:
            df_producto = df[df.family == producto]
            df_producto_year_month_day = df_producto.groupby(["year","month","day"])["sales"].sum().to_frame().reset_index()
            df_producto_day = df_producto_year_month_day.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
            days = df_producto_day.day.tolist()
            sales = df_producto_day.sales.tolist()
            fig.add_trace(go.Scatter(x=days,y=sales,name=str(producto),mode = "lines+markers",marker=dict(size=8)))            
            df_producto_day["producto"] = producto
            df_toexcel = pd.concat([df_toexcel, df_producto_day])
      df_toexcel = df_toexcel[['producto','day','sales']]
      df_toexcel = df_toexcel.sort_values(['producto','day'])
      df_toexcel["day"] = df_toexcel["day"].replace(dict_dias)
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","day":"dia"}),"resultados_por_dia_producto.xlsx")                
   else:
      days = df.day.tolist()
      df_toexcel = pd.DataFrame(columns = ['day','sales','tienda','producto'])
      fig = go.Figure()
      for tienda_producto in options_tiendas_productos:
            tienda,producto = tienda_producto
            nb_tienda = int(tienda.split(" ")[1])
            df_tienda_producto = df[(df.family == producto)&(df.store_nbr == nb_tienda)]
            df_tienda_producto_year_month_day = df_tienda_producto.groupby(["year","month","day"])["sales"].sum().to_frame().reset_index()
            df_tienda_producto_day = df_tienda_producto_year_month_day.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
            days = df_tienda_producto_day.day.tolist()
            sales = df_tienda_producto_day.sales.tolist()            
            fig.add_trace(go.Scatter(x=days,y=sales,name=tienda + " " +str(producto) ,mode = "lines+markers",marker=dict(size=8)))
            df_tienda_producto_day["tienda"] = tienda
            df_tienda_producto_day["producto"] = producto
            df_toexcel = pd.concat([df_toexcel,df_tienda_producto_day])
      df_toexcel = df_toexcel[['tienda','producto','day','sales']]
      df_toexcel = df_toexcel.sort_values(['tienda','producto','day'])
      df_toexcel["day"] = df_toexcel["day"].replace(dict_dias)
      downloadExcel(df_toexcel.rename(columns = {"sales":"ventas","day":"dia"}),"resultados_por_dia_tienda_producto.xlsx")                  
   fig.update_xaxes(title_text = "dia", title_font = {"size": 20}, title_standoff = 25, ticktext=days, tickvals=days,)
   fig.update_yaxes(title_text = "ventas", title_font = {"size": 20}, title_standoff = 25)
   st.plotly_chart(fig, config = {'scrollZoom': False})        

def graph_daily_by_year(responses,df):

   por_tiendas = False
   por_tipo_de_productos = False
   fig, ax = plt.subplots() 
   ax.set_xlabel('Day in week', fontweight ='bold', fontsize = 15)
   ax.set_ylabel('Total sales', fontweight ='bold', fontsize = 15)   
   if "tiendas" in responses:

       por_tiendas = True
       options_tiendas = responses["tiendas"]
       numeros_tiendas = [int(store.split(" ")[1]) for store in options_tiendas]
       numeros_tiendas.sort()
       options_tiendas = ["Tienda" + " " + str(numero_tienda) for numero_tienda in numeros_tiendas]           
       df_toexcel = pd.DataFrame(columns = ["day","sales","tienda","año"])
   elif "productos" in responses:
       por_tipo_de_productos = True 
       options_productos = responses["productos"]
       options_productos.sort()
       df_toexcel = pd.DataFrame(columns = ["day","sales","producto","año"])
   elif "tiendas_productos" in responses:
       por_tiendas = True            
       por_tipo_de_productos = True 
       options_tiendas_productos = responses["tiendas_productos"]
       options_tiendas_productos_num = [(int(elt[0].split(" ")[1]),elt[1]) for elt in options_tiendas_productos]
       options_tiendas_productos_num.sort()
       options_tiendas_productos = [("Tienda " + str(elt[0]),elt[1]) for elt in options_tiendas_productos_num]       
       df_toexcel = pd.DataFrame(columns = ["day","sales","tienda","producto","año"])
   else:
       df_toexcel = pd.DataFrame(columns = ["day","sales","año"])     
   
   years = df.sort_values("year")["year"].unique()
   days = df.sort_values("day")["day"].unique()    


   if (por_tiendas == False) and (por_tipo_de_productos == False):
      fig = go.Figure()
      for year in years:
         df_year = df[df.year == year]         
         df_day_month_year = df_year.groupby(["month","day"])["sales"].sum().to_frame().reset_index()
         df_day = df_day_month_year.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
         days = df_day.day.tolist()
         sales = df_day.sales.tolist() 
         fig.add_trace(go.Scatter(x=days,y=sales,name=str(year),mode = "lines+markers",marker=dict(size=8))) 

   elif por_tipo_de_productos == False:
      fig = go.Figure()
      for year in years:
         df_year = df[df.year == year]         
         for store in options_tiendas:
            nb_store = int(store.split(" ")[1])  
            df_store = df_year[df_year.store_nbr == nb_store]
            df_store_year_month_day = df_store.groupby(["month","day"])["sales"].sum().to_frame().reset_index()
            df_store_day = df_store_year_month_day.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
            days = df_store_day.day.tolist()
            sales = df_store_day.sales.tolist()            
            fig.add_trace(go.Scatter(x=days,y=sales,name=str(store)+ " " +str(year),mode = "lines+markers",marker=dict(size=8))) 

   elif por_tiendas == False:
      fig = go.Figure()
      for year in years:
         df_year = df[df.year == year]      
         for producto in options_productos:
            df_producto = df_year[df_year.family == producto]
            df_producto_year_month_day = df_producto.groupby(["month","day"])["sales"].sum().to_frame().reset_index()
            df_producto_day = df_producto_year_month_day.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
            days = df_producto_day.day.tolist()
            sales = df_producto_day.sales.tolist()            
            fig.add_trace(go.Scatter(x=days,y=sales,name=producto+ " " +str(year),mode = "lines+markers",marker=dict(size=8)))   
   else:
      fig = go.Figure()
      for year in years:
         df_year = df[df.year == year]      
         for tienda_producto in options_tiendas_productos:
            tienda,producto = tienda_producto
            nb_tienda = int(tienda.split(" ")[1])
            df_tienda_producto = df_year[(df_year.family == producto)&(df_year.store_nbr == nb_tienda)]
            df_tienda_producto_year_month_day = df_tienda_producto.groupby(["month","day"])["sales"].sum().to_frame().reset_index()
            df_tienda_producto_day = df_tienda_producto_year_month_day.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
            days = df_tienda_producto_day.day.tolist()
            sales = df_tienda_producto_day.sales.tolist()            
            fig.add_trace(go.Scatter(x=days,y=sales,name=tienda + " " +str(producto)+ " "+str(year),mode = "lines+markers",marker=dict(size=8)))
   fig.update_xaxes(title_text = "dia",title_font = {"size": 20},title_standoff = 25,ticktext=days,tickvals=days,)
   fig.update_yaxes(title_text = "ventas",title_font = {"size": 20},
        title_standoff = 25)
   st.plotly_chart(fig, config = {'scrollZoom': False})  

def graph_daily_by_month(responses,df):

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
       df_toexcel = pd.DataFrame(columns = ["day","sales","tienda","año"])
   elif "productos" in responses:
       por_tipo_de_productos = True 
       options_productos = responses["productos"]
       options_productos.sort()
       df_toexcel = pd.DataFrame(columns = ["day","sales","producto","año"])
   elif "tiendas_productos" in responses:
       por_tiendas = True            
       por_tipo_de_productos = True 
       options_tiendas_productos = responses["tiendas_productos"]
       options_tiendas_productos_num = [(int(elt[0].split(" ")[1]),elt[1]) for elt in options_tiendas_productos]
       options_tiendas_productos_num.sort()
       options_tiendas_productos = [("Tienda " + str(elt[0]),elt[1]) for elt in options_tiendas_productos_num]       
       df_toexcel = pd.DataFrame(columns = ["day","sales","tienda","producto","año"])
   else:
       df_toexcel = pd.DataFrame(columns = ["day","sales","año"])      
   
   months = df.sort_values("month")["month"].unique()
   days = df.sort_values("day")["day"].unique()



   if (por_tiendas == False) and (por_tipo_de_productos == False):
      fig = go.Figure()
      for month in months:
         month_name = dict_month[month] 
         df_month = df[df.month == month]         
         df_day_month_year = df_month.groupby(["year","day"])["sales"].sum().to_frame().reset_index()
         df_day = df_day_month_year.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
         days = df_day.day.tolist()
         sales = df_day.sales.tolist() 
         fig.add_trace(go.Scatter(x=days,y=sales,name=str(month_name),mode = "lines+markers",marker=dict(size=8)))

   elif por_tipo_de_productos == False:
      fig = go.Figure()
      for month in months:
         month_name = dict_month[month] 
         df_month = df[df.month == month]      
         for store in options_tiendas:
            nb_store = int(store.split(" ")[1])  
            df_store = df_month[df_month.store_nbr == nb_store]
            df_store_year_month_day = df_store.groupby(["year","day"])["sales"].sum().to_frame().reset_index()
            df_store_day = df_store_year_month_day.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
            days = df_store_day.day.tolist()
            sales = df_store_day.sales.tolist()       
            fig.add_trace(go.Scatter(x=days,y=sales,name=str(store)+" "+str(month_name),mode = "lines+markers",marker=dict(size=8)))     

   elif por_tiendas == False:
      fig = go.Figure()
      for month in months:
         month_name = dict_month[month] 
         df_month = df[df.month == month]      
         for producto in options_productos:
            df_producto = df_month[df_month.family == producto]
            df_producto_year_month_day = df_producto.groupby(["year","day"])["sales"].sum().to_frame().reset_index()
            df_producto_day = df_producto_year_month_day.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
            days = df_producto_day.day.tolist()
            sales = df_producto_day.sales.tolist() 
            fig.add_trace(go.Scatter(x=days,y=sales,name=producto+" "+str(month_name),mode = "lines+markers",marker=dict(size=8)))            
   else:
      fig = go.Figure()
      for month in months:
         month_name = dict_month[month] 
         df_month = df[df.month == month]   
         for tienda_producto in options_tiendas_productos:
            tienda,producto = tienda_producto
            nb_tienda = int(tienda.split(" ")[1])
            df_tienda_producto = df_month[(df_month.family == producto)&(df_month.store_nbr == nb_tienda)]
            df_tienda_producto_year_month_day = df_tienda_producto.groupby(["year","day"])["sales"].sum().to_frame().reset_index()
            df_tienda_producto_day = df_tienda_producto_year_month_day.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
            days = df_tienda_producto_day.day.tolist()
            sales = df_tienda_producto_day.sales.tolist() 
            fig.add_trace(go.Scatter(x=days,y=sales,name=tienda_producto + " " + str(month_name),mode = "lines+markers",marker=dict(size=8)))           
   fig.update_xaxes(title_text = "dia",title_font = {"size": 20},title_standoff = 25,ticktext=days,tickvals=days,)
   fig.update_yaxes(title_text = "ventas",title_font = {"size": 20},title_standoff = 25)
   st.plotly_chart(fig, config = {'scrollZoom': False})     

def graph_daily_by_month_and_year(responses,df):

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
       df_toexcel = pd.DataFrame(columns = ["day","sales","tienda","año"])
   elif "productos" in responses:
       por_tipo_de_productos = True 
       options_productos = responses["productos"]
       options_productos.sort()
       df_toexcel = pd.DataFrame(columns = ["day","sales","producto","año"])
   elif "tiendas_productos" in responses:
       por_tiendas = True            
       por_tipo_de_productos = True 
       options_tiendas_productos = responses["tiendas_productos"]
       options_tiendas_productos_num = [(int(elt[0].split(" ")[1]),elt[1]) for elt in options_tiendas_productos]
       options_tiendas_productos_num.sort()
       options_tiendas_productos = [("Tienda " + str(elt[0]),elt[1]) for elt in options_tiendas_productos_num]       
       df_toexcel = pd.DataFrame(columns = ["day","sales","tienda","producto","año"])
   else:
       df_toexcel = pd.DataFrame(columns = ["day","sales","año"])    
   
   months = df.sort_values("month")["month"].unique()
   years = df.sort_values("year")["year"].unique()
   days = df.sort_values("day")["day"].unique()



   if (por_tiendas == False) and (por_tipo_de_productos == False):
      fig = go.Figure()
      for year in years:
         for month in months:
            month_name = dict_month[month] 
            df_month_year = df[(df.month == month)&(df.year == year)]         
            df_day = df_month_year.groupby("day")["sales"].sum().to_frame().reset_index().sort_values("day")
            days = df_day.day.tolist()
            sales = df_day.sales.tolist()
            fig.add_trace(go.Scatter(x=days,y=sales,name=str(month_name)+"-"+str(year),mode = "lines+markers",marker=dict(size=8))) 

   elif por_tipo_de_productos == False:
      fig = go.Figure()
      for year in years:
         for month in months:
            month_name = dict_month[month] 
            df_month_year = df[(df.month == month)&(df.year == year)]         
            for store in options_tiendas:
               nb_store = int(store.split(" ")[1])  
               df_store = df_month_year[df_month_year.store_nbr == nb_store]
               df_store_day = df_store.groupby("day")["sales"].sum().to_frame().reset_index().sort_values("day")
               days = df_store_day.day.tolist()
               sales = df_store_day.sales.tolist()
               fig.add_trace(go.Scatter(x=days,y=sales,name=str(store)+" "+str(month_name)+"-"+str(year),mode = "lines+markers",marker=dict(size=8)))              

   elif por_tiendas == False:
      fig = go.Figure()
      for year in years:
         for month in months:
            month_name = dict_month[month] 
            df_month_year = df[(df.month == month)&(df.year == year)]         
            for producto in options_productos:
               df_producto = df_month_year[df_month_year.family == producto]
               df_producto_day = df_producto.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
               days = df_producto_day.day.tolist()
               sales = df_producto_day.sales.tolist() 
               fig.add_trace(go.Scatter(x=days,y=sales,name=producto+" "+str(month_name)+"-"+str(year),\
                                        mode = "lines+markers",marker=dict(size=8)))           
   else:
      fig = go.Figure()
      for year in years:
         for month in months:
            month_name = dict_month[month] 
            df_month_year = df[(df.month == month)&(df.year == year)]         
            for tienda_producto in options_tiendas_productos:
               tienda,producto = tienda_producto
               nb_tienda = int(tienda.split(" ")[1])
               df_tienda_producto = df_month_year[(df_month_year.family == producto)&(df_month_year.store_nbr == nb_tienda)]
               df_tienda_producto_day = df_tienda_producto.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
               days = df_tienda_producto_day.day.tolist()
               sales = df_tienda_producto_day.sales.tolist()
               fig.add_trace(go.Scatter(x=days,y=sales,name=tienda +" " +producto + " " + str(month_name)+"-"+str(year),\
                                        mode = "lines+markers",marker=dict(size=8)))              
   fig.update_xaxes(title_text = "dia",title_font = {"size": 20},title_standoff = 25,ticktext=days,tickvals=days,)
   fig.update_yaxes(title_text = "ventas",title_font = {"size": 20},title_standoff = 25)
   st.plotly_chart(fig, config = {'scrollZoom': False})            