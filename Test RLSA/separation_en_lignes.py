import cv2
import numpy as np
import matplotlib.pyplot as plt

def separe_en_lignes(image_binary : np, taux=0.99) -> list :
 
    """ 
    Description : Calcule le taux de pixels blancs présents sur chaque ligne de pixels. 
                  Sépare ensuite  les lignes de pixels en fonction de leur taux. 
                  On regarde dans la liste des indices des pixels blancs et si on observe un 'saut', c'est que des lignes de pixels de texte sont là
                  On stocke donc ces indices, qui correspondent aux indices des lignes de pixel contenant du texte
                  
                  Il peut arriver que certaines lignes soit considérées comme tel mais ne sont que des bas de "p" ou des choses du genre,
                  on va donc fusionner ces minis lignes avec celle de dessus

    Exemple : >>> exemple = separe_en_lignes(image)
                  exemple = [ (0, 21), (25, 65), ...]

    Input : (image) : une image binarisée en numpy
            (taux) : un float entre 0 et 1 représentant le nombre de pixels blancs / le nombre de pixels total de la ligne. De base sur 0.98

    Output : (indices_lignes) : une liste de tuples, chaque tuple les coordonées y de début et de fin de chaque ligne

    """
    # Listes contenant les indices y des lignes de pixels noirs et blanches (en fonction de leurs taux)
    liste_indices_pixels_blancs = []
    liste_indices_pixels_noirs = []

    for i in range(len(image_binary)) :
        ligne_pixel = image_binary[i]
        # Calcul du nombre de pixels blancs dans une ligne
        somme = 0
        for j in image_binary[i] :
            if j == 255 : 
                somme += 1
            else : 
                somme += 0
        # Calcul du taux de pixels blancs dans la ligne
        taux_de_blancs = somme/len(ligne_pixel)
        # Si le taux est > a un certain nombre (0.985 de base) on considère que cette ligne ne contient pas de texte
        if taux_de_blancs >= taux : #Quasi que des blancs
            liste_indices_pixels_blancs.append(i)
        else : 
            liste_indices_pixels_noirs.append(i)

    # On regarde dans la liste des indices des pixels blancs et si on observe un 'saut', c'est que des lignes de pixels de texte sont là
    # On stocke donc ces indices, qui correspondent aux indices des lignes de pixel contenant du texte
    indices_lignes = []
    for i in range(1, len(liste_indices_pixels_blancs)) :
        if liste_indices_pixels_blancs[i] != liste_indices_pixels_blancs[i-1]+1 :
            indices_lignes.append((liste_indices_pixels_blancs[i-1], liste_indices_pixels_blancs[i])) #Améliorer le +-10

    """
    # Fusion des minis lignes avec celle du dessus

    # Création d'une liste contenant la hauteur de chaque ligne
    liste_hauteurs = []
    for elt in indices_lignes :
        liste_hauteurs.append((elt[1]-elt[0]))

    # On trouve où sont les minis lignes, stockage de leurs indices et fusion
    # pour définir ce qu'est une mini ligne : une ligne dont la heuteur est inférieure à 60% de la précédente
    liste_indices_a_supprimer = []
    for i in range(1, len(indices_lignes)) :
        if liste_hauteurs[i] < liste_hauteurs[i-1]*0.6 :
            liste_indices_a_supprimer.append(i)
            out = indices_lignes[i]
            indices_lignes[i-1] = (indices_lignes[i-1][0], out[1])
   
   # On supprime les minis lignes
    liste_finale = []
    for i in range(len(indices_lignes)) :
        if i not in liste_indices_a_supprimer :
            liste_finale.append(indices_lignes[i])
    """
    
    return indices_lignes

"""
if __name__=="__main__" :

    image = cv2.imread('image_texte_chatgpt.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (thresh, image_binary) = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    plt.figure()
    plt.imshow(image_binary, cmap=plt.cm.gray)
    plt.show()

    indices_lignes = separe_en_lignes(image_binary)
    print("Indices y de début de fin pour chaque ligne :", indices_lignes)

    for t in indices_lignes :   
        plt.figure()
        plt.imshow(image[t[0]:t[1]])
        plt.show()
"""