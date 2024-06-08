import cv2
import numpy as np
import matplotlib.pyplot as plt

def separe_en_lignes(image_binary: np.ndarray, taux=0.001) -> list:
    """
    Description :
    Cette fonction calcule le taux de pixels noirs présents sur chaque ligne de pixels
    d'une image binarisée et sépare ensuite les lignes de pixels en fonction de ce taux.
    Les lignes de texte sont identifiées et leurs indices de début et de fin sont retournés.

    Exemple :
    >>> exemple = separe_en_lignes(image_binaire)
    >>> exemple
    [(410, 503), (518, 609), (623, 711), (729, 820), ... ]

    Input :
    - image_binary (np.ndarray) : une image binarisée (en numpy).
    - taux (float) : Un float entre 0 et 1 représentant le nombre de pixels noirs
                     divisé par le nombre de pixels total de la ligne. Par défaut 0.001.

    Output :
    - indices_lignes (list) : Une liste de tuples, chaque tuple représentant les
                              coordonnées y de début et de fin de chaque ligne de texte.
    """

    # Listes contenant les indices y des lignes de pixels noirs
    liste_indices_pixels_noirs = []

    # Parcours chaque ligne de l'image binarisée
    for i in range(len(image_binary)):
        ligne_pixel = image_binary[i]
        # Calcul du nombre de pixels noirs dans une ligne
        somme = np.sum(ligne_pixel == 0)
        # Calcul du taux de pixels noirs dans la ligne
        taux_de_noirs = somme / len(ligne_pixel)
        # Si le taux est >= au seuil, on considère que cette ligne contient du texte
        if taux_de_noirs >= taux:  # Contient suffisamment de pixels noirs
            liste_indices_pixels_noirs.append(i)

    # Convertir les indices de pixels noirs en plages continues représentant les lignes de texte
    indices_lignes = []
    
    # Si aucun pixel noir n'a été trouvé, retourner une liste vide
    if not liste_indices_pixels_noirs:
        return indices_lignes

    # Initialisation de la première plage continue
    start = liste_indices_pixels_noirs[0]

    # Parcours la liste des indices de pixels noirs pour identifier les plages continues
    for i in range(1, len(liste_indices_pixels_noirs)):
        # Si l'indice actuel n'est pas consécutif au précédent, une nouvelle plage commence
        if liste_indices_pixels_noirs[i] != liste_indices_pixels_noirs[i - 1] + 1:
            indices_lignes.append((start-1, liste_indices_pixels_noirs[i - 1]+1))
            start = liste_indices_pixels_noirs[i]

    # Ajouter la dernière plage continue
    indices_lignes.append((start-1, liste_indices_pixels_noirs[-1]+1))

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