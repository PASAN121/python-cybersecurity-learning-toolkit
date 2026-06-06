from pathlib import Path


#get the path of the current directory

def get_user_path():
    
    print("Please enter the path of the directory you want to organize.")
    print("example path: C:/Users/YourName/Desktop/FolderToOrganize")
    
    while True:


        user_path = input("Enter the path of the directory you want to organize: ")
        if Path(user_path).is_dir():
            return user_path
        else:
            print("Invalid path. Please enter a valid directory path.")


    