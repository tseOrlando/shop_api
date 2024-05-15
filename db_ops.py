from datetime import datetime
import mysql.connector
import yaml
from models import product
import csv

class essential_crud_t():

    # config login
    def __init__(self):
        db_config = yaml.safe_load(open('conf.yml', 'r'))
    
        self.peer = mysql.connector.connect(
            host=db_config['database']['host'],
            port=db_config['database']['port'],
            user=db_config['database']['user'],
            password=db_config['database']['password'],
            database=db_config['database']['name'])
        
    # once the instance gets deleted, closses connection automatically
    def __del__(self):
        if self.peer:
            self.peer.close()

    # makes json-like output prettier with their values n keys 
    def pretty(self, records, cursor): return [dict(zip([desc[0] for desc in cursor.description], row)) for row in records]

    # makes query life easier doing the same process in one function that saves instances of cursors in a less redundant way
    def operation(self, query, all_or_one = True, commit_needed = False):
        cursor = self.peer.cursor()
        cursor.execute(query)
        
        if commit_needed: self.peer.commit()
        
        return self.pretty(cursor.fetchall() if all_or_one else cursor.fetchone(), cursor) 
    
    # for ops such as insert, delete or update
    def secure_operation(self, query, operation, all_or_one=True, commit_needed=False):
        try:
            self.operation(query, all_or_one, commit_needed)
            return self.result(operation)
        except Exception as error:
            if "fetch from." not in str(error): return self.result(operation) #mierdon de error ekk
            else: return {f"{operation} operation error": error}

    # auto result for less redundant json-like code
    def result(self, operation): return {"result" : f"{operation} successfully!"}

    # gets all the info needed for a polite way of showing the categories, subcategories and products with useful info
    def get_all_global(self, stuff : str = ""): return self.operation(f"SELECT c.name AS category_name, sc.name AS subcategory_name, p.name AS product_name, p.company AS product_brand, p.price AS product_price FROM product p INNER JOIN subcategory sc ON p.subcategory_id = sc.subcategory_id INNER JOIN category c ON sc.category_id = c.category_id {stuff};")
    
    # orders by asc or desc
    def order(self, how : str): return self.get_all_global(f"ORDER BY product_name {how}")

    # contains or not
    def contains(self, word): return self.get_all_global(f"WHERE p.name LIKE '%{word}%'")

    # skip and limit
    def skip(self, skip, limit): return self.get_all_global(f" LIMIT {limit} OFFSET {skip};")

    # do i need to really explain this
    def get_all(self): return self.operation("SELECT * FROM product;")

    # ???
    def get(self, id): return self.operation(f"SELECT * FROM product WHERE product_id = {id};")

    # adds a product
    def add(self, record: product): return self.secure_operation(f"INSERT INTO product (name, description, company, price, units, subcategory_id) VALUES ('{record.name}', '{record.description}', '{record.company}', {record.price}, {record.units}, {record.subcategory_id});", "added", True, True)
    
    # deletes a product
    def delete(self, id): return self.secure_operation(f"DELETE FROM product WHERE product_id = {id};", "deleted", True, True)

    # updates a product info, with the parameters you want, just to let you know : 
    # "product_id": int,
    # "name": "value",
    # "description": "value",
    # "company": "value",
    # "price": decimal,
    # "units": int,
    # "subcategory_id": int,
    # "created_at": "datetime",
    # "updated_at": "datetime"
    def update(self, id, record_parameters : dict):
        set_clause = ", ".join([f"{key} = '{value}'" for key, value in record_parameters.items()])
        return self.secure_operation(f"UPDATE product SET {set_clause} WHERE product_id = {id};", "updated", True, True)

    #loads csv and checks if categories - subcategories - products exists
    def load_csv(self, _csv):
        now = datetime.now()
        insert = "inserted"
        update = "updated"
        result = []

        for row in csv.DictReader(open(_csv, 'r')):

            category_name = row['nom_categoria']
            category_result = self.operation(f"SELECT * FROM category WHERE name = '{category_name}'")
            category_id = row['id_categoria']

            subcategory_name = row['nom_subcategoria']
            subcategory_result = self.operation(f"SELECT * FROM subcategory WHERE name = '{subcategory_name}'")
            subcategory_id = row['id_subcategoria']

            product_name = row['nom_producto']
            product_result = self.operation(f"SELECT * FROM product WHERE name = '{product_name}'")

            if not category_result: self.secure_operation(f"INSERT INTO category (name, created_at, updated_at) VALUES ('{category_name}', '{now}', '{now}')", insert, True, True)
            else: self.secure_operation(f"UPDATE category SET name = '{category_name}', updated_at = '{now}' WHERE category_id = {category_id}", update, True, True)

            if not subcategory_result: self.secure_operation(f"INSERT INTO subcategory (name, category_id, created_at, updated_at) VALUES ('{subcategory_name}', {category_id}, '{now}', '{now}')", insert, True, True)
            else: self.secure_operation(f"UPDATE subcategory SET name = '{subcategory_name}', category_id = {category_id}, updated_at = '{now}' WHERE subcategory_id = {subcategory_id}", update, True, True)

            if not product_result: self.secure_operation(f"INSERT INTO product (name, description, company, price, units, subcategory_id, created_at, updated_at) VALUES ('{product_name}', '{row['descripcion_producto']}', '{row['companyia']}', {row['precio']}, {row['unidades']}, {subcategory_id}, '{now}', '{now}');", insert, True, True)
            else: self.secure_operation(f"UPDATE product SET name = '{product_name}', updated_at = '{now}' WHERE product_id = {row['id_producto']}", update, True, True)

            result.append({"loaded" : {"category": category_result, "subcategory" : subcategory_result, "product" : product_result}})

        return result