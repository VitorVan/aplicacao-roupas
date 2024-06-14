import numpy as np
import cv2
from skimage import io, color, measure, filters, exposure, img_as_ubyte
from skimage.feature import local_binary_pattern, graycomatrix, graycoprops
from rembg import remove
from io import BytesIO
from PIL import Image
from scipy.spatial import distance, cKDTree
from sklearn.preprocessing import StandardScaler

def calculate_compactness(binary_image, largest_contour, perimeter):
    moments = measure.moments_central(binary_image, contour=largest_contour)
    area = moments[0, 0]
    compactness = (perimeter ** 2) / area
    return compactness

def calculate_compactness_normalized(binary_image, largest_contour, perimeter):
    moments = measure.moments_central(binary_image, contour=largest_contour)
    area = moments[0, 0]
    image_height, image_width = binary_image.shape
    image_area = image_height * image_width
    compactness = (perimeter ** 2) / (area / image_area)
    return compactness

def calculate_rectangularity(binary_image, largest_contour):
    moments = measure.moments_central(binary_image, contour=largest_contour)
    area = moments[0, 0]
    min_row, max_row, min_col, max_col = np.min(largest_contour[:, 0]), np.max(largest_contour[:, 0]), \
                                          np.min(largest_contour[:, 1]), np.max(largest_contour[:, 1])
    bounding_box_area = (max_row - min_row) * (max_col - min_col)
    rectangularity = area / bounding_box_area
    return rectangularity

def calculate_circularity(binary_image, largest_contour, perimeter):
    moments = measure.moments_central(binary_image, contour=largest_contour)
    area = moments[0, 0]
    circularity = (4 * np.pi * area) / (perimeter ** 2)
    return circularity

def calculate_shape_features(image, threshold=0.6):
    if image.shape[2] == 4:
        image = color.rgba2rgb(image)
    image_gray = color.rgb2gray(image)
    image_gray = exposure.equalize_hist(image_gray)
    image_gray = filters.gaussian(image_gray, sigma=2)
    binary_image = image_gray > threshold
    contours = measure.find_contours(binary_image, 0.5)
    largest_contour = max(contours, key=len)
    polygon = measure.approximate_polygon(largest_contour, tolerance=100)
    contour_mask = np.zeros_like(binary_image, dtype=np.uint8)
    contour_mask[np.round(largest_contour[:, 0]).astype(int), np.round(largest_contour[:, 1]).astype(int)] = 1
    perimeter = measure.perimeter(contour_mask)
    image_height, image_width = image_gray.shape
    image_perimeter = image_height * 2 + image_width * 2
    normalized_perimeter = perimeter / image_perimeter
    num_vertices = len(polygon)
    hu_moments = measure.moments_hu(measure.moments(contour_mask))
    compactness = calculate_compactness(binary_image, largest_contour, perimeter)
    normalized_compactness = calculate_compactness_normalized(binary_image, largest_contour, normalized_perimeter)
    rectangularity = calculate_rectangularity(binary_image, largest_contour)
    circularity = calculate_circularity(binary_image, largest_contour, perimeter)
    euler_number = measure.euler_number(contour_mask)
    features = [
        normalized_perimeter,
        num_vertices,
        compactness,
        rectangularity,
        circularity
    ]
    return features

def calculate_color_histogram(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    hist_h = cv2.calcHist([hsv_image], [0], None, [256], [0, 256])
    hist_s = cv2.calcHist([hsv_image], [1], None, [256], [0, 256])
    hist_v = cv2.calcHist([hsv_image], [2], None, [256], [0, 256])
    hist_h = cv2.normalize(hist_h, hist_h).flatten()
    hist_s = cv2.normalize(hist_s, hist_s).flatten()
    hist_v = cv2.normalize(hist_v, hist_v).flatten()
    return np.concatenate([hist_h, hist_s, hist_v])

def calculate_texture_features(image):
    gray_image = color.rgb2gray(image)
    lbp = local_binary_pattern(gray_image, P=8, R=1, method='uniform')
    lbp_hist, _ = np.histogram(lbp, bins=np.arange(0, 10), density=True)
    glcm = graycomatrix((gray_image * 255).astype('uint8'), distances=[1], angles=[0], symmetric=True, normed=True)
    contrast = graycoprops(glcm, 'contrast')[0, 0]
    dissimilarity = graycoprops(glcm, 'dissimilarity')[0, 0]
    homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
    energy = graycoprops(glcm, 'energy')[0, 0]
    correlation = graycoprops(glcm, 'correlation')[0, 0]
    texture_features = np.hstack([lbp_hist, contrast, dissimilarity, homogeneity, energy, correlation])
    return texture_features

def extract_features(image):
    shape_features = calculate_shape_features(image)
    # image_data.seek(0)
    # image = io.imread(image_data)
    color_histogram = calculate_color_histogram(image)
    texture_features = calculate_texture_features(image)
    all_features = np.hstack([shape_features, color_histogram, texture_features])
    return all_features