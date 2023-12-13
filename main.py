from fastapi import FastAPI, Query,Path,Body
#including specific types 
from enum import Enum
from typing import Optional
from pydantic import BaseModel

# JSONify the output of post requests
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


#create app instance 
app = FastAPI()


# A post request will have to contain the following fields with the following data types, this is a pydantic model
# What must a post req contain is declared in the pydantic model
#declare BaseModel
class Item(BaseModel):
    name:str
    discription:Optional[str]=None
    price:float
    tax:float | None = None

# Our Database as of now stored in a dictionary
fake_items_db =[{"item_name": "item1"}, {"item_description": "item1 description"},
                {"item_name": "item2"}, {"item_description": "item2 description"},
                {"item_name": "item3"}, {"item_description": "item3 description"},
                {"item_name": "item4"}, {"item_description": "item4 description"},
                {"item_name": "item5"}, {"item_description": "item5 description"}
                ]




#create routes

#routes related to posts
#get post for some ID
@app.get("/posts/{id}")
def get_post_by_id(id: int):
    return {"message": f"This is get post by id route with current id: {id}"}


@app.delete("/delete/{id}")
def delete_post(id: int):
    return {"message": f"This is delete route for id: {id}".format(id)}

#routes related to user information

# get all users
@app.get("/all_users")
def get_all_user():
    return {"message": "This is gets all users route"}

@app.post("/user/{id}")
def get_user_by_id(id: int):
    return {"message": f"This is get user by id route with current id: {id}"}

@app.get("/user/me")
def get_current_user():
    return {"message": f"This is get current user with {id} route"}


# get all items

@app.get("/all-items",response_class=JSONResponse)
def get_all_items(skip:int=0, limit:int=10):
        return JSONResponse(fake_items_db[skip: skip+limit])

    
@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    return JSONResponse(content=json_compatible_item_data)


# get item rate including taxes
@app.post("/item")
def create_item(item: Item):
    item_rate = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_rate.update({"price_with_tax":price_with_tax})
    return item_rate


#Passing numeric query parameters
@app.get("/items_validation{item_id}")
def get_item_validation(*,item_id: int=Path(..., title="The ID to get"), 
                        q:str, size: float=Query(..., gt=0, lt=7.75)
):
        results={"item_id": item_id, "size":size}
        if q:
            results.update({"q": q},**results)
        return results
    
# Passing Multiple query parameters

@app.put("/new_items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(..., title="The ID to update"),
    tax: Optional[float] = None,
    item: Item | None = None,
    q: str | None = None
):
    results = {"item_id": item_id}

    if q:
        results |= {"q": q}

    if item:
        results["item"] = item

    if tax is not None:
        results["tax"] = tax

    return results



class Item(BaseModel):
    name:str
    
    
@app.put("/new_items/{item_id}")
def update_item(item_id:int, item:Item=Body(..., embed=True)):
    return {"item_id": item_id,"item":item}
    