import unittest
from gestor.transactions import Transactions
from datetime import datetime

class TestTransactions(unittest.TestCase):

    def test_transaction_creation(self):
        t = Transactions('income', 100.0, 'Salario', 'Pago mensual', '01-06-2024 10:00:00')
        self.assertEqual(t.Model, 'income')
        self.assertEqual(t.Amount, 100.0)
        self.assertEqual(t.Category, 'Salario')
        self.assertEqual(t.Description, 'Pago mensual')
        self.assertIsInstance(t.Date, datetime)

    def test_transaction_invalid_date(self):
        with self.assertRaises(ValueError):
            Transactions('expense', 50.0, 'Comida', 'Cena', '2024-06-01')

if __name__ == '__main__':
    unittest.main()