
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
from skimage import io as skio

def postUploadHandler(directory_path: str):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        if not filename.endswith(".png") and not filename.endswith(".jpg") and not filename.endswith(".jpeg"):
            raise HTTPException(status_code=401, detail="Arquivo deve estar em .png, .jpg ou .jpeg")
        
        # Ler o arquivo para memória
        with open(file_path, "rb") as file:
            image_data = file.read()

        # Remover o fundo da imagem
        image_no_bg = remove_bg(BytesIO(image_data))

        # Extrair as características da imagem sem fundo
        image = skio.imread(image_no_bg)
        embedding = create_clip_embedding(image)

        print(len(embedding[0]))

        generatedUuid = str(uuid.uuid4())

        save_path = f"../frontend/public/clothes/{generatedUuid + os.path.splitext(filename)[1]}"

        with open(save_path, "wb") as buffer:
            output = Image.fromarray(image)
            output.save(buffer, format="JPEG")

        data = [(generatedUuid, embedding[0], {
            'fileName': generatedUuid + os.path.splitext(filename)[1]
        })]

        print(data)

        add_clothes_to_clip_index(data)

    return {"message": "Items adicionados com sucesso"}


postUploadHandler('photos')