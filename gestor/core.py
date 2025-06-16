import csv
from transactions import Transactions
from typing import List
import pandas as pd

class FinanceManager:
    ''' Clase para gestionar las transacciones financieras.
    Esta clase permite cargar, guardar y manipular transacciones financieras,
    así como calcular balances y gastos por categoría.
    Atributos:
        transactions_list (List[Transactions]): Lista de transacciones financieras.
        DATE_FORMAT (str): Formato de fecha y hora utilizado para las transacciones.
    Métodos:
        load_csv: Carga transacciones desde un archivo CSV.
        save_csv: Guarda transacciones en un archivo CSV.
        add_transaction: Añade una nueva transacción a la lista.
        total_balance: Calcula el balance total de las transacciones.
        categories_expenses: Calcula los gastos totales por categoría.
        historial_expenses: Devuelve un historial de todas las transacciones de tipo 'expense'.
    ''' 
    
    DATE_FORMAT = '%d-%m-%Y %H:%M:%S'
    
    def __init__(self):
        self.transactions_list = []
    
    def load_csv(self, filename: str) -> None:
        '''Carga transacciones desde un archivo CSV.'''
        try:
            df = pd.read_csv(filename, encoding='utf-8')
            for _, row in df.iterrows():
                try:
                    t = Transactions(
                        row['Model'],
                        float(row['Amount']),
                        row['Category'],
                        row['Description'],
                        row['Date/Time']
                    )
                    self.transactions_list.append(t)
                except (KeyError, ValueError) as e:
                    print(f"Warning: Skipping invalid row {row}. Error: {e}")
        except FileNotFoundError:
            print(f"Error: El archivo {filename} no existe.")
            pass

    def save_csv(self, filename: str) -> None:
        '''Guarda transacciones en un archivo CSV.'''
        data = [t.__dict__ for t in self.transactions_list]
        df = pd.DataFrame(data)
        df.columns = ['model', 'amount', 'category', 'description', 'date']
        df.to_csv(filename, index=False)       

    def add_transaction(self, transaction: Transactions) -> None:
        '''Añade una nueva transacción a la lista.'''

        self.transactions_list.append(transaction)

    def total_balance(self) -> float:
        '''Calcula el balance total de las transacciones.'''
        total = 0
        for t in self.transactions_list:
            if t.model == 'income':
                total += t.amount
            else:
                total -= t.amount
        return total    
    
    def categories_expenses(self) -> dict[str, float]:
        '''Calcula los gastos totales por categoría.'''
        categories = {}
        for t in self.transactions_list:
            if t.model == 'expense':
                categories[t.category] = categories.get(t.category, 0) + t.amount
        return categories

    def historial_expenses(self) -> List[Transactions]: 
        '''Devuelve un historial de todas las transacciones de tipo 'expense'.'''
        return [t for t in self.transactions_list if t.model == 'expense']


