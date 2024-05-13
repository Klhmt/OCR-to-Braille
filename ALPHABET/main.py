import matplotlib.pyplot as plt
from skimage.io import imread
import os

def rogner_image(matrice):
    # Trouver les coordonnées du rectangle de contours True
    min_ligne = len(matrice)
    max_ligne = 0
    min_colonne = len(matrice[0])
    max_colonne = 0
    
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            if matrice[i][j] == False:
                min_ligne = min(min_ligne, i)
                max_ligne = max(max_ligne, i)
                min_colonne = min(min_colonne, j)
                max_colonne = max(max_colonne, j)
    
    # Créer une nouvelle matrice contenant seulement le rectangle délimité par les contours True
    nouvelle_matrice = []
    for i in range(min_ligne, max_ligne + 1):
        nouvelle_matrice.append(matrice[i][min_colonne:max_colonne + 1])
    
    return nouvelle_matrice

def parcourir_images_dossier(dossier):
    # Vérifie si le dossier existe
    if not os.path.exists(dossier):
        print("Le dossier spécifié n'existe pas.")
        return
    
    # Liste les fichiers dans le dossier
    fichiers = os.listdir(dossier)
    
    # Filtrer les fichiers d'image
    images = [fichier for fichier in fichiers if fichier.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    return images
    # Afficher les noms des images
    # print("Images dans le dossier '{}':".format(dossier))
    # for image in images:
    #     print(image)

def cree_alphabet(dossier) : 

    alphabet=[]
    lettres=parcourir_images_dossier(dossier)
    for lettre in lettres:

        I=imread(f'{dossier}/{lettre}', as_gray=True)
        threshold_value=0.8
        I2=I>threshold_value 
        alphabet.append(rogner_image(I2))

        # for i in alphabet : 
        # plt.imshow(i)
        # plt.show()

alphabet_minuscule=cree_alphabet('caract_min')
alphabet_majuscule=cree_alphabet('caract_maj')
