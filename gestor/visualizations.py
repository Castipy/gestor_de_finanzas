import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from typing import List
from gestor.core import FinanceManager

class Graphs:

    ''' Clase para generar gráficos de gastos.
    Esta clase utiliza la biblioteca Seaborn para crear gráficos de gastos
    basados en las transacciones financieras almacenadas en la clase FinanceManager.
    
    Atributos:
        manager (FinanceManager): Instancia de la clase FinanceManager que contiene las transacciones.
    Métodos:
        expenses_graphics: Genera gráficos de gastos en diferentes formatos (barra, pastel, línea).
        save_graph: Guarda el gráfico generado en un archivo.
    '''
    DATE_FORMAT = '%d-%m-%Y %H:%M:%S'

    def __init__(self, manager:FinanceManager):
        self.manager = manager
        
    def expenses_graphics(self, df:pd.DataFrame, title:str, graph_type:str = 'bar')-> plt.Figure:
        '''Genera gráficos de gastos en diferentes formatos (barra, pastel, línea).'''
        #Tamaño de la figura#
        plt.figure(figsize=(len(df.columns)*2, len(df)*2))
        #Tema y paleta de colores#
        sns.set_theme(style="whitegrid")
        sns.set_palette("pastel")
        #Filtrando por el tipo de grafico#
        if graph_type == 'pie':
            plt.pie(df['Amount'], labels=df['Category'],autopct=lambda p: '{:.0f}'.format(p * df['Amount'].sum() / 100), startangle=140)
            plt.title(title)
        elif graph_type == 'lineplot':
            #Suma los valores de todas las columnas por filas#
            df['Total'] = df.iloc[:, 1:].sum(axis=1)
            #Asignando los días (columns[0]='Date') como el índice del DF#
            df = df.set_index(df.columns[0])
            #Reindexando para obtener todos los dias y los vacios se rellenan con 0#
            df = df.reindex(range(1,32), fill_value=0)
            #Se resetea el indice para que se convierta a columna#
            df.reset_index(inplace=True)
            #Renombrando la columna que era el indice(index el cual reseteamos) a Date#
            df.rename(columns={df.columns[0]:'Date'}, inplace=True)
            sns.lineplot(data=df, x='Date', y='Total')
            plt.xticks(range(1,32,1))
            plt.xlabel("Día")
            plt.ylabel("Monto ($)")
            plt.title(title)
        else:
            df = df.reset_index()
            sns.barplot(data=df, x=df.columns[1], y='Amount', color='skyblue')
            #Obtenemos el valor maximo del eje Y#
            max_y = plt.gca().get_ylim()[1]
            #Forzamos a que los valores en Y tengan una distancia de 200u#
            plt.yticks(range(0, int(max_y) + 10, int(max_y / 10)))
            plt.xticks(rotation=0)
            plt.title(title)
            plt.xlabel("Fecha")
            plt.ylabel("Monto ($)")

        fig = plt.gcf()
        safe_title = title.replace('/', '-')
        self.save_graph(safe_title + '.png') 
        plt.tight_layout()
        plt.show()
        plt.close(fig)  # Libera memoria si se generan muchas figuras
        return fig    

    def save_graph(self, filename:str) -> None:
        '''Guarda el gráfico generado en un archivo.'''
        os.makedirs('static', exist_ok=True)
        filename = os.path.basename(filename)
        ruta_imagen = os.path.join('static', filename)
        plt.savefig(ruta_imagen)
        print(f"Gráfica guardada como: {ruta_imagen}")