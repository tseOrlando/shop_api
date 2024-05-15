# Essential CRUD Operations Tool (essential_crud_t)

This Python module provides essential CRUD (Create, Read, Update, Delete) operations for interacting with a MySQL database. It includes methods for performing various database operations such as querying, inserting, updating, and deleting records from the database.

# Before everything...
- Execute this queries in your own shop database in order to get the tables done correctly! 
```bash
CREATE TABLE category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE subcategory (
    subcategory_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);

CREATE TABLE product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    company VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    units INT,
    subcategory_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (subcategory_id) REFERENCES subcategory(subcategory_id)
);

```

# Installation
- Clone the repository:

```bash
git clone https://github.com/tseOrlando/shop_api.git
```

- Install the required dependencies:

```bash
pip install mysql-connector-python pyyaml fastapi pydantic
```
## Usage
- Import the necessary modules and classes:

```python
from datetime import datetime
import mysql.connector
import yaml
import csv
from models import product
from db_ops import essential_crud_t
```

- Initialize an instance of the essential_crud_t class:

```python
op_handler = essential_crud_t()
```
- Use the provided methods to interact with the database:

```python
# Example: Retrieve all products
products = op_handler.get_all()
```
# Class Methods
- get_all: Retrieves all products from the database.
- get_all_global: Retrieves information about categories, 
subcategories, and products.

- order: Orders products by name in ascending or descending order.
- contains: Retrieves products that contain a specific keyword in their name.
- skip: Skips a certain number of records and limits the number of returned records.
- get: Retrieves a product by its ID.
- add: Adds a new product to the database.
- delete: Deletes a product from the database.
- update: Updates information for a specific product.

## Dependencies

- mysql-connector-python: MySQL database connector.

- pyyaml: YAML parser for reading configuration files.
- fastapi: Web framework for building APIs.
- pydantic: Data validation and settings management using Python type annotations.

## Configuration
The database connection details are stored in a YAML configuration file named conf.yml. Ensure that this file is present and contains the necessary information for connecting to your MySQL database.

## Models
The product model class, defined in the models.py module, represents the structure of a product. It includes attributes such as ID, name, description, company, price, units, subcategory ID, and creation date.

API Endpoints
This module also provides several FastAPI endpoints for interacting with the database through HTTP requests:

- /products: Retrieves all products.
- /category_feed: Retrieves information about categories, subcategories, and products.
- /category_feed_ordered_: Retrieves products ordered by name in ascending or descending order.
- /category_feed_that_: Retrieves products that contain a specific keyword in their name.
- /category_feed_that_skips: Retrieves a subset of products, skipping a certain number of records and limiting the number of returned records.

- /product/{product_id}: Retrieves a product by its ID.
- /product: Adds a new product to the database.
- /load_product: Loads products from a CSV file into the database.
- /product: Updates information for a specific product.
- /product: Deletes a product from the database.

# IMPORTANT

This README provides an overview of the essential CRUD operations tool, including installation instructions, usage examples, class methods, dependencies, configuration details, models, and API endpoints. Use this tool to perform CRUD operations on your MySQL database with ease.
