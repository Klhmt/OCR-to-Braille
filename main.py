import cv2
import numpy as np
import matplotlib.pyplot as plt
from a_pretraitement import process_and_straighten_image
from b_segmentation_zones import segmentation_region
from e_reconnaissance_caract import Character, Classifieur
from f_genere_caract_degrades import generate_degraded_images
from g_braille import draw_braille_image
from h_sorted_files import find_and_sort_files
import os


################################ 1 - Prétraitement ################################
nom_image = 'image' # sans le jpg !!

if not os.path.exists(f'Test_folder/1_{nom_image}_traitee_redressee.jpg'):
    input_image_path = f'Test_folder/{nom_image}.jpg'
    output_image_path = f'Test_folder/1_{nom_image}_traitee_redressee.jpg'
    process_and_straighten_image(input_image_path, output_image_path)

################################ 2 - Segmentation zones ################################
if not os.path.exists(f'Test_folder/regions_{nom_image}'):
    segmentation_region(nom_image)

################################ 3 - Segmentaiton caractères  ################################
"""
# parcours du dossier 'regions' 
for i in range(len(os.listdir(f'Test_folder/regions_{nom_image}'))):

    # récupération de l'image
    img_list = os.listdir(f'Test_folder/regions_{nom_image}/region{i+1}')
    img_nom= f'Test_folder/regions_{nom_image}/region{i+1}/region{i+1}.jpg'

    # Définition de l'image
    img = cv2.imread(img_nom)

    # séparation en lignes 
    indices_lignes = separe_en_lignes(img)
    
    count_ligne = 1
    # pour chaque ligne
    for indices_debut_fin_ligne in indices_lignes : 

        # séparation caractères
        ranges = separe_en_caracteres(img, indices_debut_fin_ligne)

        # Création du dossier s'il n'existe pas déjà
        os.makedirs(f'Test_folder/regions_{nom_image}/region{i+1}/ligne{count_ligne}', exist_ok=True)

        count_caract = 1
        for elt in ranges :

            # Sauvegarder l'image traitée
            output_path = f'Test_folder/regions_{nom_image}/region{i+1}/ligne{count_ligne}/caract{count_caract}.jpg'
            count_caract+=1
            
            caract = img[indices_debut_fin_ligne[0]:indices_debut_fin_ligne[1], elt[0]:elt[1]]
            cv2.imwrite(output_path, caract)
            
        count_ligne+=1"""

################################ Reconnaissance caractères #############################

# créer images dégradées 
os.makedirs('Test_folder/alphabet_degrade', exist_ok=True)
generate_degraded_images('LETTRES\ARIAL\Alphabet_arial_minuscule', 'Test_folder/alphabet_degrade')

c = Classifieur(20)

for alphabet in os.listdir('LETTRES'):
    for sous_alphabet in os.listdir(f'LETTRES/{alphabet}') : 
        c.load_data_degraded('Test_folder/alphabet_degrade')
c.train()
c.generate_center_dict()


# parcours des régions 
regions = os.listdir('Test_folder/regions_image')
for region in regions : 
    print()
    print('-------------------------------------------------------------')
    print(f'Nouvelle région : {region}')


    # parcours des éléments des dossiers regions
    for ligne in os.listdir(f'Test_folder/regions_image/{region}') : 
        
        ligne_path = os.path.join(f'Test_folder/regions_image/{region}', ligne)

        # Vérifier si l'élément est un dossier et non l'image {region}.jpg 
        if os.path.isdir(ligne_path) and not ligne_path.endswith(f'{region}.jpg'): 
            
            print()
            print(f'Nouvelle ligne : {ligne}')
            print()

            text = ''
            # parcours des caractères
            for caract in find_and_sort_files(ligne_path):
                
                caract_path = os.path.join(ligne_path, caract)
                # Vérifier si l'élément n'est pas l'image braille
                if not caract_path.endswith('braille_img.png'): 
                
                    # Ouverture d'une lettre
                    im = cv2.imread(caract_path, cv2.IMREAD_GRAYSCALE)
                    a = Character(im, "")
                    a.traitement()
                    print(c.compare(a), end='')
                    text += str(c.compare(a))

            ################################ Conversion Braille #############################
            # draw_braille_image(text, f'{ligne_path}/braille_img.png') 