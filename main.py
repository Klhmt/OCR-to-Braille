import cv2
import numpy as np
import matplotlib.pyplot as plt
from a_pretraitement import process_and_straighten_image
from b_segmentation_zones import segmentation_region
from c_segmentation_lignes import separe_en_lignes
from d_segmentation_caracteres import separe_en_caracteres
# from e_reconnaissance_caract import 
import os


# 1 - Prétraitement
nom_image = 'image'

if not os.path.exists(f'Test_folder/1_{nom_image}_traitee_redressee.jpg'):
    input_image_path = f'Test_folder/{nom_image}.jpg'
    output_image_path = f'Test_folder/1_{nom_image}_traitee_redressee.jpg'
    process_and_straighten_image(input_image_path, output_image_path)

# 2 - Segmentation zones
if not os.path.exists('Test_folder/regions'):
    segmentation_region(f'Test_folder/1_{nom_image}_traitee_redressee.jpg')

# 3 - Segmentaiton caractères

# parcours du dossier 'regions' 
for i in range(len(os.listdir('Test_folder/regions'))):

    # récupération de l'image
    img_list = os.listdir(f'Test_folder/regions/region{i+1}')
    img_nom= f'Test_folder/regions/region{i+1}/region{i+1}.jpg'

    # Définition de l'image et de sa binarisation
    img = cv2.imread(img_nom)

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # (thresh, image_binary) = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # On la sépare en lignes et on récupère la 1ère ligne
    indices_lignes = separe_en_lignes(img)

    count_ligne = 1
    # pour chaque ligne
    for n in indices_lignes : 

        # on récupère la ligne n
        indices_debut_fin_ligne = n

        #Sur cette permière ligne on sépare les caractères
        ranges = separe_en_caracteres(img, indices_debut_fin_ligne)

        count_caract = 1
        for elt in ranges :

            # Création du dossier s'il n'existe pas déjà
            os.makedirs(f'Test_folder/regions/region{i+1}/caract', exist_ok=True)

            # Sauvegarder l'image traitée
            output_path = f'Test_folder/regions/region{i+1}/caract/caract_ligne_{count_ligne}_caract_{count_caract}.jpg'
            count_caract+=1
            
            caract = img[indices_debut_fin_ligne[0]:indices_debut_fin_ligne[1], elt[0]:elt[1]]
            cv2.imwrite(output_path, caract)

            
            
        count_ligne+=1

