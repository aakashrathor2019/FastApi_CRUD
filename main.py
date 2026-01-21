from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

products = []
class Product(BaseModel):
    id : int
    name: str
    age : int

class ResponseMessage(BaseModel):
    message: str
    data: Product

app.mount("/static", StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='template')
@app.get("/",response_class=HTMLResponse)
async def read(request : Request):
    return templates.TemplateResponse("index.html",{"request":request, "message": "Hello from Static"})

@app.post("/add_data", response_model=ResponseMessage)
async def add(data: Product):
    products.append(data)
    print('Products :', products)
    return {'message': 'Success', 'data': data}

@app.get('/get_one/{id}',response_model= Product)
def find_one(id : int):
    for p in products:
        if p.id == id:
            return p
    raise HTTPException(status_code=404, detail="Not found")

@app.put('/update/{id}', response_model=Product)
def update(id:int, data:Product):
    for index, p in enumerate(products):
        if p.id == id:
            data.id  = id
            products[index] = data
            return data
    raise HTTPException(status_code=404,detail='Not found')

@app.delete('/delete/{id}', response_model=Product)
def delete(id:int):
    for index, p in enumerate(products):
        if p.id == id:
            return products.pop(index)
    raise HTTPException(status_code=404, detail='Not found')

