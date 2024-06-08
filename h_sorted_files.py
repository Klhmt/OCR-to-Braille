import re
import os 

# pour affichier les caractères dans l'ordre, avec des nombres croissants, 
# et pas caract1, caract11, caract 2 etc... 

def find_and_sort_files(ligne_path):
            # Lister tous les fichiers dans le répertoire
            files = [f for f in os.listdir(ligne_path) if os.path.isfile(os.path.join(ligne_path, f))]
            
            # Filtrer et trier les fichiers en fonction des numéros extraits
            def extract_number(filename):
                match = re.search(r'caract(\d+)\.jpg', filename)
                return int(match.group(1)) if match else -1

            sorted_files = sorted(files, key=extract_number)
            
            return sorted_files

if __name__ == "__main__":
    ligne_path = "Test_folder/regions_image/region8/ligne6"  
    sorted_files = find_and_sort_files(ligne_path)
    
    # Afficher les fichiers triés
    for file in sorted_files:
        print(os.path.join(ligne_path, file))