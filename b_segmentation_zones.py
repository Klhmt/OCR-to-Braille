import matplotlib.pyplot as plt
from skimage.util import img_as_ubyte
from skimage import measure, color
from skimage.morphology import erosion, disk, opening
import numpy as np
import cv2
import os

def demander_oui_ou_non(question):
    while True:
        reponse = input(f"{question} (oui/non): ").strip().lower()
        if reponse in ('oui', 'o'):
            return True
        elif reponse in ('non', 'n'):
            return False
        else:
            print("Veuillez répondre par 'oui' ou 'non'.")

def segmentation_region() :
    input_image_path = 'TEST/image_pretraitement.jpg'
    bw = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    bw_resized=cv2.resize(bw, (0, 0), fx=0.5, fy=0.5) 
    bw_resized=np.array(bw_resized)

    go_on = True  

    while go_on : 

        # erosion pour étaler les caractères puis opening pour combler les trous
        radius = int(input('Rayon de l\'érosion entre 3 et 5 pour des caractères collés, entre 5 et 10 pour des caractères plus gros, entre 10 et 15 pour des caractères très espacés. Valeur : '))
        bw_erosion = erosion(bw_resized, disk(radius)) # valeur de radius à adapter en fonction du type de texte ici
        bw_opening = opening(bw_erosion, disk(radius)) # valeur de à adapter en fonction du type de texte ici

        # seuillage
        l=50
        bw1 = img_as_ubyte(bw_opening>l)
        bw2=np.invert(bw1)

        # Labelliser les objets connectés
        labeled, numObjects = measure.label(bw2, connectivity=1, return_num=True)

        # Définir une liste de couleurs RGB
        colors = plt.cm.spring(np.linspace(0, 1, numObjects))

        # Coloriser les régions
        pseudo_color = color.label2rgb(labeled, colors=colors)

        # Filtrer les petits points
        liste_regions_brute = measure.regionprops(labeled)
        liste_regions_brute_filtree = [region for region in liste_regions_brute if region.area > 200]

        ####################### PLOT ###############################
        plt.subplot(121)
        plt.imshow(bw)
        plt.title(f'Image de base')

        plt.subplot(122)
        plt.imshow(pseudo_color)
        plt.title('Nombre d\'objets : %g' % len(liste_regions_brute_filtree))
        plt.suptitle('fermer l\'image pour continuer')
        plt.show()

        if demander_oui_ou_non('Les paramètres d\'entrée sont-ils adaptés ?') :
            go_on=False
        else :
            go_on=True


    count=1
    for region in liste_regions_brute_filtree:
        # Extraire les bornes de la boîte englobante de la région
        min_row, min_col, max_row, max_col = region.bbox
        min_row, min_col, max_row, max_col=int(min_row*2), int(min_col*2), int(max_row*2), int(max_col*2)

        # Extraire la sous-image correspondant à la région
        region_rectangulaire = bw[min_row:max_row, min_col:max_col] 

        # Création du dossier s'il n'existe pas déjà
        os.makedirs(f'TEST/caracteres', exist_ok=True)

        # Sauvegarder l'image traitée
        cv2.imwrite(f'TEST/caracteres/region{count}.bmp', region_rectangulaire)
        count+=1