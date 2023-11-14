#File Organization: Automatically move files to specific directories based on their extension
#Duplicate File Handling: Scan for duplicates and remove them or move them to a separate folder.

import shutil
import os
import hashlib

Downloads_WD = r"C:\Users\olive\Downloads"
Documents_WD = r"C:\Users\olive\OneDrive\Documents"
Destination_Powerpoints = r"C:\Users\olive\OneDrive\Documents\Powerpoints"
Destination_PDF = r"C:\Users\olive\OneDrive\Documents\PDF's"
Destination_Docs = r"C:\Users\olive\OneDrive\Documents\Word documents"
Destination_Excel = r"C:\Users\olive\OneDrive\Documents\Excel Docs"
Destination_MATLAB = r"C:\Users\olive\OneDrive\Documents\Matlab Scripts"

def if_already_exists(source_path, destination): #function checks if a file already exists within a folder
    file_name = os.path.basename(source_path)    #Strips our file into its name, not its path
    destination_path = os.path.join(destination, file_name)   #This is the destination path, which we will check to see if it exists
    if os.path.exists(destination_path):                      #Checks if the destination path exists
        duplicate_folder = os.path.join(destination, "Duplicates")  #This is our duplicates folder
        if not os.path.exists(duplicate_folder):   #If we dont have a duplicate folder yet, we will create one
            os.makedirs(duplicate_folder)          #Creates our duplicate folder
        destination_path = os.path.join(duplicate_folder, file_name)  #create a new destination path for the duplicate file
        count = 1                   #This variable is in place to handle a situation where there is duplicates within the duplicate folder
        while os.path.exists(destination_path):
            name, extension = os.path.splitext(file_name)
            new_file_name = f"{name}({count}){extension}"
            destination_path = os.path.join(duplicate_folder, new_file_name)
            count += 1
    return destination_path
def move_files(Source_WD):                #moves files to given folders based on their file type. From a given Source (e.g downloads)
    Source_File = os.listdir(Source_WD)   #Source_File is the directory
    for file in Source_File:              #iterates through the directory
        if file.endswith((".pptx", ".odp")):                                #if the file is a powerpoint
            source_path = os.path.join(Source_WD, file)           #gives us the path of the file we want to move
            destination_path = if_already_exists(source_path, Destination_Powerpoints)
            shutil.move(source_path, destination_path)     #moves the given file
        elif file.endswith(".pdf"):
            source_path = os.path.join(Source_WD, file)
            destination_path = if_already_exists(source_path, Destination_PDF)
            shutil.move(source_path, destination_path)
        elif file.endswith((".docx",".odt")):
            source_path = os.path.join(Source_WD, file)
            destination_path = if_already_exists(source_path, Destination_Docs)
            shutil.move(source_path, destination_path)
        elif file.endswith((".xlsx", ".ods")):
            source_path = os.path.join(Source_WD, file)
            destination_path = if_already_exists(source_path, Destination_Excel)
            shutil.move(source_path, destination_path)
        elif file.endswith(".m"):
            source_path = os.path.join(Source_WD, file)
            destination_path = if_already_exists(source_path, Destination_MATLAB)
            shutil.move(source_path, destination_path)
def hash_file(filepath):       #Gets a hash for a chosen file, SHA - 1 format
    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open(filepath, 'rb') as file:
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()
def scan_for_duplicates(Folder):   #Searches for duplicates within a given folder based on their SHA - 1 hash
    hashes_of_files = {}   #dictionary to store the hashes of certain folders for comparison later
    folder_file = os.listdir(Folder)   #the directory for the folder
    for filename in folder_file:
        path = os.path.join(Folder, filename)
        if os.path.isdir(path):   #we are going to ignore if the path is a directory (Folder)
            continue
        file_hash = hash_file(path)
        if file_hash in hashes_of_files:
            duplicate_folder = os.path.join(Folder, "Duplicates")  #This is our duplicates folder
            if not os.path.exists(duplicate_folder):   #If we dont have a duplicate folder yet, we will create one
                os.makedirs(duplicate_folder)          #Creates our duplicate folder
            destination_dupe = os.path.join(duplicate_folder, filename)    
            shutil.move(path, destination_dupe)
        else:
            hashes_of_files[file_hash] = path    
    

move_files(Documents_WD)
move_files(Downloads_WD)
scan_for_duplicates(Destination_PDF)
scan_for_duplicates(Destination_Powerpoints)
scan_for_duplicates(Destination_Docs)
scan_for_duplicates(Destination_MATLAB)
scan_for_duplicates(Destination_Excel)

