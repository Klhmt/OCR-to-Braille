import cv2
import numpy as np

def separe_en_caracteres(image_binary: np.ndarray, indices_debut_fin_ligne: tuple, taux=0.001, seuil_espace_mot=20) -> list:
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
            if h[i][j] == 0:
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
            ranges.append((start, indices[i - 1]))
            # Si l'écart entre deux indices est grand, ajouter un espace pour les mots sous forme de tuple d'indices
            if indices[i] - indices[i - 1] > seuil_espace_mot:
                ranges.append((indices[i - 1] + 1, indices[i] - 1))  # Ajouter les indices de colonnes vides
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
