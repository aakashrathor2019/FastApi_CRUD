from fastapi import FastAPI, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import ResponseMessage, Product
from pymongo import MongoClient
from bson import ObjectId


client = MongoClient("mongodb://localhost:27017")
db = client['product_management']
product_colletions = db['products']

app = FastAPI()

app.mount("/static", StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='template')
@app.get("/", response_class=HTMLResponse)
async def read(request: Request):
    result = list(product_colletions.find())
    print("ALl Data:",result)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "Data": result}
    )

@app.post("/add_data", response_model=ResponseMessage) 
async def add(data: Product): 
    result = product_colletions.insert_one(data.dict()) 
    return { "message": "Success", "data": { "id": str(result.inserted_id), "name": data.name, "price": data.price } }

@app.get("/get_one/{id}")
async def find_one(id: str):
    result = product_colletions.find_one({"id": id})
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    result["_id"] = str(result["_id"])
    return result

@app.put('/update/{id}',response_model=Product)
async def update(id:str, data:Product):
    result = product_colletions.update_one({'id':id},{'$set':data.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail='Not found')
    udpated_data = product_colletions.find_one({'id':id})
    return {'id':udpated_data['id'], 'name': udpated_data['name'], 'price': udpated_data['price']}

@app.delete('/delete/{id}')
async def delete(id:str):
    result = product_colletions.delete_one({'id':id})
    print("Result :", result)
    if not result:
        raise HTTPException(status_code=404, detail='Not found')
        
    return {"message": "Product deleted successfully"}

@app.post('/upload/')
async def uploadfile(files : UploadFile):
    try:
        for file in files:
            file_path = f"/home/my/Documents/{file.filename}"
            with open (file_path, 'wb') as f:
                f.write(file.file.read())
                return {'message': 'file saved successfully'}
    except Exception as e:
        return {'message': e.args}