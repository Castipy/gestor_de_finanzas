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
        load_excel: Carga transacciones desde un archivo Excel.
        save_csv: Guarda transacciones en un archivo CSV.
        add_transaction: Añade una nueva transacción a la lista.
        total_balance: Calcula el balance total de las transacciones.
        expenses: Calcula los gastos totales por categoría agrupados por mes y año.
        monthly_expenses: Calcula los gastos mensuales por categoría o por día.
        anual_expenses: Calcula los gastos anuales o los gastos de los últimos 10 años.
    ''' 
    
    DATE_FORMAT = '%d-%m-%Y %H:%M:%S'
    FILE_PATH = os.path.join('data', os.path.basename('data.xlsx'))
    
    def __init__(self):
        self.df_transactions = pd.DataFrame()

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
            #Iterando sobre filas y columnas en este caso omite las columnas#
            for _, row in df.iterrows(): 
                try:
                    t = Transactions(
                        row['Model'],
                        float(row['Amount']),
                        row['Category'],
                        row['Description'],
                        row['Date']
                    )
                     # Creando el DF concatenando los atributos de la clase Transactions y los del propio DataFrame
                    self.df_transactions = pd.concat([self.df_transactions, 
                                                      pd.DataFrame([t.__dict__])], 
                                                      ignore_index=True)
                except (KeyError, ValueError) as e:
                    print(f"\n""Warning: Skipping invalid row {row}. Error: {e}")
        except FileNotFoundError:
            print(f"\n""Error: El archivo {self.FILE_PATH} no existe.")
            pass

    def save_excel(self) -> str:
        '''Guarda transacciones en un archivo Excel.'''
        #Asegurandonos de que el directorio existe
        os.makedirs('data', exist_ok=True) 
        #Formateando columna Date antes de guardar
        self.df_transactions['Date'] = self.df_transactions['Date'].dt.strftime(self.DATE_FORMAT) 
        print(self.df_transactions)
        self.df_transactions.to_excel(self.FILE_PATH, index=False)
        print(f'Reporte exportado exitosamente a {self.FILE_PATH}')
        return self.FILE_PATH      

    def add_transaction(self, transaction: Transactions) -> None:
        '''Añade una nueva transacción a la lista.'''
        self.df_transactions = pd.concat([self.df_transactions, pd.DataFrame([transaction.__dict__])], ignore_index=True)

    def total_balance(self) -> float:
        '''Calcula el balance total de las transacciones.'''
        if self.df_transactions.empty:
            print("\n""No hay transacciones registradas.")
            return 0.0
        total_expenses = self.df_transactions.loc[self.df_transactions['Model'] == 'expense', 'Amount'].sum()
        total_incomes = self.df_transactions.loc[self.df_transactions['Model'] == 'income', 'Amount'].sum()
        return float(total_incomes - total_expenses)
    
    def expenses(self) -> tuple:
        '''Calcula los gastos totales por categoría agrupados por mes y año.'''
        # Chequeo de transacciones #
        if self.df_transactions.empty: 
            print("\n""No hay transacciones registradas.")
            return pd.DataFrame()
        # Filtrando por gastos #
        expenses = self.df_transactions[self.df_transactions['Model'] == 'expense'].copy()
        #Chequeo de gastos
        if expenses.empty:
            return expenses
        # Columna Date nuevo indice para filtrado #
        expenses.set_index('Date', inplace=True)
        # Aun no tiene uso la tabla resumen pero muestra los gastos #
        resumen = expenses.groupby(['Category'])['Amount'].sum().reset_index()
        return expenses,resumen
              
    def monthly_expenses(self, year:str=None, month:str=None, daily:bool=False)-> pd.DataFrame:
        '''Calcula los gastos mensuales por categoría o por día.'''
        expenses,_ = self.expenses()
        # Filtrando por año y mes introducidos por usuario o actuales # 
        try:
            year = int(year) if year else pd.Timestamp.now().year
            month = int(month) if month else pd.Timestamp.now().month
        except ValueError:
            print("\n""Año y mes deben ser números enteros.")
            return
        expenses = expenses[(expenses.index.year == year) & (expenses.index.month == month)]
        if expenses.empty:
            return expenses
        # Si no se especifica que los gastos son diarios solo retornamos los gastos del mes por categorias#
        if not daily:
            resumen = expenses.groupby(['Category'])['Amount'].sum().reset_index()
        else:
            #Creando tabla pivote para mostrar los datos diferente#
            resumen = expenses.pivot_table(
                index=expenses.index.day,   # cada día como fila
                columns='Category',          # cada categoría como columna
                values='Amount',
                aggfunc='sum',
                fill_value=0
                ).reset_index()
        return resumen
    
    def anual_expenses(self, year:str=None, all_years:bool=False)-> pd.Series:
        '''Calcula los gastos anuales o los gastos de los ultimos 10 años.'''
        expenses,_ = self.expenses()
        try:
            year = int(year) if year else pd.Timestamp.now().year 
        except ValueError:
            print("\n""Año y mes deben ser números enteros.")
            return 
        if not all_years:
            #Filtrando por el año seleccionado#
            expenses = expenses[expenses.index.year == year]
            expenses['Month'] = expenses.index.month
            # Agrupar por mes y sumar
            resumen = expenses.groupby('Month')['Amount'].sum()
            return resumen
        else:
            actual_year = pd.Timestamp.now().year
            #Filtrando gastos de los 10 ultimos años#
            list_years = list(range(actual_year-9, actual_year + 1))
            resumen = expenses[expenses.index.year.isin(list_years)]
            resumen['Years'] = resumen.index.year
            resumen = resumen.groupby('Years')['Amount'].sum()
            return resumen