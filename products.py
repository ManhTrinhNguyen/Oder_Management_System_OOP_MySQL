from database import Database

class Product: 
  def __init__(self, db) -> None:
    self.db_connector = db

  def add_product(self, name, description, price, stock):
    query='INSERT INTO products (name, description, price, stock) VALUES (%s, %s, %s, %s)'
    self.db_connector.cursor.execute(query, (name, description, price, stock))
    self.db_connector.db.commit()
    print(f'Added Product: {name}, Description: {description}, Price: {price} ,Stock: {stock}')

  def update_product_price(self, product_id, price):
    # Price Before Update 
    query_1 ='Select price FROM products WHERE product_id=%s'
    self.db_connector.cursor.execute(query_1, (product_id,))
    price_before_update = self.db_connector.cursor.fetchone()[0]
    
    # Price After Update
    query_2='UPDATE products SET price=%s WHERE product_id=%s'
    self.db_connector.cursor.execute(query_2, (price, product_id))
    self.db_connector.db.commit()
    print(f'Update Price from {price_before_update}')
    print(f'To {price}')

  def update_product_stock(self, product_id, stock):
    # Stock Before Update 
    query_1 ='Select stock FROM products WHERE product_id=%s'
    self.db_connector.cursor.execute(query_1, (product_id,))
    stock_before_update = self.db_connector.cursor.fetchone()[0]
    print(stock_before_update)

    # Stock After Update
    query_2='UPDATE products SET stock=%s WHERE product_id=%s'
    self.db_connector.cursor.execute(query_2, (stock, product_id))
    self.db_connector.db.commit()
    print(f'Update Stock from {stock_before_update}')
    print(f'To {stock}')

  def remove_product(self, product_id):
    query='DELETE FROM products WHERE product_id=%s'
    self.db_connector.cursor.execute(query, (product_id,))
    self.db_connector.db.commit()
    print(f'Removed product with ID: {product_id}')

product_1 = Product(Database())

#product_1.add_product('Iphone 16 Pro Max', 'Newest Iphone', 2000, 20)
#product_1.remove_product(1)