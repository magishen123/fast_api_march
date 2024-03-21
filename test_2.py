from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

items = {
    1: {"id": 1, "title": "QWE", "description": "ABC", "category": "A", "price": 10, "discount": 1, "quantity": 5},
    2: {"id": 2, "title": "EWQ", "description": "ABC", "category": "A", "price": 10, "discount": 1, "quantity": 3}
}

# Модель данных для товара
class Item(BaseModel):
    id: int
    title: str
    description: str
    category: str
    price: float
    discount: Optional[float]
    quantity: int

# Эндпоинт для получения списка товаров
@app.get("/items", response_model=List[Item])
def get_items():
    return list(items.values())

# Эндпоинт для получения информации о товаре по id
@app.get("/items/{id}", response_model=Item)
def get_item(id: int):
    if id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[id]

# Эндпоинт для добавления нового товара
@app.post("/items", response_model=Item)
def add_item(item: Item):
    new_id = max(items.keys()) + 1 if items else 1
    items[new_id] = item.dict()
    return items[new_id]

# Обновление информации о товаре по его id используя тело запроса
@app.put("/items/{id}", response_model=Item)
def update_item(id: int, item: Item):
    if id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[id] = item.dict()
    return items[id]

# Удаление информации о товаре по id
@app.delete("/items/{id}")
def delete_item(id: int):
    if id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[id]
    return {"message": "Item deleted"}

# Фильтрация списка товаров по заданным параметрам
@app.get("/items/filter/")
def filter_items(title: Optional[str] = None, description: Optional[str] = None, category: Optional[str] = None,
                 price_from: Optional[float] = None, price_to: Optional[float] = None,
                 quantity_from: Optional[int] = None, quantity_to: Optional[int] = None,
                 discount_from: Optional[float] = None, discount_to: Optional[float] = None):
    
    filtered_items = []
    
    for item in items.values():
        if (title is None or title.lower() in item["title"].lower()) and \
           (description is None or description.lower() in item["description"].lower()) and \
           (category is None or category == item["category"]) and \
           (price_from is None or item["price"] >= price_from) and \
           (price_to is None or item["price"] <= price_to) and \
           (quantity_from is None or item["quantity"] >= quantity_from) and \
           (quantity_to is None or item["quantity"] <= quantity_to) and \
           (discount_from is None or item["discount"] is not None and item["discount"] >= discount_from) and \
           (discount_to is None or item["discount"] is not None and item["discount"] <= discount_to):
            filtered_items.append(item)
    
    return filtered_items
