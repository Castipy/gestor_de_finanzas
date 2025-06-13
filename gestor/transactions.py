from datetime import datetime
from typing import Optional

class Transactions:
    def __init__(self, type: str, amount: float, category: str, description: str, date: Optional[str] = None):
        self.type = type #ingreso o gasto#
        self.amount = amount
        self.category = category
        self.description = description
        if date:
                try:
                    format = datetime.strptime(date, '%d-%m-%Y %H:%M:%S') #convirtiendo str
                    self.date = format.strftime('%d-%m-%Y %H:%M:%S') #formatenado fecha y guardando como atributo
                except ValueError:
                    raise ValueError(f"Formato de fecha inválido: {date}")
        else:
            time = datetime.now()
            self.date = time.strftime('%d-%m-%Y %H:%M:%S')

    def __str__(self) -> str:
        list = [self.type, self.amount, self.category, self.description, self.date]
        parts = []
        for x in list:
            if x:
                parts.append(str(x))
        return ' - '.join(parts)