import csv
from transactions import Transactions
from typing import List
import pandas as pd
import os
class FinanceManager:
    ''' Clase para gestionar las transacciones financieras.
    Esta clase permite cargar, guardar y manipular transacciones financieras,
    así como calcular balances y gastos por categoría.
    Atributos:
        transactions_list (List[Transactions]): Lista de transacciones financieras.
        DATE_FORMAT (str): Formato de fecha y hora utilizado para las transacciones.
        FILE_PATH (str): Ruta del archivo donde se guardan las transacciones.
    Métodos:
        load_csv: Carga transacciones desde un archivo CSV.
        save_csv: Guarda transacciones en un archivo CSV.
        add_transaction: Añade una nueva transacción a la lista.
        total_balance: Calcula el balance total de las transacciones.
        categories_expenses: Calcula los gastos totales por categoría.
        historial_expenses: Devuelve un historial de todas las transacciones de tipo 'expense'.
    ''' 
    
    DATE_FORMAT = '%d-%m-%Y %H:%M:%S'
    FILE_PATH = os.path.join('data', os.path.basename('data.xlsx'))
    
    def __init__(self):
        self.transactions_list = []

    #Actualmente no se utiliza este método, pero se puede implementar en el futuro#    
    def load_csv(self, filename: str = os.path.join('data', os.path.basename('data.csv'))) -> None:
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
       
    def load_excel(self) -> None:
        '''Carga transacciones desde un archivo excel.'''
        try:
            df = pd.read_excel(self.FILE_PATH)
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
            print(f"Error: El archivo {self.FILE_PATH} no existe.")
            pass

    def save_excel(self) -> str:
        '''Guarda transacciones en un archivo Excel.'''
        os.makedirs('data', exist_ok=True)
        data = [t.__dict__ for t in self.transactions_list]
        df = pd.DataFrame(data)
        df.to_excel(self.FILE_PATH, index=False)
        print(f'Reporte exportado exitosamente a {self.FILE_PATH}')
        return self.FILE_PATH      


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
        df = pd.DataFrame([t.__dict__ for t in self.transactions_list])
        df['date'] = pd.to_datetime(df['date'], format=self.DATE_FORMAT)
        df = df[df['model'] == 'expense']
        return df