from a_pretraitement import process_and_straighten_image
from b_segmentation_zones import segmentation_region, demander_oui_ou_non
from d_segmentation_caracteres import segmentation_caractere_image
from e_reconnaissance_caract import reconnaissance_text_image, Classifieur
from f_genere_caract_degrades import generate_degraded_images
from g_braille import draw_braille_image
import os


################################ 0 - Import de l'image  ################################

input_image_path = f'TEST/scan_niv_gris_300ppp_fiche_ocr.bmp'

################################ 1 - Prétraitement ################################

if demander_oui_ou_non('Etape de prétraitement ? ') : 
    output_image_path = 'TEST/image_pretraitement.jpg'
    process_and_straighten_image(input_image_path, output_image_path)

################################ 2 - Segmentation zones ################################

if demander_oui_ou_non('Etape de segementation en zones de texte ? '):
    segmentation_region('TEST/image_pretraitement.jpg')

################################ 3 - Segmentaiton caractères  ################################

if demander_oui_ou_non('Etape de segementation en caractères ? '):
    print('input_image_path :', input_image_path)
    segmentation_caractere_image(input_image_path)

###################### Entraîner le PCA avec un jeu de données #############################
"""
if demander_oui_ou_non('Entraitement du PCA ? '):

    # parcours des alphabets du dossier 'LETTRES/'
    for alphabet in os.listdir('LETTRES') : 

        print('alphabet : ', alphabet)
        # parcours des sous-alphabets des alphabets
        for sous_alphabet in os.listdir(f'LETTRES/{alphabet}') :
            
            print('sous-alphabet : ', sous_alphabet)
            # Filtrer pour ne garder que les sous-dossiers
            sous_dossiers = [d for d in sous_alphabet if os.path.isdir(os.path.join(f'LETTRES/{alphabet}', d))] 

            genere_image_degradees(f'LETTRES/{alphabet}/{sous_alphabet}')
"""
if demander_oui_ou_non('Entraitement du PCA ? '):

    # parcours des alphabets du dossier 'LETTRES/'
    print(os.listdir('LETTRES/ARIAL')[0:-1])
    for sous_alphabet in os.listdir('LETTRES/ARIAL')[0:-1] : 

        
        print('sous-alphabet : ', sous_alphabet)
        # Filtrer pour ne garder que les sous-dossiers
        # sous_dossiers = [d for d in sous_alphabet if os.path.isdir(os.path.join(f'LETTRES/ARIAL', d))] 

        genere_image_degradees(f'LETTRES/ARIAL/{sous_alphabet}')

c = Classifieur(10)
c.load_data_degraded("TEST/degrade")


################################ Reconnaissance caractères #############################

if demander_oui_ou_non('Reconnaissance caractères ? '):
    texte, taux = reconnaissance_text_image(c)

################################ Conversion Braille #############################

if demander_oui_ou_non('Création des images Braille ? '):
    for region in texte:
        for ligne in region:
            for texte_ligne in ligne:
                draw_braille_image(texte, "Test_folder/braille_image.jpg") # changer en .png si erreur 

