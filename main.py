from a_pretraitement import process_and_straighten_image
from b_segmentation_zones import segmentation_region, demander_oui_ou_non
from d_segmentation_caracteres import segmentation_caractere_image
from e_reconnaissance_caract import reconnaissance_text_image, Classifieur
from f_genere_caract_degrades import generate_degraded_images
from g_braille import draw_braille_image
import os
            

################################ 0 - Import de l'image  ################################

input_image_path = 'TEST/test_cas_simple.bmp'

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

c = Classifieur(10)

demander_entrainement = demander_oui_ou_non('Entraitement du PCA ? ')

# parcours des alphabets du dossier 'LETTRES/'
for sous_alphabet in os.listdir('LETTRES/ARIAL')[0:-1] : 

    if demander_entrainement : 
        generate_degraded_images(f'LETTRES/ARIAL/{sous_alphabet}', f'TEST/degrade/{sous_alphabet}')
    c.load_data_degraded(f'LETTRES/ARIAL/{sous_alphabet}')

c.train()
c.generate_center_dict()

################################ Reconnaissance caractères #############################

if demander_oui_ou_non('Reconnaissance caractères ? '):
    texte, taux = reconnaissance_text_image(c)
    print()
    print('taux : ', taux)

################################ Conversion Braille #############################

if demander_oui_ou_non('Création des images Braille ? '):
    for region in texte:
        for ligne in region:
            for texte_ligne in ligne:
                draw_braille_image(texte, "Test_folder/braille_image.jpg") # changer en .png si erreur 

