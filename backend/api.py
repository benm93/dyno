from typing import Union, Annotated

from fastapi import FastAPI, UploadFile, File

from algorithms import Sequences, DynoLibrary

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/search/{target}/{distance}")
def read_item(target: str, distance: int):
    # DynoLibrary.search(None, target, distance)
    s = DynoLibrary.instance
    # return {"target": target, "distance": distance}
    
    results = DynoLibrary.search(s, target, distance)

    return results

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    file_string = file.file.read()
    s = Sequences(file_string)
    DynoLibrary.set_instance(s)
    return file_string