import numpy as np

def separe_en_caracteres(image_binary : np, indices_debut_fin_ligne : tuple, taux=0.001) -> list :

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