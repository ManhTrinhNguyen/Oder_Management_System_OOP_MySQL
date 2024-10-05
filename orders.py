from database import Database

class Order:
  def __init__(self, db) -> None:
    self.db_connector = db 

  # Create Order 
  def create_order(self, customer_id, products):
    try:
      # Start Transaction
      query_insert_order='INSERT INTO orders (customer_id) VALUES (%s)'
      self.db_connector.cursor.execute(query_insert_order, (customer_id,)) # Insert customer_id the customer that want to order 
      order_id = self.db_connector.cursor.lastrowid # Take last id just insert (lastrowid)

      # Add each product to order_item and update stock 
      for product_id, quantity in products.items():
        query_select_product='SELECT price, stock FROM products WHERE product_id=%s'
        self.db_connector.cursor.execute(query_select_product, (product_id,))
        product = self.db_connector.cursor.fetchone()
        
        if product[1] < quantity: 
          raise Exception(f'Insufficient stock for product {product_id}')
        
        # Insert into order_items
        query_insert_order_items='INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)'
        self.db_connector.cursor.execute(query_insert_order_items, (order_id, product_id, quantity, product[0]))

        # Update stock
        new_stock = product[1] - quantity
        query_update_new_stock='UPDATE products SET stock=%s WHERE product_id=%s'
        self.db_connector.cursor.execute(query_update_new_stock, (new_stock, product_id))
      # Commit transaction
      self.db_connector.db.commit()
      print(f"Order {order_id} created successfully.")
    except Exception as e:
      self.db_connector.db.rollback()
      raise e
    
  def view_orders(self):
    query='SELECT * FROM orders'
    self.db_connector.cursor.execute(query)
    order = (self.db_connector.cursor.fetchone())
    return f'Order_id: {order[0]}, Customer_id: {order[1]}, Datetime: {order[2]}'

    

order_1 = Order(Database())
#order_1.create_order(customer_id=6, products={2:10})
order_1.create_order(customer_id=6, products={2: 5, 4: 5})
print(order_1.view_orders())