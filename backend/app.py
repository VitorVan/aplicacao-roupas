from array import array
import os
import shutil
import uuid
import time
from io import BytesIO 
from skimage import io, color, measure, filters, exposure, img_as_ubyte
from PIL import Image
import uvicorn
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from services.background_removal import remove_bg
from services.extract_features import extract_features
from services.extract_features_clip import create_clip_embedding

from services.database import add_clothes_to_index, get_similar_clothes
from services.database_clip import add_clothes_to_clip_index, get_similar_clip_clothes

# Initialize FastAPI
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
    image = io.imread(image_no_bg)
    features = extract_features(image)


    # Salvar a imagem sem fundo em um caminho temporário
    # image_no_bg_path = f"photos/temp_{uuid.uuid4()}.jpg"
    # with open(image_no_bg_path, "wb") as buffer:
    #     shutil.copyfileobj(image_data, buffer)
    generatedUuid = str(uuid.uuid4())

    file_path = f"photos/{generatedUuid + os.path.splitext(file.filename)[1]}"

    with open(file_path, "wb") as buffer:
        output = Image.fromarray(image)
        output.save(buffer, format="JPEG")
   

    print(len(features))

    similar = get_similar_clothes(features.tolist())

    response = []

    for item in similar:
        response.append({
            "id": item.id,
            "score": item.score,
            "metadata": item.metadata
        })
    
    return {"similarItems": response}


@app.post("/add")
def postUploadHandler(file: UploadFile):
    print(file.filename)
    if not file.filename.endswith(".png") and not file.filename.endswith(".jpg") and not file.filename.endswith(".jpeg"):
        raise HTTPException(status_code=401, detail="Arquivo deve estar em .png, .jpg ou .jpeg")
    
    # Ler o arquivo para memória
    image_data = file.file.read()

    # Remover o fundo da imagem
    image_no_bg = remove_bg(BytesIO(image_data))

    # Extrair as características da imagem sem fundo
    image = io.imread(image_no_bg)
    features = extract_features(image)

    generatedUuid = str(uuid.uuid4())

    file_path = f"../frontend/public/clothes/{generatedUuid + os.path.splitext(file.filename)[1]}"

    with open(file_path, "wb") as buffer:
        output = Image.fromarray(image)
        output.save(buffer, format="JPEG")
   

    print(len(features))

    data = [(generatedUuid, features, {
        'fileName': generatedUuid + os.path.splitext(file.filename)[1]
    })]

    add_clothes_to_index(data)

    return {"message": "Item adicionado com sucesso"}



@app.post("/clipadd")
def postUploadHandler(file: UploadFile):
    print(file.filename)
    if not file.filename.endswith(".png") and not file.filename.endswith(".jpg") and not file.filename.endswith(".jpeg"):
        raise HTTPException(status_code=401, detail="Arquivo deve estar em .png, .jpg ou .jpeg")
    
    # Ler o arquivo para memória
    image_data = file.file.read()

    # Remover o fundo da imagem
    image_no_bg = remove_bg(BytesIO(image_data))

    # Extrair as características da imagem sem fundo
    image = io.imread(image_no_bg)
    embedding = create_clip_embedding(image)

    print(len(embedding[0]))


    generatedUuid = str(uuid.uuid4())

    file_path = f"../frontend/public/clothes/{generatedUuid + os.path.splitext(file.filename)[1]}"

    with open(file_path, "wb") as buffer:
        output = Image.fromarray(image)
        output.save(buffer, format="JPEG")

    data = [(generatedUuid, embedding[0], {
        'fileName': generatedUuid + os.path.splitext(file.filename)[1]
    })]

    add_clothes_to_clip_index(data)

    return {"message": "Item adicionado com sucesso"}


@app.post("/clipupload")
def postUploadHandler(file: UploadFile):
    print(file.filename)
    if not file.filename.endswith(".png") and not file.filename.endswith(".jpg") and not file.filename.endswith(".jpeg"):
        raise HTTPException(status_code=401, detail="Arquivo deve estar em .png, .jpg ou .jpeg")
    
    # Ler o arquivo para memória
    image_data = file.file.read()

    # Remover o fundo da imagem
    image_no_bg = remove_bg(BytesIO(image_data))

    # Extrair as características da imagem sem fundo
    image = io.imread(image_no_bg)
    embedding = create_clip_embedding(image)

    print(len(embedding[0]))

    similar = get_similar_clip_clothes(embedding[0].tolist())

    response = []

    for item in similar:
        response.append({
            "id": item.id,
            "score": item.score,
            "metadata": item.metadata
        })
    
    return {"similarItems": response}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run("app:app", host="localhost",port=20412, reload=True)