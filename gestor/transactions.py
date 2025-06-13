from datetime import datetime
from typing import Optional

class Transactions: 
    ''' Clase de las transacciones financieras.
    Esta clase representa una transacción financiera, ya sea un ingreso o un gasto.
    Atributos:
        type (str): Tipo de transacción ('ingreso' o 'gasto').
        amount (float): Monto de la transacción.
        category (str): Categoría de la transacción.
        description (str): Descripción de la transacción.
        date (str): Fecha y hora de la transacción en formato 'dd-mm-YYYY HH:MM:SS'.
        DATE_FORMAT (str): Formato de fecha y hora utilizado para la transacción.
    '''
    DATE_FORMAT = '%d-%m-%Y %H:%M:%S' #formato de fecha y hora
    
    def __init__(self, type: str, amount: float, category: str, description: str, date: Optional[str] = None):
        self.type = type #ingreso o gasto#
        self.amount = amount
        self.category = category
        self.description = description
        if date:
                try:
                    format = datetime.strptime(date, self.DATE_FORMAT) #convirtiendo str
                    self.date = format.strftime(self.DATE_FORMAT) #formatenado fecha y guardando como atributo
                except ValueError:
                    raise ValueError(f"Formato de fecha inválido: {date}")
        else:
            time = datetime.now()
            self.date = time.strftime(self.DATE_FORMAT)

    def __str__(self) -> str:
        list = [self.type, self.amount, self.category, self.description, self.date]
        parts = []
        for x in list:
            if x:
                parts.append(str(x))
        return ' - '.join(parts)