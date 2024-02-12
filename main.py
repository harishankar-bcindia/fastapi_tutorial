from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root1():
    return {"Message": "Hello Harishankar"}

@app.post("/fruit/{fruit_name}")
def read_root2():
    return {"Message": f"Hello Harishankar, your favourite fruit is {fruit_name}"}
