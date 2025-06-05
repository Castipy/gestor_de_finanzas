from datetime import datetime

class Transactions:
    def __init__(self, type, amount, category, description, date=None):
        self.type = type #ingreso o gasto#
        self.amount = amount
        self.category = category
        self.description = description
        if date:
            if isinstance(date, str):
                self.date = datetime.strptime(date, '%d-%m-%Y %H:%M:%S')
        else:
            time = datetime.now()
            self.date = time.strftime('%d-%m-%Y %H:%M:%S')

    def __str__(self):
        return (f"{self.type}: "
                f"- {self.amount}"
                f" - {self.category}"
                f" - {self.description}"
                f" - {self.date}")