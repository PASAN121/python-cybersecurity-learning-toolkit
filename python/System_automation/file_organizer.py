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
   suffix=[]
   for paths in file:
        suffix.append(paths.suffix.lower())  #get the file extension and convert to lower case for consistency
 
   folder_suffix=[]       

   for ext in suffix:
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            if 'Images' not in folder_suffix:
                folder_suffix.append('Images')
        elif ext in ['.doc', '.docx', '.pdf', '.txt']:
            if 'Documents' not in folder_suffix:
                folder_suffix.append('Documents')
        elif ext in ['.mp4', '.avi', '.mkv']:
            if 'Videos' not in folder_suffix:
                folder_suffix.append('Videos')
        elif ext in ['.mp3', '.wav', '.flac']:
            if 'Audio' not in folder_suffix:
                folder_suffix.append('Audio')
        elif ext in ['.zip', '.rar', '.tar.gz']:
            if 'Archives' not in folder_suffix:
                folder_suffix.append('Archives')
        else:
            if 'Others' not in folder_suffix:
                folder_suffix.append('Others')
        return folder_suffix



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