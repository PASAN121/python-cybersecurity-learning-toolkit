from pathlib import Path
import os
from datetime import datetime
import argparse
import shutil #for moving files


def validate_folder(folder):
    '''this function checks if the folder exists and is a directory'''
    
    folder=Path(folder) #convert to path object for better handling

    if not folder.exists():
        print(f"Error: The folder '{folder}' does not exist.")
        return False
    
    if not folder.is_dir():
        print(f"Error: The path '{folder}' is not a directory.")
        return False
    return folder

def scan_folder(validated_folder):
    '''this function scans the folder and returns a list of files (excluding directories)'''
    files=[]

    for item in validated_folder.iterdir():
        if item.is_dir():
            continue #skip directories
        files.append(item)
    return files

def get_file_extension(file):
    '''this function returns the file extension without the dot and in lowercase'''

    if file.suffix:
        return file.suffix[1:].lower()

    return "no_extension"

def get_category(extension):
    '''this function categorizes the file based on its extension, 
    if category is not found it returns 'others' '''

    categories = {
        "images": ["jpg", "jpeg", "png", "gif", "bmp", "tiff"],
        "documents": ["pdf", "docx", "txt", "xlsx", "pptx"],
        "videos": ["mp4", "avi", "mkv", "mov"],
        "audio": ["mp3", "wav", "aac"],
        "archives": ["zip", "rar", "tar", "gz"]
        
    }

    for category, extensions in categories.items():

        if extension in extensions:
            return category

    return "others"

def log_action(message):
    log_folder = Path("logs")
    log_folder.mkdir(exist_ok=True)

    log_file = log_folder / "organizer_log.txt"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def create_category_folder(validated_folder, category):
    '''this function creates a category folder if it doesn't exist and returns the path to the category folder'''
    category_folder=validated_folder/category
    log_action(f"Creating folder: {category_folder}")


    category_folder.mkdir(exist_ok=True) #exist_ok=True prevents error if folder already exists/run times error handle 
    #print(f"Created folder: {category_folder}")
    return category_folder


def move_file_to_category(file, category_folder):
     
    destination=category_folder/file.name

    try:
        shutil.move(str(file), str(destination))
        log_action(f"Moved '{file.name}' to '{category_folder}'")
        #print(f"Moved '{file.name}' to '{category_folder}'")
    except Exception as e:
        print(f"Error moving file '{file.name}': {e}")
        log_action(f"ERROR moving {file.name}: {e}")








#start

def main():
    #parser
    parser = argparse.ArgumentParser(description="Sort files into folders based on their extensions.")

    #folder argument

    parser.add_argument("--folder", help="The folder to organize/path to organize", required=True)

    #parse the arguments

    args = parser.parse_args()

    #print the folder to organize
    print(f"Organizing files in folder: {args.folder}")

    #validate the folder
    folder=validate_folder(args.folder)

    if not folder:
        print("Exiting due to invalid folder......")
        return
    
    #scan the folder for files
    files=scan_folder(folder)
    
    if not files:
        print("No files found in the folder to organize.")
        return
    
    #organize files
    for file in files:
        extension=get_file_extension(file)
        category=get_category(extension)
        category_folder=create_category_folder(folder, category)
        move_file_to_category(file, category_folder)

    print("File organization complete.")






if __name__ == "__main__":
    main()

