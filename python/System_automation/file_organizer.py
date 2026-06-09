from pathlib import Path
import os
from datetime import datetime
import argparse

def validate_folder(folder):
    '''this function checks if the folder exists and is a directory'''
    
    folder=Path(folder) #convert to path object for better handling

    if not os.path.exists(folder):
        print(f"Error: The folder '{folder}' does not exist.")
        return False
    if not os.path.isdir(folder):
        print(f"Error: The path '{folder}' is not a directory.")
        return False
    return folder

def scan_folder(validated_folder):
    files=[]

    for item in validated_folder.iterdir():
        if item.is_dir():
            continue #skip directories
        files.append(item)
    return files

def get_file_extension(file):

    if file.suffix:
        return file.suffix[1:].lower()

    return "no_extension"

def get_category(extension):

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



#start

def main():
    #parser
    parser = argparse.ArgumentParser(description="Sort files into folders based on their extensions.")

    #folder arggument

    parser.add_argument("--folder", help="The folder to organize/path to organize", required=True)

    #parse the arguments

    args = parser.parse_args()

    #print the folder to organize
    print(f"Organizing files in folder: {args.folder}")

    folder=args.folder

    #validate the folder
    validated_folder=validate_folder(folder)






if __name__ == "__main__":
    main()