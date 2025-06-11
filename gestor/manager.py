import csv
from transactions import Transactions
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

class FinanceManager:
    def __init__(self):
        self.transactions_list = []
    
    def load_csv(self, filename): ##funcion para cargar csv##
        try:
            with open(filename, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        t = Transactions(
                            row['Type'],
                            float(row['Amount']),
                            row['Category'],
                            row['Description'],
                            row['Date/Time']
                        )
                        self.transactions_list.append(t)
                    except (KeyError, ValueError) as e:
                        print(f"Warning: Skipping invalid row {row}. Error: {e}")
        except FileNotFoundError:
            pass

    def save_csv(self, filename): ##funcion para guardar en csv##
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Type', 'Amount', 'Category', 'Description', 'Date/Time'])
            for t in self.transactions_list:
                writer.writerow([t.type, t.amount, t.category, t.description, t.date])        

    def add_transaction(self, transaction): ##añadir transaccion##
        self.transactions_list.append(transaction)

    def total_balance(self): ##funcion para calcular balance total##
        total = 0
        for t in self.transactions_list:
            if t.type == 'income':
                total += t.amount
            else:
                total -= t.amount
        return total    
    
    def categories_expenses(self): ##funcion para calcular gastos por categoria##
        categories = {}
        for t in self.transactions_list:
            if t.type == 'expense':
                categories[t.category] = categories.get(t.category, 0) + t.amount
        return categories
    
    def categories_expenses_graphic(self): #funcion para crear gráfico de pastel##
        expenses = self.categories_expenses()
        df = pd.DataFrame(list(expenses.items()), columns=['Category', 'Amount'])
         #Ajustar elemntos para que no se superpongan#
        self.plot_graph('pie',df['Amount'],labels=df['Category'], title='Gastos por Categoría')

    def monthly_expenses_graphic(self, year, month): ##funcion para crear gráfico de gastos mensuales##
        try:    
            year = int(year) if year else pd.Timestamp.now().year
            month = int(month) if month else pd.Timestamp.now().month
        except ValueError:
            print("Año y mes deben ser números enteros.")
            return
        
        expenses = self.historial_expenses()
        df = pd.DataFrame([{'Date': t.date,'Amount': t.amount,} for t in expenses])
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y %H:%M:%S')
        df.set_index('Date', inplace=True)

        # Filtrar Gastos por año y mes#
        df_monthly_expenses = df[(df.index.year == year) & (df.index.month == month)]
        if df_monthly_expenses.empty:
            print(f"\nNo hay gastos registrados para el mes {month} del año {year}.")
            return
          
        #Filtrar Gastos diarios del mes especificado#
        df_daily_expenses = df_monthly_expenses.resample('D').sum()
        
        self.plot_graph('bar',df_daily_expenses,title=f'Gastos diarios - {month:02d}/{year}',format='%d')

    def anual_expenses_graphic(self):
        expenses = self.historial_expenses()
        if not expenses:
            print("No hay gastos registrados para mostrar en el gráfico.")
            return
        df = pd.DataFrame({'Date':t.date, 'Amount':t.amount} for t in expenses)
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y %H:%M:%S')
        df.set_index('Date', inplace=True)
        df_anual_expenses = df.resample('YE').sum()

        self.plot_graph('bar', df_anual_expenses,title='Gastos Anuales',format='%Y')

    def historial_expenses(self): ##funcion para ver historial de gastos##
        return [t for t in self.transactions_list if t.type == 'expense']

    #Funciones prácticas#
    def save_graph(self, parent_file, filename):
        os.makedirs(parent_file, exist_ok=True)
        filename = os.path.basename(filename)  # Asegura que filename no tenga separadores ni rutas
        ruta_imagen = os.path.join(parent_file, filename) # Guardar la imagen
        plt.savefig(ruta_imagen)
        print(f"Gráfica guardada como: {ruta_imagen}")
        
    def plot_graph(self, graph_type, values, title, labels=None,format=None ):
        plt.figure(figsize=(6, 4))
        sns.set_theme(style="whitegrid")
        sns.set_palette("pastel")

        if graph_type == 'pie':
            # labels ahora es un argumento nombrado
            plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.title(title)
            
        elif graph_type == 'bar':
            sns.set_context("talk")
            # values debe ser un DataFrame con columnas 'Date' y 'Amount'
            values['DateStr']=values.index.strftime(format)
            sns.barplot(data=values, x='DateStr', y='Amount', hue='Amount', palette='pastel',legend=False)
            plt.xticks(rotation=0)
            plt.title(title)
            plt.xlabel("Fecha")
            plt.ylabel("Monto ($)")

        safe_title = title.replace('/', '-')
        self.save_graph("graficas", safe_title +'.png')
        plt.tight_layout()
        plt.show()

