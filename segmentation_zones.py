import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
from skimage.util import img_as_ubyte
from skimage import measure, color
from skimage.morphology import erosion, disk, opening
import numpy as np
import cv2
import os.path


def demander_entree):
    while True:
        try:
            convient = input('Les paramètres d\'entrée sont-ils adaptés ? (oui/non) : ').strip().lower()
            if convient not in ['oui', 'non']:
                raise ValueError('Entrée non valide')
            return convient
        except ValueError as e:
            print(f"Erreur : {e}. Veuillez entrer 'oui' ou 'non'.")


# Charger l'image
nom_image = 'texte_deux_colonnes' # nom de l'image ici
image_path = f'DB_IMAGES/{nom_image}.jpg'
bw = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Vérifier si le chemin existe ou non
# pour rendre les opérations d'érosion et d'opening plus rapide
if os.path.exists(f'bw_opening_{nom_image}.npy') : 
    bw_opening = np.load(f'bw_opening_{nom_image}.npy')
else : 
    bw_resized=cv2.resize(bw, (0, 0), fx=0.5, fy=0.5) 
    bw_resized=np.array(bw_resized)

go_on = True  

while go_on : 

    # erosion pour étaler les caractères puis opening pour combler les trous
    radius = int(input('Rayon de l\'érosion entre 3 et 5 pour des caractères collés, entre 5 et 10 pour des caractères plus gros, entre 10 et 15 pour des caractères très espacés. Valeur : '))
    bw_erosion = erosion(bw_resized, disk(radius)) # valeur à adapter en fonction du type de texte ici
    bw_opening = opening(bw_erosion, disk(radius)) # valeur à adapter en fonction du type de texte ici

    # aplliquer seuillage d'Otsu
    # l=threshold_otsu(bw_opening)
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
    liste_regions_brute_filtree = [region for region in liste_regions_brute if region.area > 100]

    ####################### PLOT ###############################
    plt.subplot(121)
    plt.imshow(bw)
    plt.title(f'Image {nom_image} de base')

    plt.subplot(122)
    plt.imshow(pseudo_color)
    plt.title('Nombre d\'objets : %g' % len(liste_regions_brute_filtree))
    plt.suptitle('fermer l\'image pour continuer')
    plt.show()

    convient = demander_entree()
    if convient=='oui':
        go_on=False
    else :
        go_on=True

# Extraire les zones de texte et les sauvegarder dans une liste
liste_regions_finale = []

count=1
for region in liste_regions_brute_filtree:
    # Extraire les bornes de la boîte englobante de la région
    min_row, min_col, max_row, max_col = region.bbox
    min_row, min_col, max_row, max_col=int(min_row*2), int(min_col*2), int(max_row*2), int(max_col*2)

    # Extraire le sous-image correspondant à la région
    region_rectangulaire = bw[min_row:max_row, min_col:max_col] 

    # Ajouter la région extraite à la liste
    liste_regions_finale.append(region_rectangulaire)
    
#     ####################### TO PLOT ###############################
#     # Afficher la région extrait avec le cadre noir
#     plt.subplot(len(liste_regions_brute_filtree), 1, count)
#     count+=1
#     plt.imshow(region_rectangulaire, cmap='gray')
#     plt.title(f'Région {region.label}')
#     plt.axis('off')

# plt.show()

# Sauvegarder les régions extraites pour une utilisation ultérieure
liste_regions_finale=np.asanyarray(liste_regions_finale, dtype=object)
np.save(f'regions{nom_image}.npy', liste_regions_finale)
print(f"liste des régions entregistrée pour une utilisation ultérieure sous 'regions{nom_image}.npy")