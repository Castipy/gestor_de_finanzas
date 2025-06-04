from datetime import datetime

class Transactions:
    def __init__(self, type, amount, category, description):
        self.type = type #ingreso o gasto#
        self.amount = amount
        self.category = category
        self.description = description
        self.date = datetime.now()
    def __str__(self):
        return (f"{self.type}: "
                f"{self.amount} - "
                f"{self.category} - "
                f"{self.description} - "
                f"{self.date.strftime('%d-%m-%Y %H:%M:%S')}")