import pytesseract
import cv2
# import re

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

def pytesseract_extract_text(image_path):
    # Lire l'image
    img = cv2.imread(image_path)
    
    # Convertir en niveaux de gris
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Appliquer un seuillage binaire inverse
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Optionnel : Redimensionner l'image pour améliorer la reconnaissance
    scale_percent = 200  # augmenter la taille de l'image de 200%
    width = int(thresh.shape[1] * scale_percent / 100)
    height = int(thresh.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(thresh, dim, interpolation=cv2.INTER_LINEAR)
    
    # Lire le texte de l'image (le caractère isolé dans notre cas)
    custom_config = r'--oem 3 --psm 10'  # OEM mode 3: default, PSM mode 10: Treat the image as a single character
    text = pytesseract.image_to_string(resized, config=custom_config)
    
    # Enlever les espaces et les retours à la ligne. 
    # Sinon la comparaison avec le caractère identifié retourne False pour chaque caractères !
    char = text.strip()

    # Filtrer pour ne garder que les caractères imprimables
    # char = re.sub(r'[^a-zA-Z0-9]', '', char)

    return char

if __name__ == "main":
    text = pytesseract_extract_text("TEST/caracteres/region1_ligne1_3.bmp")
    print(text)


