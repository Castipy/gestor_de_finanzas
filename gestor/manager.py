import csv
from transactions import Transactions
import matplotlib.pyplot as plt
from datetime import datetime
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
    
    def pie_graphic(self): #funcion para crear gráfico de pastel##
        expenses = self.categories_expenses()
        if not expenses:
            print("No hay gastos registrados para mostrar en el gráfico.")
            return
        labels = list(expenses.keys())
        values = list(expenses.values())
        plt.figure(figsize=(8,8))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Gastos por Categoría")
 
        os.makedirs("graficas", exist_ok=True) # Crear carpeta si no existe
        ruta_imagen = os.path.join("graficas", "grafica_gastos.png") # Guardar la imagen
        plt.savefig(ruta_imagen)
        print(f"Gráfica guardada como: {ruta_imagen}")
        plt.show() #Mostrar la figura#


    def historial_expenses(self): ##funcion para ver historial de gastos##
        return [t for t in self.transactions_list if t.type == 'expense']
