# OCR to Braille

Our high school project "Projet d'Initiation à l'Ingénierie (P2I)" is about creating an OCR system that allows to transform text in a photo into Braille characters.

1 - redressement algo Gatien enlevé prc que ça avait retourné l'image

2 - segmentation de caractères problème.... 
Exemple région 2 il détecte 8 lignes alors qu'il n'y en a que 5
Et les r sont tout bizares, découpés.

3 - quel format pour image braille (q° pour Gatien). J'ai mis en png prc ça à l'air de mieux marcher que jpg. C'est OK ? 


Tuto server HTML :
- Installez Flask : 'pip install flask opencv-python pillow'
- dans le terminal VScode, exécuter : 'python app.py'
- Aller dans la bibliothèque des fichier de son ordi, et cliquer sur le fichier html
- Calculer du taux d'erreur 

