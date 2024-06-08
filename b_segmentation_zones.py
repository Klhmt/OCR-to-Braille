import matplotlib.pyplot as plt
from skimage.util import img_as_ubyte
from skimage import measure, color
from skimage.morphology import erosion, disk, opening
import numpy as np
import cv2
import os
import shutil

# Fonction pour demander une réponse oui/non à l'utilisateur
def demander_oui_ou_non(question):
    """
    Pose une question 

    Input : 
        - question (str) : la question à poser
    Return : 
        - reponse (bool)
    """
    while True:
        # Poser la question
        reponse = input(f"{question} (oui/non): ").strip().lower()
        # Si la réponse est oui, renvoyer True 
        if reponse in ('oui', 'o'):
            return True
        # Si la réponse est non, renvoyer False
        elif reponse in ('non', 'n'):
            return False
        # Sinon, répéter la question
        else:
            print("Veuillez répondre par 'oui' ou 'non'.")

# Fonction pour vider et supprimer un dossier
def vider_et_supprimer_dossier(dossier_path):
    """
    Permet de vider puis supprimer un dossier. 
    Utile pour repartir de zéro lorque l'utilisateur demande de repasser par l'étape de segmentation 

    Input : 
        - dossier_path : chemin du dossier à supprimer

    Output : 
        - None
    """
    if os.path.exists(dossier_path) and os.path.isdir(dossier_path):
        # Vider le dossier
        for filename in os.listdir(dossier_path):
            file_path = os.path.join(dossier_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Supprimer les fichiers et liens symboliques
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Supprimer les sous-dossiers
            except Exception as e:
                print(f"Erreur en supprimant {file_path}. Raison: {e}")
        # Supprimer le dossier
        try:
            os.rmdir(dossier_path)
        except Exception as e:
            print(f"Erreur en supprimant le dossier {dossier_path}. Raison: {e}")

# Fonction pour segmenter des régions dans une image
def segmentation_region(input_image_path):
    """
    Permet d'identifier et de segmenter les zones de textes dans une image. 
    Sauvegarde au format bitmap (.bmp) les images des régions identifiées.

    Input : 
        - input_image_path: chemin de l'image en entrée
    Output : 
        - None
    """
    vider_et_supprimer_dossier('Images/caracteres')  # Vider et supprimer le dossier de sortie
    bw = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)  # Lire l'image en niveaux de gris

    # Redimensionner l'image
    bw_resized = cv2.resize(bw, (0, 0), fx=0.5, fy=0.5) 
    bw_resized = np.array(bw_resized)

    go_on = True  # Initialiser la boucle

    while go_on: 
        # Demander à l'utilisateur de fournir un rayon pour l'érosion
        radius = int(input('Rayon de l\'érosion entre 3 et 5 pour des caractères collés, entre 5 et 10 pour des caractères plus gros, entre 10 et 15 pour des caractères très espacés. Valeur : '))
        # Appliquer l'érosion puis l'ouverture
        bw_erosion = erosion(bw_resized, disk(radius))  # Érosion avec un disque de rayon donné
        bw_opening = opening(bw_erosion, disk(radius))  # Ouverture avec un disque de même rayon

        # Seuillage
        l = 50
        bw1 = img_as_ubyte(bw_opening > l)  # Seuillage binaire
        bw2 = np.invert(bw1)  # Inverser les couleurs

        # Labelliser les objets connectés
        labeled, numObjects = measure.label(bw2, connectivity=1, return_num=True)

        # Définir une liste de couleurs RGB
        colors = plt.cm.spring(np.linspace(0, 1, numObjects))

        # Coloriser les régions
        pseudo_color = color.label2rgb(labeled, colors=colors)

        # Filtrer les petites régions
        liste_regions_brute = measure.regionprops(labeled)
        liste_regions_brute_filtree = [region for region in liste_regions_brute if region.area > 200]

        ####################### PLOT ###############################
        plt.subplot(121)
        plt.imshow(bw)
        plt.title('Image de base')

        plt.subplot(122)
        plt.imshow(pseudo_color)
        plt.title('Nombre d\'objets : %g' % len(liste_regions_brute_filtree))
        plt.suptitle('fermer l\'image pour continuer')
        plt.show()

        # Demander à l'utilisateur si les paramètres sont adaptés
        if demander_oui_ou_non('Les paramètres d\'entrée sont-ils adaptés ?'):
            go_on = False
        else:
            go_on = True

    count = 1
    for region in liste_regions_brute_filtree:
        # Extraire les bornes de la boîte englobante de la région
        min_row, min_col, max_row, max_col = region.bbox
        min_row, min_col, max_row, max_col = int(min_row * 2), int(min_col * 2), int(max_row * 2), int(max_col * 2)

        # Extraire la sous-image correspondant à la région
        region_rectangulaire = bw[min_row:max_row, min_col:max_col] 

        # Création du dossier s'il n'existe pas déjà
        os.makedirs(f'Images/caracteres', exist_ok=True)

        # Sauvegarder l'image traitée
        cv2.imwrite(f'Images/caracteres/region{count}.bmp', region_rectangulaire)
        count += 1

if __name__== "main" : 
    segmentation_region()