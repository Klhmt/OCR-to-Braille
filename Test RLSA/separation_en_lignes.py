import cv2
import numpy as np
import matplotlib.pyplot as plt

def separe_en_lignes(image_binary: np.ndarray, taux=0.001, reduction=1, tol=10) -> list:
    """
    Description :
    Calcule le taux de pixels noirs présents sur chaque ligne de pixels.
    Sépare ensuite les lignes de pixels en fonction de leur taux et de la tolérance
    pour détecter les espaces entre les paragraphes.

    Exemple :
    >>> exemple = separe_en_lignes(image)
    >>> exemple
    [(0, 21), (25, 65), ...]

    Input :
    - image_binary (np.ndarray) : une image binarisée (en numpy).
    - taux (float) : Un float entre 0 et 1 représentant le nombre de pixels noirs
                     divisé par le nombre de pixels total de la ligne. Par défaut 0.001.
    - reduction (int) : Un entier >= 1, indiquant par quel nombre on divise le nombre de colonnes
                        de l'image pour faire les tests. Par défaut 1.
    - tol (int) : Tolérance pour détecter les grands espaces entre les lignes de texte,
                  permettant de distinguer les paragraphes. Par défaut 10.

    Output :
    - indices_lignes (list) : Une liste de tuples, chaque tuple représentant les
                              coordonnées y de début et de fin de chaque ligne.
    """

    # Listes contenant les indices y des lignes de pixels noirs
    liste_indices_pixels_noirs = []

    image_reduite = image_binary[0:len(image_binary), 0:int(len(image_binary[0]) / reduction)]

    for i in range(len(image_reduite)):
        ligne_pixel = image_reduite[i]
        # Calcul du nombre de pixels noirs dans une ligne
        somme = np.sum(ligne_pixel == 0)
        # Calcul du taux de pixels noirs dans la ligne
        taux_de_noirs = somme / len(ligne_pixel)
        # Si le taux est >= au seuil, on considère que cette ligne contient du texte
        if taux_de_noirs >= taux:  # Quasi que des noirs
            liste_indices_pixels_noirs.append(i)

    # Utiliser une tolérance pour détecter les espaces entre les paragraphes
    diff = np.diff(liste_indices_pixels_noirs)
    indices_lignes = []
    start = liste_indices_pixels_noirs[0]

    for i in range(len(liste_indices_pixels_noirs) - 1):
        if diff[i] > tol:  # Un grand saut indique un espace de paragraphe
            indices_lignes.append((start, liste_indices_pixels_noirs[i]))
            start = liste_indices_pixels_noirs[i + 1]
        elif diff[i] != 1:  # Une nouvelle ligne de texte commence
            indices_lignes.append((start, liste_indices_pixels_noirs[i]))
            start = liste_indices_pixels_noirs[i + 1]

    # Ajouter la dernière ligne détectée
    indices_lignes.append((start, liste_indices_pixels_noirs[-1]))

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