# rename_module.py

import os
import shutil

# RENAME 

def rename_foiles(directory_path, re_switch, word_del, file_exten, word_new,dir_mode):
    if directory_path is None:
        raise ValueError("Directory path is not provided.")
    
    for root, dirs, files in os.walk(directory_path):
        if not re_switch:  # Si switch es False, omitir los subdirectorios
            if root != directory_path:
                continue
        if dir_mode == False:
            for filename in files:
                try:
                    if word_del in filename and (file_exten == "" or filename.endswith(file_exten)):
                        old_path = os.path.join(root, filename)
                        new_filename = filename.replace(word_del, word_new)
                        new_path = os.path.join(root, new_filename)
                        shutil.move(old_path, new_path)
                except:
                    raise Exception("An error occurred while renaming files.")
        if dir_mode == True:
            for filename in dirs:
                try:
                    if word_del in filename and (file_exten == "" or filename.endswith(file_exten)):
                        old_path = os.path.join(root, filename)
                        new_filename = filename.replace(word_del, word_new)
                        new_path = os.path.join(root, new_filename)
                        shutil.move(old_path, new_path)
                except:
                    raise Exception("An error occurred while renaming files.")
       

def move_files(directory_path, directory_move, reversepath, re_switch, file_exten):
    if directory_path is None or directory_move is None:
        raise ValueError("Directory path or move path is not provided.")

    if reversepath:
        # Swap the values of directory_path and directory_move
        directory_path, directory_move = directory_move, directory_path

    for root, dirs, files in os.walk(directory_path):
        if not re_switch:  # Si switch es False, omitir los subdirectorios
            if root != directory_path:
                continue
        for filename in files:
            if not re_switch or filename.endswith(file_exten):
                source_file = os.path.join(root, filename)
                if file_exten:
                    # Si se especificó una extensión, crear la carpeta en el destino
                    folder_name = os.path.basename(root)
                    dest_folder = os.path.join(directory_move, folder_name)
                    os.makedirs(dest_folder, exist_ok=True)
                    dest_file = os.path.join(dest_folder, filename)
                else:
                    dest_file = os.path.join(directory_move, filename)
                shutil.move(source_file, dest_file)
    