import matplotlib.pyplot as plt
from skimage.util import img_as_ubyte
from skimage import measure, color
from skimage.morphology import erosion, disk, opening
import numpy as np
import cv2
import os


def demander_entree():
    while True:
        try:
            convient = input('Les paramètres d\'entrée sont-ils adaptés ? (oui/non) : ').strip().lower()
            if convient not in ['oui', 'non']:
                raise ValueError('Entrée non valide')
            return convient
        except ValueError as e:
            print(f"Erreur : {e}. Veuillez entrer 'oui' ou 'non'.")


# Charger l'image
nom_image = 'image'
input_image_path = f'Test_folder/1_{nom_image}_traitee_redressee.jpg'
image_path = f'DB_IMAGES/{nom_image}.jpg'
bw = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

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

    # seuillage
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


count=1
for region in liste_regions_brute_filtree:
    # Extraire les bornes de la boîte englobante de la région
    min_row, min_col, max_row, max_col = region.bbox
    min_row, min_col, max_row, max_col=int(min_row*2), int(min_col*2), int(max_row*2), int(max_col*2)

    # Extraire la sous-image correspondant à la région
    region_rectangulaire = bw[min_row:max_row, min_col:max_col] 

    # Création du dossier s'il n'existe pas déjà
    os.makedirs('Test_folder/regions', exist_ok=True)

    # Chemin du dossier à créer
    folder_path = f'Test_folder/regions/region{count}'

    # Création du dossier s'il n'existe pas déjà
    os.makedirs(folder_path, exist_ok=True)
    print(f"Le dossier '{folder_path}' a été créé.")

    # Sauvegarder l'image traitée
    output_path = f'{folder_path}/region{count}.jpg'
    count+=1
    cv2.imwrite(output_path, region_rectangulaire)
    print(f"Image segmentée en zones de texte enregistrée sous {output_path}")