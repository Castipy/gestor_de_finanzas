import csv
from transactions import Transactions

class FinanceManager:
    def __init__(self):
        self.transactions_list = []
    
    def add_transaction(self, transaction):
        self.transactions_list.append(transaction)

    def save_csv(self, filename):
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Type', 'Amount', 'Category', 'Description', 'Date/Time'])
            for t in self.transactions_list:
                writer.writerow([t.type, t.amount, t.category, t.description, t.date.strftime('%Y-%m-%Y%H:%M:%S')])

    def load_csv(self, filename):
        try:
            with open(filename, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    t = Transactions(
                        row['Type'],
                        float(row['Amount']),
                        row['Category'],
                        row['Description'],
                        row['Date/Time']
                    )
                    self.transactions_list.append(t)
        except FileNotFoundError:
            pass

    def total_balance(self):
        total = 0
        for t in self.transactions_list:
            if t.type == 'income':
                total += t.amount
            else:
                total -= t.amount
        return total    
    
    def categories_expenses(self):
        categories = {}
        for t in self.transactions_list:
            if t.type == 'expense':
                categories[t.category] = categories.get(t.category, 0) + t.amount
        return categories
