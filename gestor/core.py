import csv
from transactions import Transactions
from typing import List

class FinanceManager:
    def __init__(self):
        self.transactions_list = []
    
    def load_csv(self, filename: str) -> None: ##funcion para cargar csv##
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
            print(f"Error: El archivo {filename} no existe.")
            pass

    def save_csv(self, filename: str) -> None: ##funcion para guardar en csv##
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Type', 'Amount', 'Category', 'Description', 'Date/Time'])
            for t in self.transactions_list:
                writer.writerow([t.type, t.amount, t.category, t.description, t.date])        

    def add_transaction(self, transaction: Transactions) -> None: ##añadir transaccion##
        self.transactions_list.append(transaction)

    def total_balance(self) -> float: ##funcion para calcular balance total##
        total = 0
        for t in self.transactions_list:
            if t.type == 'income':
                total += t.amount
            else:
                total -= t.amount
        return total    
    
    def categories_expenses(self) -> dict[str, float]: ##funcion para calcular gastos por categoria##
        categories = {}
        for t in self.transactions_list:
            if t.type == 'expense':
                categories[t.category] = categories.get(t.category, 0) + t.amount
        return categories

    def historial_expenses(self) -> List[Transactions]: ##funcion para ver historial de gastos##
        return [t for t in self.transactions_list if t.type == 'expense']


