import os
import shutil
import uuid
import time
import uvicorn
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware

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
  

  generatedUuid = str(uuid.uuid4())
  file_path = f"photos/{generatedUuid + os.path.splitext(file.filename)[1]}"

  with open(file_path, "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)
  
  start_time = time.time()
  similarClothes = getSimilarClothes(file_path)
  print(similarClothes)
  end_time = time.time()
  elapsed_time = end_time - start_time
  elapsed_time = round(elapsed_time)
  print(f"Time taken: {elapsed_time}")
  
  return {"similarClothes": similarClothes}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run("app:app", host="localhost",port=20412, reload=True)