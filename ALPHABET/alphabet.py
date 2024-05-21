import numpy as np
from skimage.io import imread
from skimage.transform import resize
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from skimage import measure
import os

def add_black_border(image, border_size=5):
    """Ajoute un bord noir autour d'une image."""
    new_shape = (image.shape[0] + 2 * border_size, image.shape[1] + 2 * border_size)
    bordered_image = np.zeros(new_shape, dtype=image.dtype)
    bordered_image[border_size:-border_size, border_size:-border_size] = image
    return bordered_image

def crop_to_content(image):
    """Rogne l'image pour garder uniquement la zone contenant le caractère."""
    # Convertir l'image en niveaux de gris
    gray_image = rgb2gray(image)
    
    # Appliquer un seuillage pour obtenir une image binaire
    thresh = threshold_otsu(gray_image)
    binary_image = gray_image < thresh
    
    # Trouver les contours des objets dans l'image binaire
    labeled_image = measure.label(binary_image)
    regions = measure.regionprops(labeled_image)
    
    # Trouver la boîte englobante de la région contenant le caractère
    if regions:
        min_row, min_col, max_row, max_col = regions[0].bbox
        cropped_image = binary_image[min_row:max_row, min_col:max_col]
        return cropped_image
    else:
        return binary_image  # Si aucune région n'est trouvée, retourner l'image binaire entière

def load_and_resize_alphabet(image_paths, target_size=(100, 80)):
    alphabet = []
    for path in image_paths:
        image = imread(path)
        cropped_image = crop_to_content(image)
        image_with_border = add_black_border(cropped_image, border_size=5)
        resized_image = resize(image_with_border, target_size, anti_aliasing=False)
        alphabet.append(resized_image)
    return alphabet


fichiers = os.listdir('caract_min')
alphabet = load_and_resize_alphabet([f'caract_min/{fichier}' for fichier in fichiers])

# Sauvegarder l'alphabet redimensionné pour une utilisation ultérieure
np.save('alphabet_minuscule.npy', alphabet)
