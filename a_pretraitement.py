import cv2
import numpy as np
import os
import re

def compute_skew(image):
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Binariser l'image
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Trouver les coordonnées des pixels non nuls
    coords = np.column_stack(np.where(binary > 0))
    
    # Calculer une boîte englobante inclinée
    rect = cv2.minAreaRect(coords)
    angle = rect[-1]
    
    # Corriger l'angle pour obtenir une rotation positive ou négative
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
        
    return angle

def process_and_straighten_image(image_path, output_path):
    # Lire l'image depuis le fichier
    image = cv2.imread(image_path)
    
    # Calculer l'angle de redressement
    angle = compute_skew(image)
    
    # Obtenir les dimensions de l'image
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    
    # Calculer la matrice de rotation
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Appliquer la rotation pour redresser l'image
    straightened = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    # Convertir l'image redressée en niveaux de gris
    straightened_gray = cv2.cvtColor(straightened, cv2.COLOR_BGR2GRAY)
    straightened_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Appliquer le seuillage d'Otsu
    _, binary_image = cv2.threshold(straightened_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Sauvegarder l'image traitée
    cv2.imwrite(output_path, binary_image)

if __name__== "main" : 
    nom_image = 'Test_folder/texte_deux_colonnes.jpg'
    input_image_path = f'Test_folder/{nom_image}.jpg'
    output_image_path = f'Test_folder/1_{nom_image}_traitee_redressee.jpg'
    process_and_straighten_image(input_image_path, output_image_path)