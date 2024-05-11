# Dépendences
import cv2
import numpy as np
import matplotlib.pyplot as plt
from separation_en_lignes import separe_en_lignes


def separe_en_caracteres(image_binary : np, indices_debut_fin_ligne : tuple, taux=0.05) -> list :

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
            if h[i][j] == 0 :
                dictionnaire[j] += 1
    # On divise par le nombre de pixels pour avoir le taux de pixels noirs dans la colonne
    for num_colonne in dictionnaire.keys() :
        dictionnaire[num_colonne] /= len(h)

    # On conserve dans une liste ceux qui ont un taux >= 0.05
    indices = []
    for elt in dictionnaire.keys() :
        if dictionnaire[elt] >= taux :
            indices.append(elt)

    # Obtenir des plages continues de pixels représentant les caractères
    ranges = []
    start = indices[0]
    for i in range(1, len(indices)):
        if indices[i] != indices[i - 1] + 1:
            ranges.append((start, indices[i - 1]))
            start = indices[i]
    ranges.append((start, indices[-1]))

    return ranges


"""
if __name__=="__main__" :

    # Définition de l'image et de sa binarisation
    image = cv2.imread('scan1.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (thresh, image_binary) = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # On la sépare en lignes et on récupère la 1ère ligne
    indices_lignes = separe_en_lignes(image_binary)
    indices_debut_fin_ligne = indices_lignes[0]

    #Sur cette prrmière ligne on sépare les caractères
    ranges = separe_en_caracteres(image_binary, (402,487))
    for elt in ranges :
        plt.figure(figsize=(20,10))
        plt.imshow(image[indices_debut_fin_ligne[0]:indices_debut_fin_ligne[1], elt[0]:elt[1]])
        plt.show()
"""