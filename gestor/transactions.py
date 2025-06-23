from datetime import datetime
from typing import Optional

class Transactions: 
    ''' Clase de las transacciones financieras.
    Esta clase representa una transacción financiera, ya sea un ingreso o un gasto.
    Atributos:
        model (str): Tipo de transacción ('ingreso' o 'gasto').
        amount (float): Monto de la transacción.
        category (str): Categoría de la transacción.
        description (str): Descripción de la transacción.
        date (str): Fecha y hora de la transacción en formato 'dd-mm-YYYY HH:MM:SS'.
        DATE_FORMAT (str): Formato de fecha y hora utilizado para la transacción.
    '''
    DATE_FORMAT = '%d-%m-%Y %H:%M:%S' #formato de fecha y hora
    
    def __init__(self, model: str, amount: float, category: str, description: str, date: Optional[str] = None):
        self.Model = model #ingreso o gasto#
        self.Amount = amount
        self.Category = category
        self.Description = description
        if date:
                try:
                    self.Date = datetime.strptime(date, self.DATE_FORMAT) #convirtiendo str
                except ValueError:
                    raise ValueError(f"Formato de fecha inválido: {date}")
        else:
            self.Date = datetime.now()

    def __str__(self) -> str:
        # Formatea la fecha solo al mostrarla
        formated_date = self.Date.strftime(self.DATE_FORMAT)
        parts = [self.Model, self.Amount, self.Category, self.Description, formated_date]
        return ' - '.join(str(x) for x in parts if x)