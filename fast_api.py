from fastapi import FastAPI
from db_ops import essential_crud_t
from models import product

#waoow api !11!!1!

app = FastAPI()
op_handler = essential_crud_t()

@app.get("/products")
def get_products(): return op_handler.get_all()

@app.get("/category_feed")
def get_product_feed(): return op_handler.get_all_global()

@app.get("/category_feed_ordered_")
def get_product_ordered_by(by : str = "asc"): return op_handler.order(by)

@app.get("/category_feed_that_")
def get_product_that_contains(contains : str = "peo"): return op_handler.contains(contains)

@app.get("/category_feed_that_skips")
def get_product_that_skips(skip : str = "0",limit : str = "10"): return op_handler.skip(skip, limit)

@app.get("/product/{product_id}")
def get_product(id): return op_handler.get(id)

@app.post("/product")
def add_product(product : product): return op_handler.add(product)

@app.post("/load_product")
def load_product(csv): return op_handler.load_csv(csv)

@app.put("/product")
def update_product(id, record_parameters : dict): return op_handler.update(id, record_parameters)

@app.delete("/product")
def delete_product(id): return op_handler.delete(id)