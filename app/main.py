from fastapi import FastAPI

# define the server url (excl. hostname:port)
# srvurl = "/testapi/v1"
srvurl = ""

# basic information
app = FastAPI(
    title="FastAPI template project",
    descriptions=(
        "This is a FastAPI boilerplate. "
        "Please adjust it to your needs. "),
    version="0.1.0",
    openapi_url=f"{srvurl}/openapi.json",
    docs_url=f"{srvurl}/docs",
    redoc_url=f"{srvurl}/redoc"
)


# specify the endpoints
@app.get(f"{srvurl}/")
def read_root():
    return {"msg": "Hello World"}


@app.get(f"{srvurl}/items/")
async def read_items_null():
    return {"item_id": None}


@app.get(srvurl + "/items/{item_id}")
async def read_items(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
