from fastapi import FastAPI
import uvicorn
from enum import Enum
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def route1() -> dict:
    return {'message' : 'Response from route 1 API'}

@app.get('/fruit/{fruit_name}')
async def route2(fruit_name:str) -> dict:
    return {'message' : f"Fruit name is {fruit_name}"}

@app.get('/age/{age}')
async def route3(age:int) -> dict:
    return {'message' : f"Age is {age}"}

class ModelName(str,Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model1(model_name: ModelName) -> dict:
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name is ModelName.lenet:
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/files/{file_path:path}")
async def read_file(file_path) -> dict:
    return {"file_path" : file_path}

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.get("/paths/")
async def read_mandatory_path(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items_post/")
async def create_item(body: Item):
    '''
    Hello fuunction
    '''
    if body.tax is not None:
        body.tax = round(body.price+body.tax,2)
    body.price = round(body.price,2)
    return body

# @app.put("/items_body_and_path/{item_id}")
# async def update_item(item_id: int, body: Item):
#     return {"item_id": item_id, **body.dict()}

# @app.put("/items_body_and_query_path/{item_id}")
# async def update_item_query_path_string(item_id: int, body: Item, module:str|None=None):
#     return {"item_id": item_id,"module":module, **body.dict()} # ** to unpack items of any dict

class User(BaseModel):
    username: str
    full_name: str | None = None

from typing import Annotated
from fastapi import Body, FastAPI

# @app.put("/items_two_body_class/{item_id}")
# async def update_item_to_bodies(
#     item_id: int, item: Item, user: User, importance: Annotated[int, Body()] = 5
# ):
#     results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
#     '''
#     body_example =
#                     {
#                     "item": {
#                         "name": "Foo",
#                         "description": "The pretender",
#                         "price": 42.0,
#                         "tax": 3.2
#                     },
#                     "user": {
#                         "username": "dave",
#                         "full_name": "Dave Grohl"
#                     },
#                     "importance": 8
#                     }
#     '''
#     return results

@app.get("/items_update_q_if_present/")
async def read_items_if_present_query(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results = {**results,"q":q}
    return results

from fastapi import FastAPI, Query
@app.get("/items_query_length_not_exceed_limit/")
async def read_items_within_limit_of_query(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results = {**results,"q":q}
    return results

# @app.get("/items_using_ellipsis_to_make_query_mandatory/")
# async def read_items_uisng_ellipsis(q: Annotated[str, Query(min_length=3)] = ...):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results = {**results,"q":q}
#     return results


@app.get("/items_list_of_multiple_item_as_parameter/")
async def read_items_list_of_items(q: Annotated[list[str] | None, Query()] = None):
    '''
    query_params = ?q=foo&q=bar
    '''
    query_items = {"q": q}
    return query_items

@app.get("/items_read_items_list_of_default_items_/")
async def read_items_list_of_default_items_(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items


@app.get("/items_title_desc/")
async def read_items_items_title_desc(
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results = {**results,"q":q}
    return results

from fastapi import FastAPI, Path
@app.get("/items_using_kwargs_parameters/{item_id}")
async def read_items_items_using_kwargs_parameters(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"item_id": item_id}
    if q:
        results = {**results,"q":q}
    return results

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)], q: str
):
    '''
    gt: greater than
    le: less than or equal
    ge: greater than or equal
    lt: less than
    '''
    results = {"item_id": item_id}
    if q:
        results = {**results,"q":q}
    return results





# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8001)
# uvicorn main2:app --reload --host 0.0.0.0 --port 8001 & uvicorn main2:app --reload --host 0.0.0.0 --port 8002

