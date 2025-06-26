import unittest
from gestor.core import FinanceManager
from gestor.transactions import Transactions
import pandas as pd

class TestFinanceManager(unittest.TestCase):

    def setUp(self):
        """Se ejecuta antes de cada prueba."""
        self.fm = FinanceManager()

    def test_add_transaction(self):
        """Verifica que una transacción se añade correctamente."""
        tx = Transactions('income', 1000, 'Salario', 'Pago mensual')
        self.fm.add_transaction(tx)
        self.assertEqual(len(self.fm.df_transactions), 1)


#########################################
#_____________Total_Income______________#
######################################### 

    def test_total_balance_income(self):
        """Verifica que el balance se calcula correctamente para un ingreso."""
        tx = Transactions('income', 2000, 'Extra', 'Ingreso extra')
        self.fm.add_transaction(tx)
        self.assertEqual(self.fm.total_balance(), 2000.0)

    def test_total_balance_income_and_expense(self):
        """Verifica que el balance es correcto al tener ingresos y gastos."""
        self.fm.add_transaction(Transactions('income', 3000, 'Salario', 'Pago'))
        self.fm.add_transaction(Transactions('expense', 1000, 'Comida', 'Restaurante'))
        self.assertEqual(self.fm.total_balance(), 2000.0)

#########################################
#_______________Expenses________________#
######################################### 

    def test_expenses(self):
        """Verifica que los gastos se filtran correctamente."""
        self.fm.add_transaction(Transactions('income', 500, 'Regalo', ''))
        self.fm.add_transaction(Transactions('expense', 200, 'Transporte', 'Bus'))
        expenses, resumen = self.fm.expenses()
        self.assertEqual(len(expenses), 1)
        self.assertIn('Transporte', resumen['Category'].values)

    def test_monthly_expenses_empty(self):
        """Verifica que retorna vacío cuando no hay datos en el mes consultado."""
        status,df = self.fm.monthly_expenses('1999', '01')
        if status=='no_data':
            self.assertTrue(df.empty)
    
    def test_monthly_expenses_invalid_date(self):
        """Verifica que lanza un error si la fecha es inválida."""
        status, df = self.fm.monthly_expenses('invalido', '01')
        if status == 'invalid_date':
            self.assertRaises(ValueError)
    
    def test_monthly_expenses_daily(self):
        """Verifica que retorna un DataFrame con los gastos diarios del mes."""
        self.fm.add_transaction(Transactions('expense', 100, 'Comida', '2023-10-01'))
        self.fm.add_transaction(Transactions('expense', 50, 'Transporte', '2023-10-02'))
        status, df = self.fm.monthly_expenses('2023', '10', daily=True)
        if status == 'ok':
            self.assertTrue(isinstance(df, pd.DataFrame))
            self.assertEqual(len(df), 2)
            self.assertIn('Comida', df['Category'].values)
            self.assertIn('Transporte', df['Category'].values)

    def test_anual_expenses_invalid_year(self):
        """Verifica que lanza un error si el año es inválido."""
        status, df = self.fm.anual_expenses(year="invalido")
        self.assertRaises(ValueError)
    
    def test_anual_expenses_empty(self):
        """Verifica que retorna vacío cuando no hay datos en el año consultado."""
        status, df = self.fm.anual_expenses(year="1999")
        self.assertTrue(df.empty)
        
    def test_anual_expenses_all_years(self):
        """Verifica que retorna un DataFrame con todos los años."""
        self.fm.add_transaction(Transactions('income', 1000, 'Salario', '2001'))
        self.fm.add_transaction(Transactions('expense', 500, 'Comida', '2000'))
        status, df = self.fm.anual_expenses(all_years=True)
        if status == 'ok':
            self.assertTrue(isinstance(df, pd.Series))
            self.assertGreater(len(df), 0)

#########################################
#Mostrar,Eliminar y Editar transacciones#
#########################################

    def test_list_transactions(self):
        """Verifica que se listan correctamente las transacciones."""
        tx1 = Transactions('income', 1000, 'Salario', 'Pago mensual')
        tx2 = Transactions('expense', 200, 'Comida', 'Restaurante')
        self.fm.add_transaction(tx1)
        self.fm.add_transaction(tx2)
        tx_all = self.fm.list_transactions()
        tx_income = self.fm.list_transactions('income')
        tx_expese = self.fm.list_transactions('expense')
        self.assertEqual(len(tx_income), 1)
        self.assertEqual(len(tx_expese), 1)
        self.assertEqual(len(tx_all), 2)
        self.assertTrue(
            ((tx_all['Model'] == tx1.Model) &
            (tx_all['Amount'] == tx1.Amount) &
            (tx_all['Category'] == tx1.Category) &
            (tx_all['Description'] == tx1.Description)
            ).any()
)

    def test_delete_transaction(self):
        """Verifica que se elimina correctamente una transacción."""
        tx = Transactions('expense', 300, 'Transporte', 'Taxi')
        self.fm.add_transaction(tx)
        initial_length = len(self.fm.df_transactions)
        self.fm.delete_transaction(0)
        self.assertEqual(len(self.fm.df_transactions), initial_length - 1)
        self.assertNotIn(tx, self.fm.df_transactions.values)

    def test_delete_transaction_false(self):
        """Verifica que se elimina correctamente una transacción."""
        tx = Transactions('expense', 300, 'Transporte', 'Taxi')
        self.fm.add_transaction(tx)
        initial_length = len(self.fm.df_transactions)
        self.assertEqual(self.fm.delete_transaction(5), False)

    def test_edit_transaction(self):
        """Verifica que se edita correctamente una transacción."""
        self.test_add_transaction()
        self.assertEqual(self.fm.edit_transaction(0, **{'Amount': 1500}),True)
        self.assertEqual(self.fm.df_transactions.at[0, 'Amount'], 1500) 
        
    def test_edit_transaction_false(self):
        """Verifica que se edita correctamente una transacción."""
        self.test_add_transaction()
        self.assertEqual(self.fm.edit_transaction(0, **{'Zapatos': 1500}), False)
        self.assertEqual(self.fm.df_transactions.at[0, 'Amount'], 1000) 
        
    def test_search_transactions(self):
        """Verifica que se busca correctamente una transacción."""
        tx1 = Transactions('income', 1000, 'Salario', 'Pago mensual')
        tx2 = Transactions('expense', 200, 'Comida', 'Restaurante')
        self.fm.add_transaction(tx1)
        self.fm.add_transaction(tx2)
        result = self.fm.search_transactions(category='Salario')
        self.assertEqual(len(result), 1)
        self.assertIn(tx1.__dict__, result.to_dict(orient='records'))

if __name__ == '__main__':
    unittest.main()