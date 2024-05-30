#Traduction Braille / Impression image lisible par Trotec
from PIL import Image, ImageDraw

# Définition de la taille des points braille dans l'image
POINT_SIZE = 500

# Définition de la taille de la grille braille (2x3)
GRID_WIDTH = 2 * POINT_SIZE
GRID_HEIGHT = 3 * POINT_SIZE

# Dictionnaire de correspondance entre les caractères ASCII et leur équivalent en braille
braille_map = {
    'a': [1, 0, 0, 0, 0, 0],
    'b': [1, 0, 1, 0, 0, 0],
    'c': [1, 1, 0, 0, 0, 0],
    'd': [1, 1, 0, 1, 0, 0],
    'e': [1, 0, 0, 1, 0, 0],
    'f': [1, 1, 1, 0, 0, 0],
    'g': [1, 1, 1, 1, 0, 0],
    'h': [1, 0, 1, 1, 0, 0],
    'i': [0, 1, 1, 0, 0, 0],
    'j': [0, 1, 1, 1, 0, 0],
    'k': [1, 0, 0, 0, 1, 0],
    'l': [1, 0, 1, 0, 1, 0],
    'm': [1, 1, 0, 0, 1, 0],
    'n': [1, 1, 0, 1, 1, 0],
    'o': [1, 0, 0, 1, 1, 0],
    'p': [1, 1, 1, 0, 1, 0],
    'q': [1, 1, 1, 1, 1, 0],
    'r': [1, 0, 1, 1, 1, 0],
    's': [0, 1, 1, 0, 1, 0],
    't': [0, 1, 1, 1, 1, 0],
    'u': [1, 0, 0, 0, 1, 1],
    'v': [1, 0, 1, 0, 1, 1],
    'w': [0, 1, 1, 1, 0, 1],
    'x': [1, 1, 0, 0, 1, 1],
    'y': [1, 1, 0, 1, 1, 1],
    'z': [1, 0, 0, 1, 1, 1],
    ' ': [0, 0, 0, 0, 0, 0],
    '!': [0, 1, 0, 1, 1, 0],
    '"': [0, 1, 1, 0, 0, 1],
    '#': [0, 1, 1, 1, 0, 1],
    '$': [0, 1, 0, 0, 1, 1],
    '%': [1, 0, 1, 1, 1, 0],
    '&': [0, 1, 1, 1, 1, 1],
    "'": [0, 1, 0, 0, 0, 0],
    '(': [0, 1, 0, 0, 1, 0],
    ')': [0, 1, 0, 0, 1, 1],
    '*': [0, 1, 0, 1, 0, 1],
    '+': [0, 1, 0, 1, 1, 1],
    ',': [0, 0, 0, 0, 1, 0],
    '-': [0, 0, 0, 0, 1, 1],
    '.': [0, 1, 0, 1, 0, 0],
    '/': [0, 1, 0, 1, 1, 0],
    '0': [0, 1, 1, 0, 0, 0],
    '1': [0, 1, 1, 0, 0, 1],
    '2': [0, 1, 1, 0, 1, 0],
    '3': [0, 1, 1, 0, 1, 1],
    '4': [0, 1, 1, 1, 0, 0],
    '5': [0, 1, 1, 1, 0, 1],
    '6': [0, 1, 1, 1, 1, 0],
    '7': [0, 1, 1, 1, 1, 1],
    '8': [0, 1, 1, 0, 1, 0],
    '9': [0, 1, 1, 1, 0, 0],
    ':': [0, 0, 1, 0, 1, 0],
    ';': [0, 0, 1, 0, 1, 1],
    '<': [0, 0, 1, 0, 0, 0],
    '=': [0, 0, 1, 0, 0, 1],
    '>': [0, 0, 1, 1, 0, 0],
    '?': [0, 0, 1, 1, 0, 1],
    '@': [0, 1, 0, 1, 0, 0],
    '[': [0, 0, 1, 0, 1, 0],
    '\\': [0, 1, 0, 1, 0, 1],
    ']': [0, 1, 1, 0, 1, 1],
    '^': [0, 0, 1, 1, 0, 0],
    '_': [0, 0, 0, 0, 1, 0],
    '`': [0, 0, 0, 0, 1, 1],
    '{': [0, 1, 0, 1, 1, 1],
    '|': [0, 0, 1, 0, 0, 0],
    '}': [0, 1, 1, 0, 0, 0],
    '~': [0, 0, 1, 0, 0, 1],
}

def text_to_braille(text):
    braille_text = []
    for char in text.lower():
        if char in braille_map:
            braille_text.append(braille_map[char])
    return braille_text

def calculate_image_dimensions(braille_text):
    # Calcul de la taille de l'image
    image_width = ((GRID_WIDTH + POINT_SIZE // 3) + POINT_SIZE // 3)* len(braille_text)
    image_height = GRID_HEIGHT + POINT_SIZE // 2 + int( 1.5 * POINT_SIZE )
    return image_width, image_height

def draw_braille_image(text, filename):
    braille_text = text_to_braille(text)
    image_width, image_height = calculate_image_dimensions(braille_text)

    # Création de l'image
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle([0, 0, image_width, image_height], radius = POINT_SIZE, fill = "black", outline = "red", width = int( POINT_SIZE/20 ))

    # Dessin des points braille avec dégradé du centre (blanc) vers l'extérieur (noir)
    x_offset = POINT_SIZE / (POINT_SIZE * 2.1)
    y_offset = POINT_SIZE
    
    print(f"La taille d'un pixel doit etre : {2 / (POINT_SIZE * 0.76)} mm")
    print(f"La hauteur de l'image doit etre : {(2 / (POINT_SIZE * 0.76)) * image_height} mm")

    for char in braille_text:
        for j, point in enumerate(char):
            if point:
                x, y = j % 2, j // 2
                center_x = (x_offset * (GRID_WIDTH + POINT_SIZE // 2)) + (x * POINT_SIZE) + POINT_SIZE // 2
                center_y = (y * POINT_SIZE) + POINT_SIZE // 2 + y_offset

                for r in range(POINT_SIZE // 2, 0, -1):
                    grayscale_value = int((1 - r * 1.25 / (POINT_SIZE // 2)) * 255)
                    rgba_color = (grayscale_value, grayscale_value, grayscale_value)

                    draw.ellipse([(center_x - r, center_y - r),
                                  (center_x + r, center_y + r)],
                                  fill = rgba_color)
        x_offset += 1

    # Enregistrement de l'image
    image.save(filename)

# Exemple d'utilisation
text = "Hello World"
draw_braille_image(text, "braille_image.png")