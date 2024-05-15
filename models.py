
from pydantic import BaseModel
from datetime import datetime

#model of product (barely used but useful to centralize data structures for the api)

class product(BaseModel):
    id : int
    name : str
    description : str
    company : str
    price : int
    units : int
    subcategory_id : int
    created_at : datetime