import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from typing import List
from core import FinanceManager

class Graphs:
    def __init__(self, manager:FinanceManager):
        self.manager = manager

    def categories_expenses_graphic(self) -> None:
        expenses = self.manager.categories_expenses()
        df = pd.DataFrame(list(expenses.items()), columns=['Category', 'Amount'])
        self.plot_graph('pie', df['Amount'], labels=df['Category'], title='Gastos por Categoría')

    def monthly_expenses_graphic(self, year:str, month:str) -> None:
        try:
            year = int(year) if year else pd.Timestamp.now().year
            month = int(month) if month else pd.Timestamp.now().month
        except ValueError:
            print("Año y mes deben ser números enteros.")
            return

        expenses = self.manager.historial_expenses()
        df = pd.DataFrame([{'Date': t.date, 'Amount': t.amount} for t in expenses])
        df['Date'] = pd.to_datetime(df['Date'], format=self.manager.DATE_FORMAT)
        df.set_index('Date', inplace=True)

        df_monthly_expenses = df[(df.index.year == year) & (df.index.month == month)]
        if df_monthly_expenses.empty:
            print(f"\nNo hay gastos registrados para el mes {month} del año {year}.")
            return

        df_daily_expenses = df_monthly_expenses.resample('D').sum()
        self.plot_graph('bar', df_daily_expenses, title=f'Gastos diarios - {month:02d}-{year}', format='%d')

    def anual_expenses_graphic(self) -> None:
        expenses = self.manager.historial_expenses()
        if not expenses:
            print("No hay gastos registrados para mostrar en el gráfico.")
            return
        df = pd.DataFrame({'Date': t.date, 'Amount': t.amount} for t in expenses)
        df['Date'] = pd.to_datetime(df['Date'], format=self.manager.DATE_FORMAT)
        df.set_index('Date', inplace=True)
        df_anual_expenses = df.resample('YE').sum()
        self.plot_graph('bar', df_anual_expenses, title='Gastos Anuales', format='%Y')

    def save_graph(self, parent_file:str, filename:str) -> None:
        os.makedirs(parent_file, exist_ok=True)
        filename = os.path.basename(filename)
        ruta_imagen = os.path.join(parent_file, filename)
        plt.savefig(ruta_imagen)
        print(f"Gráfica guardada como: {ruta_imagen}")

    def plot_graph(self, graph_type:str, values:pd.DataFrame, title:str, labels:List[str]=None, format=None) -> None:
        if graph_type not in {'pie', 'bar'}:
            raise ValueError(f"Tipo de gráfico no soportado: {graph_type}")
        
        plt.figure(figsize=(6, 4))
        sns.set_theme(style="whitegrid")
        sns.set_palette("pastel")
    
        if graph_type == 'pie':
            plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.title(title)
        elif graph_type == 'bar':
            sns.set_context("talk")
            values['DateStr'] = values.index.strftime(format)
            sns.barplot(data=values, x='DateStr', y='Amount', color='skyblue')
            plt.xticks(rotation=0)
            plt.title(title)
            plt.xlabel("Fecha")
            plt.ylabel("Monto ($)")

        safe_title = title.replace('/', '-')
        self.save_graph("graficas", safe_title + '.png')
        plt.tight_layout()
        plt.show()
        ##Para Futuras Test###
        fig = plt.gcf()
        return fig