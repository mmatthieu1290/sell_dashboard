import streamlit as st
import matplotlib.pyplot as plt

def graph_daily(responses,df):

   por_tiendas = False
   por_tipo_de_productos = False
   fig, ax = plt.subplots() 
   ax.set_xlabel('Day in week', fontweight ='bold', fontsize = 15)
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
      df_day_month_year = df.groupby(["year","month","day"])["sales"].sum().to_frame().reset_index()
      df_day = df_day_month_year.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
      days = df_day.day.tolist()
      sales = df_day.sales.tolist() 
      ax.plot(days,sales)
      ax.set_xticks(ticks=days)
      for day,sale in zip(days,sales):
      
         ax.scatter(day,sale,c="blue")

   elif por_tipo_de_productos == False:
      for store in options_tiendas:
            nb_store = int(store.split(" ")[1])  
            df_store = df[df.store_nbr == nb_store]
            df_store_year_month_day = df_store.groupby(["year","month","day"])["sales"].sum().to_frame().reset_index()
            df_store_day = df_store_year_month_day.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
            days = df_store_day.day.tolist()
            sales = df_store_day.sales.tolist()            
            ax.plot(days,sales,label = str(store))
            for day,sale in zip(days,sales):
               ax.scatter(day,sale,c="blue")
            ax.set_xticks(ticks=days)   

   elif por_tiendas == False:
      for producto in options_productos:
            df_producto = df[df.family == producto]
            df_producto_year_month_day = df_producto.groupby(["year","month","day"])["sales"].sum().to_frame().reset_index()
            df_producto_day = df_producto_year_month_day.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
            days = df_producto_day.day.tolist()
            sales = df_producto_day.sales.tolist()            
            ax.plot(days,sales,label = producto)
            for day,sale in zip(days,sales):
               ax.scatter(day,sale,c="blue")
            ax.set_xticks(ticks=days)   
   else:
      for tienda_producto in options_tiendas_productos:
            tienda,producto = tienda_producto
            nb_tienda = int(tienda.split(" ")[1])
            df_tienda_producto = df[(df.family == producto)&(df.store_nbr == nb_tienda)]
            df_tienda_producto_year_month_day = df_tienda_producto.groupby(["year","month","day"])["sales"].sum().to_frame().reset_index()
            df_tienda_producto_day = df_tienda_producto_year_month_day.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
            days = df_tienda_producto_day.day.tolist()
            sales = df_tienda_producto_day.sales.tolist()            
            ax.plot(days,sales,label = tienda_producto)
            for day,sale in zip(days,sales):
               ax.scatter(day,sale,c="blue")
            ax.set_xticks(ticks=days)   
   ax.legend()
   ax.grid()
   st.pyplot(fig)    

def graph_daily_by_year(responses,df):

   por_tiendas = False
   por_tipo_de_productos = False
   fig, ax = plt.subplots() 
   ax.set_xlabel('Day in week', fontweight ='bold', fontsize = 15)
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
       
      df_year = df[df.year == year]

      if (por_tiendas == False) and (por_tipo_de_productos == False):
         df_day_month_year = df_year.groupby(["month","day"])["sales"].sum().to_frame().reset_index()
         df_day = df_day_month_year.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
         days = df_day.day.tolist()
         sales = df_day.sales.tolist() 
         ax.plot(days,sales,label=str(year))
         ax.set_xticks(ticks=days)
         for day,sale in zip(days,sales):
      
            ax.scatter(day,sale,c="blue")

      elif por_tipo_de_productos == False:
         for store in options_tiendas:
            nb_store = int(store.split(" ")[1])  
            df_store = df_year[df_year.store_nbr == nb_store]
            df_store_year_month_day = df_store.groupby(["month","day"])["sales"].sum().to_frame().reset_index()
            df_store_day = df_store_year_month_day.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
            days = df_store_day.day.tolist()
            sales = df_store_day.sales.tolist()            
            ax.plot(days,sales,label = str(store)+" "+str(year))
            for day,sale in zip(days,sales):
               ax.scatter(day,sale,c="blue")
            ax.set_xticks(ticks=days)   

      elif por_tiendas == False:
         for producto in options_productos:
            df_producto = df_year[df_year.family == producto]
            df_producto_year_month_day = df_producto.groupby(["month","day"])["sales"].sum().to_frame().reset_index()
            df_producto_day = df_producto_year_month_day.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
            days = df_producto_day.day.tolist()
            sales = df_producto_day.sales.tolist()            
            ax.plot(days,sales,label = producto+" "+str(year))
            for day,sale in zip(days,sales):
               ax.scatter(day,sale,c="blue")
            ax.set_xticks(ticks=days)   
      else:
         for tienda_producto in options_tiendas_productos:
            tienda,producto = tienda_producto
            nb_tienda = int(tienda.split(" ")[1])
            df_tienda_producto = df_year[(df_year.family == producto)&(df_year.store_nbr == nb_tienda)]
            df_tienda_producto_year_month_day = df_tienda_producto.groupby(["month","day"])["sales"].sum().to_frame().reset_index()
            df_tienda_producto_day = df_tienda_producto_year_month_day.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
            days = df_tienda_producto_day.day.tolist()
            sales = df_tienda_producto_day.sales.tolist()            
            ax.plot(days,sales,label = tienda_producto + " " + str(year))
            for day,sale in zip(days,sales):
               ax.scatter(day,sale,c="blue")
            ax.set_xticks(ticks=days)   
   ax.legend()
   ax.grid()
   st.pyplot(fig)    

def graph_daily_by_month(responses,df):

   dict_month = {1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",7:"Julio",8:"Agosto",9:"Septiembre",
                 10:"Octubre",11:"Noviembre",12:"Diciembre"}

   por_tiendas = False
   por_tipo_de_productos = False
   fig, ax = plt.subplots() 
   ax.set_xlabel('Day in week', fontweight ='bold', fontsize = 15)
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
   
   months = df.sort_values("month")["month"].unique()

   for month in months:
      month_name = dict_month[month] 
      df_month = df[df.month == month]

      if (por_tiendas == False) and (por_tipo_de_productos == False):
         df_day_month_year = df_month.groupby(["year","day"])["sales"].sum().to_frame().reset_index()
         df_day = df_day_month_year.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
         days = df_day.day.tolist()
         sales = df_day.sales.tolist() 
         ax.plot(days,sales,label=str(month_name))
         ax.set_xticks(ticks=days)
         for day,sale in zip(days,sales):
      
            ax.scatter(day,sale,c="blue")

      elif por_tipo_de_productos == False:
         for store in options_tiendas:
            nb_store = int(store.split(" ")[1])  
            df_store = df_month[df_month.store_nbr == nb_store]
            df_store_year_month_day = df_store.groupby(["year","day"])["sales"].sum().to_frame().reset_index()
            df_store_day = df_store_year_month_day.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
            days = df_store_day.day.tolist()
            sales = df_store_day.sales.tolist()            
            ax.plot(days,sales,label = str(store)+" "+str(month_name))
            for day,sale in zip(days,sales):
               ax.scatter(day,sale,c="blue")
            ax.set_xticks(ticks=days)   

      elif por_tiendas == False:
         for producto in options_productos:
            df_producto = df_month[df_month.family == producto]
            df_producto_year_month_day = df_producto.groupby(["year","day"])["sales"].sum().to_frame().reset_index()
            df_producto_day = df_producto_year_month_day.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
            days = df_producto_day.day.tolist()
            sales = df_producto_day.sales.tolist()            
            ax.plot(days,sales,label = producto+" "+str(month_name))
            for day,sale in zip(days,sales):
               ax.scatter(day,sale,c="blue")
            ax.set_xticks(ticks=days)   
      else:
         for tienda_producto in options_tiendas_productos:
            tienda,producto = tienda_producto
            nb_tienda = int(tienda.split(" ")[1])
            df_tienda_producto = df_month[(df_month.family == producto)&(df_month.store_nbr == nb_tienda)]
            df_tienda_producto_year_month_day = df_tienda_producto.groupby(["year","day"])["sales"].sum().to_frame().reset_index()
            df_tienda_producto_day = df_tienda_producto_year_month_day.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
            days = df_tienda_producto_day.day.tolist()
            sales = df_tienda_producto_day.sales.tolist()            
            ax.plot(days,sales,label = tienda_producto + " " + str(month_name))
            for day,sale in zip(days,sales):
               ax.scatter(day,sale,c="blue")
            ax.set_xticks(ticks=days)   
   ax.legend()
   ax.grid()
   st.pyplot(fig)       

def graph_daily_by_month_and_year(responses,df):

   dict_month = {1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",7:"Julio",8:"Agosto",9:"Septiembre",
                 10:"Octubre",11:"Noviembre",12:"Diciembre"}

   por_tiendas = False
   por_tipo_de_productos = False
   fig, ax = plt.subplots() 
   ax.set_xlabel('Day in week', fontweight ='bold', fontsize = 15)
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
   
   months = df.sort_values("month")["month"].unique()
   years = df.sort_values("year")["year"].unique()

   for year in years:
      for month in months:
         month_name = dict_month[month] 
         df_month_year = df[(df.month == month)&(df.year == year)]

         if (por_tiendas == False) and (por_tipo_de_productos == False):
            df_day = df_month_year.groupby("day")["sales"].sum().to_frame().reset_index().sort_values("day")
            days = df_day.day.tolist()
            sales = df_day.sales.tolist() 
            ax.plot(days,sales,label=str(month_name)+"-"+str(year))
            ax.set_xticks(ticks=days)
            for day,sale in zip(days,sales):
      
               ax.scatter(day,sale,c="blue")

         elif por_tipo_de_productos == False:
            for store in options_tiendas:
               nb_store = int(store.split(" ")[1])  
               df_store = df_month_year[df_month_year.store_nbr == nb_store]
               df_store_day = df_store.groupby("day")["sales"].sum().to_frame().reset_index().sort_values("day")
               days = df_store_day.day.tolist()
               sales = df_store_day.sales.tolist()            
               ax.plot(days,sales,label = str(store)+" "+str(month_name)+"-"+str(year))
               for day,sale in zip(days,sales):
                  ax.scatter(day,sale,c="blue")
               ax.set_xticks(ticks=days)   

         elif por_tiendas == False:
            for producto in options_productos:
               df_producto = df_month_year[df_month_year.family == producto]
               df_producto_day = df_producto.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
               days = df_producto_day.day.tolist()
               sales = df_producto_day.sales.tolist()            
               ax.plot(days,sales,label = producto+" "+str(month_name)+"-"+str(year))
               for day,sale in zip(days,sales):
                  ax.scatter(day,sale,c="blue")
               ax.set_xticks(ticks=days)   
         else:
            for tienda_producto in options_tiendas_productos:
               tienda,producto = tienda_producto
               nb_tienda = int(tienda.split(" ")[1])
               df_tienda_producto = df_month_year[(df_month.family == producto)&(df_month.store_nbr == nb_tienda)]
               df_tienda_producto_day = df_tienda_producto.groupby("day")["sales"].mean().to_frame().reset_index().sort_values("day")
               days = df_tienda_producto_day.day.tolist()
               sales = df_tienda_producto_day.sales.tolist()            
               ax.plot(days,sales,label = tienda_producto + " " + str(month_name)+"-"+str(year))
               for day,sale in zip(days,sales):
                  ax.scatter(day,sale,c="blue")
               ax.set_xticks(ticks=days)   
   ax.legend()
   ax.grid()
   st.pyplot(fig)          