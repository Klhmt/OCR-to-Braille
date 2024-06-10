from a_pretraitement import process_and_straighten_image
from b_segmentation_zones import segmentation_region, demander_oui_ou_non
from d_segmentation_caracteres import segmentation_caractere_image
from e_reconnaissance_caract import reconnaissance_text_image, Classifieur
from g_braille import draw_braille_image
from j_entrainer_pca import genere_image_degradees
import os


################################ 0 - Import de l'image  ################################

input_image_path = r'test_cas_simple.bmp'

################################ 1 - Prétraitement ################################

if demander_oui_ou_non('Etape de prétraitement ? ') : 
    output_image_path = 'Images/image_pretraitement.jpg'
    process_and_straighten_image(input_image_path, output_image_path)

################################ 2 - Segmentation zones ################################

if demander_oui_ou_non('Etape de segementation en zones de texte ? '):
    segmentation_region(output_image_path)

################################ 3 - Segmentaiton caractères  ################################

if demander_oui_ou_non('Etape de segementation en caractères ? '):
    print('input_image_path :', input_image_path)
    segmentation_caractere_image(input_image_path)

###################### Entraîner le PCA avec un jeu de données #############################

if demander_oui_ou_non('Génération images degradées (attention ne pas re générer si des fichiers existent déjà ? '):

    # parcours des alphabets du dossier 'LETTRES/'
    print(os.listdir('LETTRES/ARIAL')[0:-1])
    for sous_alphabet in os.listdir('LETTRES/ARIAL')[0:-1] : 
        
        print('Génération images dégradées pour le sous-alphabet : ', sous_alphabet)
        # Filtrer pour ne garder que les sous-dossiers
        
        genere_image_degradees(f'LETTRES/ARIAL/{sous_alphabet}', sous_alphabet)


################################ Reconnaissance caractères #############################

if demander_oui_ou_non('Reconnaissance caractères ? '):
    c = Classifieur(30)
    
    for sous_alphabet in os.listdir('LETTRES/ARIAL')[0:-1] :
        c.load_data_degraded(f"Images/degrade/{sous_alphabet}")

    c.train()
    c.generate_center_dict()
    texte = reconnaissance_text_image(c)

################################ Conversion Braille #############################

if demander_oui_ou_non('Création des images Braille ? '):
    for _ in range(len(texte)):
        draw_braille_image(texte[_], f"Braille/braille_ligne_{_}.jpg") # changer en .png si erreur 

