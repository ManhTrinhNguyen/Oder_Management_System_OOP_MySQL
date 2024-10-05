import unittest.mock
import pytest 
import sys 
from unittest.mock import patch, MagicMock 
import unittest

sys.path.insert(1, '/Users/trinhnguyen/Documents/Meta-Certificate/Database/Oder_Management_System_OOP_MySQL/')

from products import Product
from database import Database 

class Test_Product(unittest.TestCase): 
  # Setup test run at the begginning of each test
  @patch('mysql.connector.connect')
  def setUp(self, mock_connect): # mock_connect is arg as the mysq.connector.connect
    # Mock DB connection 
    self.mock_db = MagicMock()
    # Mocl Cursor 
    self.mock_db_cursor = MagicMock()

    # Mock connect(mysql.connector.connect) will return value of  mock_db 
    mock_connect.return_value = self.mock_db

    # Mock_db cursor will return value of mock_db_Cursor 
    self.mock_db.cursor.return_value = self.mock_db_cursor
    
    # Initialize the database . Now it will run with mock mysql.connector.connect instead if real one 
    self.product=Product(Database())

  def test_add_product(self): 
    # Call method want to test 
    self.product.add_product('Iphone14', 'New', 1000, 10)

    # Assert that SQL executed correctly 
    self.mock_db_cursor.execute.assert_called_with(
      'INSERT INTO products (name, description, price, stock) VALUES (%s, %s, %s, %s)',
      ('Iphone14', 'New', 1000, 10)
      )
    #Assert that the commit was call once 
    self.mock_db.commit.assert_called_once()

  def test_update_product_price(self):
    # Call method want to test
    self.product.update_product_price(1, 1000)

    # Assert that Select query run correctly 
    select_call = unittest.mock.call(
      'Select price FROM products WHERE product_id=%s',
      (1,)
    )

    # Assert that Update query run correcly 
    update_call = unittest.mock.call(
      'UPDATE products SET price=%s WHERE product_id=%s',
      (1000, 1)
    )

    # Assert both call (update and select) were made 
    self.mock_db_cursor.execute.assert_has_calls([select_call, update_call], any_order=True)

    # Assert commit were called
    self.mock_db.commit.assert_called()

  def test_update_product_stock(self):
    # Call method want to test
    self.product.update_product_stock(1, 20)

    # Assert that Select query run correctly 
    select_call = unittest.mock.call(
      'Select stock FROM products WHERE product_id=%s',
      (1,)
    )

    # Assert that Update query run correctly 
    update_call = unittest.mock.call(
      'UPDATE products SET stock=%s WHERE product_id=%s',
      (20, 1)
    )

    # Assert both call (update and select) were made 
    self.mock_db_cursor.execute.assert_has_calls([select_call, update_call], any_order=True)

    # Assert commit were called
    self.mock_db.commit.assert_called()

  def test_remove_product(self):
    # Call method want to test 
    self.product.remove_product(1)

    # Assert that Delete query run correctly 
    self.mock_db_cursor.execute.assert_called_with(
      'DELETE FROM products WHERE product_id=%s',
      (1,)
    )
    
    # Assert commit made 
    self.mock_db.commit.assert_called()
