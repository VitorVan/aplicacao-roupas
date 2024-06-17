import clip
import torch
from PIL import Image
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def create_clip_embedding(image):
    if isinstance(image, np.ndarray):
        # If image is a NumPy array, convert it to PIL Image
        image = Image.fromarray(image)
    elif not isinstance(image, Image.Image):
        raise TypeError("Image must be a PIL Image or a NumPy array")

    # Preprocess the image
    image = preprocess(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        image_embeddings = model.encode_image(image)
        return image_embeddings.cpu().numpy()
