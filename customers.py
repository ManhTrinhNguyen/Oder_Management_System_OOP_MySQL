from database import Database

class Customer:
  def __init__(self, db):
    self.db_connector = db 
     
  def add_customer(self, name, email, address):
    query='INSERT INTO customers (name, email, address) VALUES (%s, %s, %s)'
    self.db_connector.cursor.execute(query, (name, email, address))
    self.db_connector.db.commit()
    print(f'Added {name} with Email: {email} and Address: {address} to DB')

  def view_customer(self, customer_id):
    query='SELECT * FROM customers WHERE customer_id=%s' # Select clause no need to commit db
    self.db_connector.cursor.execute(query, (customer_id,))
    customer = self.db_connector.cursor.fetchone()
    return (f'Customer ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}, Address: {customer[3]}')

  def update_customer(self, customer_id, name=None, email=None, address=None):
    query='UPDATE customers SET name=%s, email=%s, address=%s WHERE customer_id=%s'
    # Before update
    before_update_customer = self.view_customer(customer_id)
    # Updating
    self.db_connector.cursor.execute(query, (name, email, address, customer_id))   
    self.db_connector.db.commit()
    # After update
    after_update_customer = self.view_customer(customer_id)
    print(f'Updated from {before_update_customer}')
    print(f'To {after_update_customer}')

  def delete_customer(self, customer_id):
    query='DELETE FROM customers WHERE customer_id=%s'
    self.db_connector.cursor.execute(query, (customer_id,))
    self.db_connector.db.commit()

    
customer_1 = Customer(Database()) 

#customer_1.add_customer('Tim', 'Tim@gmail.com', '123st 94110')
customer_1.delete_customer(5)




