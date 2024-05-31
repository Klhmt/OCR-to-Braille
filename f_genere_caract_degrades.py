import os
import random
import numpy as np
from skimage import io, transform, util, exposure, filters



def degrade_image(nom, image_path, folder_path):
    """Génère des images dégradés. Codé par ChatGPT 4o"""
    # Charger l'image en niveaux de gris
    image = io.imread(image_path, as_gray=True)
    
    # Créer le dossier s'il n'existe pas
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for i in range(5):
        degraded_image = np.copy(image)
        applied_alterations = []  # Liste pour stocker les altérations déjà appliquées
        
        # Appliquer plusieurs altérations aléatoires
        for _ in range(random.randint(1, 4)):  # Choisir un nombre aléatoire d'altérations entre 1 et 4
            choice = random.choice(['distrorsion', 'étirement', 'rotation', 'perte_contraste', 'flou', 'bruit', 'distorsion_contours'])
            
            # Vérifier si cette altération a déjà été appliquée
            while choice in applied_alterations:
                choice = random.choice(['distrorsion', 'étirement', 'rotation', 'perte_contraste', 'flou', 'bruit'])
            
            # Appliquer l'altération choisie
            if choice == 'distrorsion':
                #degraded_image = transform.swirl(degraded_image, rotation=random.uniform(0, 2*np.pi/50))
                pass
            elif choice == 'étirement':
                factor = random.uniform(0.9, 1.1)
                degraded_image = transform.rescale(degraded_image, scale=(factor, factor))
            elif choice == 'rotation':
                angle = random.uniform(-2, 2)  # Réduire l'amplitude de la rotation
                degraded_image = transform.rotate(degraded_image, angle, mode='edge')  # Utilisation de mode='edge' pour éviter d'ajouter du noir
            elif choice == 'perte_contraste':
                degraded_image = exposure.adjust_gamma(degraded_image, gamma=random.uniform(0.9, 1.1))
            elif choice == 'flou':
                degraded_image = filters.gaussian(degraded_image, sigma=random.uniform(0.3, 0.8))
            elif choice == 'bruit':
                degraded_image = util.random_noise(degraded_image, var=random.uniform(0.0001, 0.001))
            
            # Ajouter cette altération à la liste des altérations déjà appliquées
            applied_alterations.append(choice)
        
        # Convertir l'image dégradée en uint8
        degraded_image = (degraded_image * 255).astype(np.uint8)
        
        # Enregistrer l'image dégradée
        image_name = f"{os.path.basename(nom)}_{i+1}.png"
        io.imsave(os.path.join(folder_path, image_name), degraded_image)



def generate_degraded_images(path_original: str, path_degrade: str):
    for filename in os.listdir(path_original):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            image_path = os.path.join(path_original, filename)
            degrade_image(image_path.split(".")[0], image_path, path_degrade)


if __name__ == 'main' :
    generate_degraded_images("~/klem/Alphabet/", "~/klem/alphabet_degrade")
