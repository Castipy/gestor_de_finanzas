import csv
from transactions import Transactions
import matplotlib.pyplot as plt
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
        if not expenses:
            print("No hay gastos registrados para mostrar en el gráfico.")
            return
        df = pd.DataFrame(list(expenses.items()), columns=['Category', 'Amount'])
         #Ajustar elemntos para que no se superpongan#
        self.plot_graph('pie',df['Amount'], df['Category'], 'Gastos por Categoría')

    def monthly_expenses_graphic(self, year, month): ##funcion para crear gráfico de gastos mensuales##
        try:    
            year = int(year) if year else pd.Timestamp.now().year
            month = int(month) if month else pd.Timestamp.now().month
        except ValueError:
            print("Año y mes deben ser números enteros.")
            return
        
        expenses = self.historial_expenses()
        if not expenses:
            print("\nNo hay gastos registrados para mostrar en el gráfico.")
            return
        
        df = pd.DataFrame([{'Date': t.date,'Amount': t.amount,
        } for t in expenses])
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y %H:%M:%S')
        df.set_index('Date', inplace=True)
        
        # Filtrar Gastos por año y mes#
        df_monthly_expenses = df[(df.index.year == year) & (df.index.month == month)]
        if df_monthly_expenses.empty:
            print(f"\nNo hay gastos registrados para el mes {month} del año {year}.")
            return  
        #Filtrar Gastos diarios del mes especificado#
        df_daily_expenses = df_monthly_expenses.resample('D').sum()

        self.plot_graph('bar', df_daily_expenses['Amount'], df_daily_expenses.index, f'Gastos diarios - {month:02d}/{year}')

    def historial_expenses(self): ##funcion para ver historial de gastos##
        return [t for t in self.transactions_list if t.type == 'expense']

    #Funciones prácticas#
    def save_graph(self, parent_file, filename):
        os.makedirs(parent_file, exist_ok=True)
        ruta_imagen = os.path.join(parent_file, filename) # Guardar la imagen
        plt.savefig(ruta_imagen)
        print(f"Gráfica guardada como: {ruta_imagen}")
        
    def plot_graph(self, type, values, label, title):
        if type == 'pie':
            plt.figure(figsize=(6,6))
            plt.pie(values, labels=label, autopct='%1.1f%%', startangle=140)
            plt.title(title)
            plt.tight_layout()
            self.save_graph("graficas", "gastos_categorías.png")
            plt.show()
        else:
            plt.figure(figsize=(6, 4))
            values.plot(kind=type, color='skyblue', edgecolor='black')
            plt.xticks(ticks=range(len(values)), labels=label.strftime('%d'), rotation=0)
            plt.grid(axis='both', linestyle='--', alpha=0.7)
            plt.xlabel('Día')
            plt.ylabel('Monto')
            self.save_graph("graficas", "gastos_diarios.png")
            plt.show()