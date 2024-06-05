import os
from e_reconnaissance_caract import Classifieur
from f_genere_caract_degrades import generate_degraded_images


def genere_image_degradees(path_folder, sous_alphabet) : 
    """
    genere des images dégradées.

    Input : 
        - path_folder (str) : chemin du dossier contenant les images à dégrader
    Output : 
        - None
    """
    # créer images dégradées 

    # creer un dossier pour le nouvel alphabet dégradé (s'il n'existe pas déjà)
    os.makedirs(f'TEST/degrade/{sous_alphabet}', exist_ok=True)

    # c = Classifieur(20)

    generate_degraded_images(path_folder, f'TEST/degrade/{sous_alphabet}')

    # c.load_data_degraded('TEST/degrade')
    # c.train()
    # c.generate_center_dict()