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
    os.makedirs('TEST/degrade', exist_ok=True)

    generate_degraded_images(path_folder, os.path.join('TEST/degrade', sous_alphabet))
