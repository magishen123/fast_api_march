# Импорт всего чего только можно 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

items = {
    1: {"id": "1", "title": "QWE", "description": "ABC", "category": "A", "price": 10 , "discount": 1 , "quantity": "A"},
    2: {"id": "1", "title": "EWQ", "description": "ABC", "category": "A", "price": 10 , "discount": 1 , "quantity": "A"} 

}
#items = {}
# Модель данных для товара
class Item(BaseModel):
    id: int
    title: str
    description: str
    category: str
    price: float
    discount: float | None
    quantity: int

# База данных товаров (здесь представлена просто как список)
inventory = []

# Эндпоинт для получения списка товаров
@app.get("/items", response_model=List[Item])
def get_items():
    return inventory

# Эндпоинт для получения информации о товаре по id
@app.get("/items/{id}", response_model=Item)
def get_item(id: int):
    for item in inventory:
        if item.id == id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Эндпоинт для добавления нового товара
@app.post("/items", response_model=Item)
def add_item(item: Item):
    new_id = max(items.keys()) + 1 if items else 1
    items[new_id] = items.dict()
    return {"id": new_id, **item.dict()}
    #inventory.append(item)
    #return item

# Обновление информации о товаре по его id используя тело запроса
@app.put("/items/{id}")
async def update_item(id: int, item: Item):
    if id not in items:
        raise HTTPException(status_code=404, detail="Film not found")
    items[id] = item.dict()
    return items[id]

# Удаление информации о фильме по id
@app.delete("/items/{id}")
async def delete_film(id: int):
    if id not in items:
        raise HTTPException(status_code=404, detail="Film not found")
    del items[id]
    return {"message": "Film deleted"}

# Фильтрация списка фильмов по заданным параметрам-----------------
@app.get("/films/filter")
async def filter_items(id: int, title: Optional[str] = None, description: Optional[str] = None, category: Optional[str] = None, price: Optional[float] = None, discount: Optional[float] = None, quantity: Optional[str] = None):
    filtered_items = []
    for item_id, item_data in items.items():
        if (id is None or item_data["id"] == id) and \
           (category is None or item_data["category"] == category) and \
           (price is None or item_data["price"] == price) and \
           (discount is None or item_data["discount"] == discount) and \
           (quantity is None or item_data["quantity"] == quantity) and \
           (description is None or item_data["description"] == description) and \
           (title is None or title.lower() in item_data["title"].lower()):
            filtered_items.append({item_id: item_data})
    return filtered_items


# Эндпоинт для продажи одного или нескольких товаров
@app.get("/sale/")
def sell_items(id: List[int]):
    sold_items = []
    for item_id in id:
        item_found = False
        for item in inventory:
            if item.id == item_id:
                item_found = True
                if item.quantity > 0:
                    item.quantity -= 1
                    sold_items.append(item)
                else:
                    return {"message": "Insufficient quantity", "items": [item]}
        if not item_found:
            raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item sold", "items": sold_items}



# Эндпоинт для увеличения количества единицы на складе
@app.get("/increment/")
def increment_items(id: List[int], quantity: List[int]):
    updated_items = []
    for i in range(len(id)):
        item_found = False
        for item in inventory:
            if item.id == id[i]:
                item_found = True
                item.quantity += quantity[i]
                updated_items.append(item)
        if not item_found:
            raise HTTPException(status_code=404, detail="Item not found")
    return updated_items
# Пример запуска приложения
#import uvicorn
#uvicorn.run(app, host="127.0.0.1", port=8000)