from flask import Flask, request, send_file
from PIL import Image
import io
import cv2
import numpy as np

app = Flask(__name__)

def preprocess_image(image):
    # Implémentez votre code de prétraitement ici
    # Exemple : convertir en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

def process_step_1(image):
    # Exemple de traitement pour l'étape 1
    return preprocess_image(image)

def process_step_2(image):
    # Implémentez le traitement de l'étape 2 ici
    return image

def process_step_3(image):
    # Implémentez le traitement de l'étape 3 ici
    return image

def process_step_4(image):
    # Implémentez le traitement de l'étape 4 ici
    return image

def process_step_5(image):
    # Implémentez le traitement de l'étape 5 ici
    return image

@app.route('/process', methods=['POST'])
def process():
    step = int(request.form['step'])
    image_file = request.files['image'].read()
    image = np.array(Image.open(io.BytesIO(image_file)))

    if step == 1:
        processed_image = process_step_1(image)
    elif step == 2:
        processed_image = process_step_2(image)
    elif step == 3:
        processed_image = process_step_3(image)
    elif step == 4:
        processed_image = process_step_4(image)
    elif step == 5:
        processed_image = process_step_5(image)
    else:
        return "Invalid step", 400

    _, buffer = cv2.imencode('.png', processed_image)
    io_buf = io.BytesIO(buffer)
    return send_file(io_buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
