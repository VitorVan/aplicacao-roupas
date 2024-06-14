import os
import shutil
import uuid
import time
from io import BytesIO 
import uvicorn
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from services.background_removal import remove_bg
from services.extract_features import extract_features

from getSimilarClothes import getSimilarClothes


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://192.168.1.110:5173"
]

@app.get("/")
async def root():
  return {"message": "Hello World"}

@app.post("/upload")
def postUploadHandler(file: UploadFile):
    print(file.filename)
    if not file.filename.endswith(".png") and not file.filename.endswith(".jpg") and not file.filename.endswith(".jpeg"):
        raise HTTPException(status_code=401, detail="Arquivo deve estar em .png, .jpg ou .jpeg")

    # Ler o arquivo para memória
    image_data = file.file.read()

    # Remover o fundo da imagem
    image_no_bg = remove_bg(BytesIO(image_data))

    # Extrair as características da imagem sem fundo
    features = extract_features(image_no_bg)

    # Salvar a imagem sem fundo em um caminho temporário
    image_no_bg_path = f"photos/temp_{uuid.uuid4()}.png"
    with open(image_no_bg_path, "wb") as buffer:
        buffer.write(image_no_bg.getvalue())

    return {"features": features.tolist()}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run("app:app", host="localhost",port=20412, reload=True)