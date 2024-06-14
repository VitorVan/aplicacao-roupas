from skimage import io, color, img_as_ubyte
from rembg import remove
from io import BytesIO
from PIL import Image

def remove_bg(image_data):
    image = io.imread(image_data)
    image_no_bg = remove(image)
    if image_no_bg.shape[2] == 4:
        image_no_bg = color.rgba2rgb(image_no_bg)
    image_no_bg = img_as_ubyte(image_no_bg)
    output_buffer = BytesIO()
    image_pil = Image.fromarray(image_no_bg)
    image_pil.save(output_buffer, format='PNG')
    output_buffer.seek(0)
    return output_buffer