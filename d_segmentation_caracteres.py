import numpy as np
import os
import re
import cv2
from c_segmentation_lignes import separe_en_lignes

def separe_en_caracteres_v0(image_binary : np, indices_debut_fin_ligne : tuple, taux=0.001) -> list :

    """
    Description : Prends en entrée une ligne de texte dans une image et renvoie les indice de colonnes de début et de fin de chaque caractère
                  
                  Le but est d'obtenir le taux de pixel noirs de chaque colonne. 
                  On crée un dictionnaire stockant le nombre de pixels noirs par colonne (en parcourant l'image).
                  On divise par le nombre de pixels pour avoir le taux de pixels noirs dans la colonne.

                  On conserve seulement ceux qui sont supérieus à un certain taux et on les garde dans ue liste.
                  Nous avons donc une liste de plusieurs plages continues de données mais les plages ne sont pas continues entre elles.
                  On va donc récupérer les indices de début et de fin de chaque plage de données continues.
                  Ce qui représente les indices de début et de fin de chaque caractères de la ligne.

    Exemple : >>> ranges = separe_en_lignes(image)
                  ranges = [ (0, 21), (25, 65), ...]

    Inputs : - image_binary (np) : la verion binarisée de l'image dont on veut extraire les carctères
             - indices_debut_fin_ligne (tuple) : les indices de début et de fin de la ligne dont on veut extraire les caractères
             - taux (float) : fixé de base à 0.05, permet de spérarer les colonnes de pixel contenant de l'information ou non

    Output : (ranges) list : une liste de tuples des indices de colonnes de début et de fin de chaque caractère pour la ligne entrée
    """
   
    # Définition de l'image binarisée de la ligne voulue
    h = image_binary[indices_debut_fin_ligne[0]:indices_debut_fin_ligne[1]]

    # Création d'un dictionnaire stockant le nombre de pixels noirs par colonne
    dictionnaire = {}
    for k in range(len(h[0])) :
        dictionnaire[k] = 0

    for i in range(len(h)) :
        for j in range(len(h[i])) :
            if np.all(h[i][j] == 0) :
                dictionnaire[j] += 1
    # On divise par le nombre de pixels pour avoir le taux de pixels noirs dans la colonne
    for num_colonne in dictionnaire.keys() :
        dictionnaire[num_colonne] /= len(h)

    # On conserve dans une liste ceux qui ont un taux >= 0.001
    indices = []
    for elt in dictionnaire.keys() :
        if dictionnaire[elt] >= taux :
            indices.append(elt)

    # Vérifier si des indices ont été trouvés
    if not indices:
        return []
    
    # Obtenir des plages continues de pixels représentant les caractères en rajoutant un peu d'espace entre les caractères pour ne pas qu'ils soient sérrés dans leurs cases
    d = np.diff(indices)
    espaces =[int(val/2) for val in d if val > 1]
    
    ranges = []
    start = indices[0]
    indices_espaces = 0
    for i in range(1, len(indices)):
        if indices[i] != indices[i - 1] + 1:
            if indices_espaces < len(espaces):
                val_avant = espaces[indices_espaces - 1] if indices_espaces > 0 else espaces[indices_espaces]
                val_apres = espaces[indices_espaces]
            else:
                val_avant = 0
                val_apres = 0
            ranges.append((start - val_avant, indices[i - 1] + val_apres))
            start = indices[i]
            indices_espaces += 1

    val_avant = espaces[indices_espaces - 1] if indices_espaces > 0 else 0
    ranges.append((start - val_avant, indices[-1] + val_avant))

    return ranges

def separe_en_caracteres(image_binary, indices_debut_fin_ligne: tuple, taux=0.001, seuil_espace_mot=15) -> list:
    """
    Description : Prend en entrée une ligne de texte dans une image et renvoie les indices de colonnes de début et de fin de chaque caractère,
                  incluant les espaces entre les mots sous forme de tuples d'indices.

    Exemple : >>> ranges = separe_en_caracteres(image_binary, indices_debut_fin_ligne)
                  ranges = [ (0, 21), (25, 65), (66, 79), (80, 85), ...]

    Inputs : - image_binary (np.ndarray) : la version binarisée de l'image dont on veut extraire les caractères
             - indices_debut_fin_ligne (tuple) : les indices de début et de fin de la ligne dont on veut extraire les caractères
             - taux (float) : fixé de base à 0.001, permet de séparer les colonnes de pixels contenant de l'information ou non
             - seuil_espace_mot (int) : le seuil pour détecter les espaces entre les mots

    Output : (ranges) list : une liste de tuples des indices de colonnes de début et de fin de chaque caractère et espaces pour la ligne entrée
    """
   
    # Définition de l'image binarisée de la ligne voulue
    h = image_binary[indices_debut_fin_ligne[0]:indices_debut_fin_ligne[1]]

    # Création d'un dictionnaire stockant le nombre de pixels noirs par colonne
    dictionnaire = {k: 0 for k in range(len(h[0]))}

    # Comptage des pixels noirs par colonne
    for i in range(len(h)):
        for j in range(len(h[i])):
            if np.all(h[i][j] == 0):
                dictionnaire[j] += 1
    
    # Calcul du taux de pixels noirs pour chaque colonne
    for num_colonne in dictionnaire.keys():
        dictionnaire[num_colonne] /= len(h)

    # Liste des indices de colonnes ayant un taux de pixels noirs supérieur au seuil
    indices = [elt for elt in dictionnaire.keys() if dictionnaire[elt] >= taux]

    # Obtenir des plages continues de pixels représentant les caractères et les espaces
    ranges = []
    if not indices:
        return ranges  # Retourne une liste vide si aucun indice trouvé

    start = indices[0]
    for i in range(1, len(indices)):
        if indices[i] != indices[i - 1] + 1:
            # Ajouter la plage de colonnes pour un caractère
            ranges.append((max(0, start - 2), min(len(h[0]) - 1, indices[i - 1] + 2)))
            # Si l'écart entre deux indices est grand, ajouter un espace pour les mots sous forme de tuple d'indices
            if indices[i] - indices[i - 1] > seuil_espace_mot:
                ranges.append((indices[i - 1] + 1, indices[i] - 1))  # Ajouter les indices de colonnes vides
            start = indices[i]
    ranges.append((max(0, start - 2), min(len(h[0]) - 1, indices[-1] + 2)))

    return ranges


def nom_images_des_regions() : 
    """
    Parcours le dossier 'TEST/caracteres' et ne récupère que les images qui ont un nom de la forme 'region{nb_region}.bmp 

    Output : 
        - regions (list) : une liste des noms des images correspondant aux régions
    """

    # Chemin du dossier à parcourir
    dossier = 'TEST/caracteres'

    # Expression régulière pour matcher les noms de fichiers de la forme 'region{nb_region}.bmp'
    pattern = re.compile(r'region\d+\.bmp')

    # Liste pour stocker les chemins des images correspondant au pattern
    chemin_regions = []

    # Parcourir le dossier
    for fichier in os.listdir(dossier):
        if pattern.match(fichier):
            # Ajouter le chemin complet de l'image à la liste
            chemin_image = os.path.join(dossier, fichier)
            chemin_regions.append(chemin_image)

    return chemin_regions

def segmentation_caractere_image(input_image_path) :
    """
    Extrait tous les caractères d'une image. Création d'images matricielles au format bitmap entregistrées sous TEST/caracteres

    Input : 
        - input_image_path (str) : Chemin de l'image d'entrée
    Output : 
        - None
        
    """
    
    # liste des région et initialisation du compteur de régions
    chemin_regions = nom_images_des_regions()
    count_region = 1

    # parcours du dossier 'TEST/caracteres', à la recherche des images correpondant au zones de texte.
    for chemin_region in chemin_regions : 

        # Définition de l'image
        image_region = cv2.imread(chemin_region)
        print('chemin_region : ', chemin_region)

        # séparation en lignes 
        indices_lignes = separe_en_lignes(image_region)
        
        count_ligne = 1
        # pour chaque ligne
        for indices_debut_fin_ligne in indices_lignes : 

            # séparation caractères
            ranges = separe_en_caracteres(image_region, indices_debut_fin_ligne)

            # parcours des caracteres de la ligne
            count_caract = 1
            for elt in ranges :
                
                caract = image_region[indices_debut_fin_ligne[0]:indices_debut_fin_ligne[1], elt[0]:elt[1]]

                # Sauvegarder l'image en format matriciel (bitmap)
                cv2.imwrite(f'TEST/caracteres/region{count_region}_ligne{count_ligne}_{count_caract}.bmp', caract)
                count_caract+=1
                
            count_ligne+=1
        count_region+=1