from gestor.transactions import Transactions
import pandas as pd
import os
import glob
class FinanceManager:
    ''' Clase para gestionar las transacciones financieras.
    Esta clase permite cargar, guardar y manipular transacciones financieras,
    así como calcular balances y gastos por categoría.
    Atributos:
        transactions_list (List[Transactions]): Lista de transacciones financieras.
        DATE_FORMAT (str): Formato de fecha y hora utilizado para las transacciones.
        ERROR (pd.DataFrame): DataFrame para registrar errores durante la carga de transacciones.
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
    ERROR = pd.DataFrame(columns=['Error','Message'])
    
    def __init__(self):
        self.df_transactions = pd.DataFrame({
            'Model': pd.Series(dtype='str'),
            'Amount': pd.Series(dtype='float'),
            'Category': pd.Series(dtype='str'),
            'Description': pd.Series(dtype='str'),
            'Date': pd.Series(dtype='datetime64[ns]')
        })

#########################################
#Cargar y Salvar Archivos Excel#
#########################################    
       
    def load_excel(self) -> pd.DataFrame:
        '''Carga transacciones desde un archivo excel.'''
        files = glob.glob(os.path.join('data', 'data_*.xlsx'))
        try:
            latest_file = max(files, key=os.path.getctime)
            df = pd.read_excel(latest_file)

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
                    
                    # Formateando la columna Date a tipo datetime#
                    self.convert_date(self.df_transactions, 'Date', 'to_datetime')
                except (KeyError, ValueError) as e:
                    self.ERROR=self.errors_register(e, f'Error al procesar la fila: {row}')
            return self.ERROR if not self.ERROR.empty else None
        except (FileNotFoundError, ValueError) as e:
            self.ERROR=self.errors_register(e, f'Archivo no encontrado en ruta {files}')
            return self.ERROR if not self.ERROR.empty else None

    def save_excel(self) -> str:
        '''Guarda transacciones en un archivo Excel.'''
        #Asegurandonos de que el directorio existe
        os.makedirs('data', exist_ok=True) 
        #Formateando columna Date antes de guardar
        self.convert_date(self.df_transactions, 'Date', 'to_string')
        #Guardando el DataFrame en un archivo Excel con la fecha actual
        filename = f"data_{pd.Timestamp.now().strftime('%Y-%m-%d')}.xlsx"
        path = os.path.join('data', filename)
        self.df_transactions.to_excel(path, index=False)
        return path     

#########################################
#Añadir transaccion,mostrar gastos#
#########################################

    def add_transaction(self, transaction: Transactions) -> None:
        '''Añade una nueva transacción a la lista.'''
        # Asegura que todas las columnas estén presentes en el diccionario
        data = {col: getattr(transaction, col, None) for col in self.df_transactions.columns}
        # Si TODOS los valores son None, no agregues la fila (evita el warning)
        if all(v is None for v in data.values()):
            return
        new_row = pd.DataFrame([data], columns=self.df_transactions.columns)
        self.df_transactions = pd.concat([self.df_transactions, new_row], ignore_index=True)

    def total_balance(self) -> float:
        '''Calcula el balance total de las transacciones.'''
        if self.df_transactions.empty:
            return pd.DataFrame()
        total_expenses = self.df_transactions.loc[self.df_transactions['Model'] == 'expense', 'Amount'].sum()
        total_incomes = self.df_transactions.loc[self.df_transactions['Model'] == 'income', 'Amount'].sum()
        return float(total_incomes - total_expenses)
    
    def expenses(self) -> tuple:
        '''Calcula los gastos totales por categoría agrupados por mes y año.'''
        # Filtrando por gastos #
        expenses = self.df_transactions[self.df_transactions['Model'] == 'expense'].copy()
        #Chequeo de gastos
        if expenses.empty:
            return expenses, pd.DataFrame()
        # Columna Date nuevo indice para filtrado #
        expenses.set_index('Date', inplace=True)
        # Aun no tiene uso la tabla resumen pero muestra los gastos #
        resumen = expenses.groupby(['Category'])['Amount'].sum().reset_index()
        return expenses,resumen
              
    def monthly_expenses(self, year:str=None, month:str=None, daily:bool=False)-> tuple:
        '''Calcula los gastos mensuales por categoría o por día.'''
        expenses,_ = self.expenses()
         # Asegura que el índice es datetime parapruebas posteriores #
        if not isinstance(expenses.index, pd.DatetimeIndex):
            if 'Date' in expenses.columns:
                expenses['Date'] = pd.to_datetime(expenses['Date'], errors='coerce')
                expenses = expenses.set_index('Date')
        # Filtrando por año y mes introducidos por usuario o actuales # 
        try:
            year = int(year) if year else pd.Timestamp.now().year
            month = int(month) if month else pd.Timestamp.now().month
            expenses = expenses[(expenses.index.year == year) & (expenses.index.month == month)]
        except (ValueError) as e:
            return 'invalid_date', pd.DataFrame()
        if expenses.empty:
            return 'no_data',expenses
        # Si no se especifica que los gastos son diarios solo retornamos los gastos del mes por categorias#
        if not daily:
            resumen = expenses.groupby(['Category'])['Amount'].sum().reset_index()
            return 'ok', resumen
        else:
            #Creando tabla pivote para mostrar los datos diferente#
            resumen = expenses.pivot_table(
                index=expenses.index.day,   # cada día como fila
                columns='Category',          # cada categoría como columna
                values='Amount',
                aggfunc='sum',
                fill_value=0
                ).reset_index()
        return 'ok',resumen
    
    def anual_expenses(self, year:str=None, all_years:bool=False)-> tuple:
        '''Calcula los gastos anuales o los gastos de los ultimos 10 años.'''
        expenses,_ = self.expenses()
        # Asegura que el índice es datetime para pruebas posteriores #
        if not isinstance(expenses.index, pd.DatetimeIndex):
            if 'Date' in expenses.columns:
                expenses['Date'] = pd.to_datetime(expenses['Date'], errors='coerce')
                expenses = expenses.set_index('Date')
        try:
            year = int(year) if year else pd.Timestamp.now().year 
        except (ValueError) as e:
            return 'invalid_year', pd.DataFrame()
        
        if not all_years:
            #Filtrando por el año seleccionado#
            expenses = expenses[expenses.index.year == year]
            expenses['Month'] = expenses.index.month
            if expenses.empty:
                return 'no_data', pd.Series()
            
            # Agrupar por mes y sumar
            resumen = expenses.groupby('Month')['Amount'].sum()
            return 'ok',resumen
        else:
            actual_year = pd.Timestamp.now().year
            #Filtrando gastos de los 10 ultimos años#
            list_years = list(range(actual_year-9, actual_year + 1))
            resumen = expenses[expenses.index.year.isin(list_years)]
            if resumen.empty:
                return 'no_data', pd.Series()
            
            # Agrupar por año y sumar
            resumen['Years'] = resumen.index.year
            resumen = resumen.groupby('Years')['Amount'].sum()
            return 'ok',resumen

#########################################
        #Manejo de Errores#
######################################### 
    def convert_date(self, df: pd.DataFrame, date_column: str, conv_type:str) -> pd.DataFrame:
        '''Convierte una columna de fecha a tipo datetime.'''

        if conv_type == 'to_datetime':
            try:
                df[date_column] = pd.to_datetime(df[date_column], format=self.DATE_FORMAT)
            except ValueError:
                pass
            return df
        
        elif conv_type == 'to_string':
            df[date_column] = df[date_column].dt.strftime(self.DATE_FORMAT)
            return df 
         
    def errors_register(self, e, message) -> pd.DataFrame:
        '''Retorna los errores registrados'''
        self.ERROR = pd.concat([self.ERROR, 
                                    pd.DataFrame([{'Error': type(e).__name__, 'Message': message}])], 
                                    ignore_index=True)
        return self.ERROR

#########################################
#Mostrar,Eliminar y Editar transacciones#
#########################################

    def list_transactions(self, model_filter: str = None) -> pd.DataFrame:
        '''Devuelve las transacciones con sus índices visibles, opcionalmente filtradas por tipo.'''
        
        if self.df_transactions.empty:
            return pd.DataFrame()
        
        df_copy = self.df_transactions.copy()
        df_copy.index.name = 'Index'
        if model_filter in ['income', 'expense']:
            df_copy = df_copy[df_copy['Model'] == model_filter]
        
        return df_copy.reset_index()
    
    def delete_transaction(self, index: int) -> bool:
        '''Elimina una transacción por su índice. Retorna True si se eliminó, False si no.'''
        if 0 <= index < len(self.df_transactions):
            self.df_transactions.drop(index=index, inplace=True)
            self.df_transactions.reset_index(drop=True, inplace=True)
            return True
        return False
    
    def edit_transaction(self, index: int, **kwargs) -> bool:
        '''Edita una transacción por su índice. kwargs pueden ser columnas nuevas.'''
        if 0 <= index < len(self.df_transactions):
            for key, value in kwargs.items():
                if key in self.df_transactions.columns:
                    if key == 'Date':
                        try:
                            value = pd.to_datetime(value, format=self.DATE_FORMAT)
                        except ValueError:
                            continue  # Ignora si la fecha es inválida
                    self.df_transactions.at[index, key] = value
                else:
                    return False               
            return True
        return False
    
    def search_transactions(self, model: str = None, 
                            category: str = None,
                            description: str = None,
                            start_date: str = None,
                            end_date: str = None) -> pd.DataFrame:
        '''Busca transacciones por modelo, categoría, descripción y rango de fechas.'''
        if self.df_transactions.empty:
            return pd.DataFrame()
        
        df = self.df_transactions.copy()

        if model:
            df = df[df['Model'].str.lower() == model.lower()]
        if category:
            df = df[df['Category'].str.lower().str.contains(category.lower())]
        if description:
            df = df[df['Description'].str.lower().str.contains(description.lower())]
        if start_date:
            try:
                start_date = pd.to_datetime(start_date, format=self.DATE_FORMAT)
                df = df[df['Date'] >= start_date]
            except ValueError:
                return pd.DataFrame()
        if end_date:
            try:
                end_date = pd.to_datetime(end_date, format=self.DATE_FORMAT)
                df = df[df['Date'] <= end_date]
            except ValueError:
                pass
        return df
    
            