import pytesseract
pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import cv2

def pytesseract_extract_text(image_path):

    img=cv2.imread(image_path)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    text=pytesseract.image_to_string(img)
    return text

if __name__ == "main":
    text = pytesseract_extract_text("Test_folder\image.jpg")
    print(text)


