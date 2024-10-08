import unittest.mock
import pytest 
import sys 
from unittest.mock import patch, MagicMock 
import unittest

sys.path.insert(1, '/Users/trinhnguyen/Documents/Meta-Certificate/Database/Oder_Management_System_OOP_MySQL/')

from orders import Order
from database import Database

class Test_Order(unittest.TestCase):

  @patch('mysql.connector.connect')
  def setUp(self, mock_connect):
    # Mock connect db 
    self.mock_db = MagicMock()
    # Mock connect cursor 
    self.mock_cursor = MagicMock()

    # Mock_connect (mysql.connector.connect) will return value as mock_db
    mock_connect.return_value = self.mock_db
    # Mock_db.cursor will return self._mock_cursor 
    self.mock_db.cursor.return_value = self.mock_cursor

    # Initilize DB 
    self.order = Order(Database())

  def test_create_order(self):
    # Customer Id 
    customer_id = 1
    
    product= {
      1: 2, # product_id: quantity 
      2: 1
    }

    # Mock last row id
    self.mock_cursor.lastrowid = 101

    # Mock product select query and results (price, stocks)
    self.mock_cursor.fetchone.side_effect = [(10.0, 5), (20.0, 3)] # First product, second product

    # Call the method 
    self.order.create_order(customer_id, product)

    # Assertion 
    self.mock_cursor.execute.assert_any_call('INSERT INTO orders (customer_id) VALUES (%s)', (customer_id,))
    self.mock_cursor.execute.assert_any_call('SELECT price, stock FROM products WHERE product_id=%s', (1,))
    self.mock_cursor.execute.assert_any_call('SELECT price, stock FROM products WHERE product_id=%s', (2,))
    self.mock_cursor.execute.assert_any_call(
      'INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)',
      (101, 1, 2, 10.0)
    )
    self.mock_cursor.execute.assert_any_call(
      'UPDATE products SET stock=%s WHERE product_id=%s', 
      (3, 1)
    )
    self.mock_db.commit.assert_called_once()




