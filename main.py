from a_pretraitement import process_and_straighten_image
from b_segmentation_zones import segmentation_region, demander_oui_ou_non
from d_segmentation_caracteres import segmentation_caractere_image
from e_reconnaissance_caract import reconnaissance_text_image, Classifieur
from g_braille import draw_braille_image
from j_entrainer_pca import genere_image_degradees
import os
            

################################ 0 - Import de l'image  ################################

input_image_path = f'TEST/scan_niv_gris_300ppp_fiche_ocr.bmp'

################################ 1 - Prétraitement ################################

if demander_oui_ou_non('Etape de prétraitement ? ') : 
    output_image_path = 'TEST/image_pretraitement.jpg'
    process_and_straighten_image(input_image_path, output_image_path)

################################ 2 - Segmentation zones ################################

if demander_oui_ou_non('Etape de segementation en zones de texte ? '):
    segmentation_region()

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
c = Classifieur(10)

if demander_oui_ou_non('Entraitement du PCA ? '):

    # parcours des alphabets du dossier 'LETTRES/'
    for sous_alphabet in os.listdir('LETTRES/ARIAL')[0:-1] : 

        genere_image_degradees(f'LETTRES/ARIAL/{sous_alphabet}', sous_alphabet)
        c.load_data_degraded(f'LETTRES/ARIAL/{sous_alphabet}')

c.train()
c.generate_center_dict()

################################ Reconnaissance caractères #############################

# J'ai mis ça provisoirement parce que j'avais pas envie de créer un des caractères dégradés de tous les alphabets 
# mais normalement ça n'a pas ça place ici, c'est juste au dessus qu'on entraine le pca


if demander_oui_ou_non('Reconnaissance caractères ? '):
    texte, taux = reconnaissance_text_image(c)
    print(taux)

################################ Conversion Braille #############################

if demander_oui_ou_non('Création des images Braille ? '):
    for region in texte:
        for ligne in region:
            for texte_ligne in ligne:
                draw_braille_image(texte, "Test_folder/braille_image.jpg") # changer en .png si erreur 

