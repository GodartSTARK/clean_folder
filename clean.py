import transliterate 
import os
import pathlib
import shutil
import patoolib
import tempfile


def normalize(filename):
    name = str(filename)
    name = transliterate.translit(name, 'ru', reversed=True)
    name = ''.join([char if char.isalnum() or char == '.' or char.isdigit() else '_' for char in name])
    return name


def move(file_path):
    file_extension = os.path.splitext(file_path)[-1].lower()[1:]
    for folder_name, allowed_extensions in dict_folders.items():
        if file_extension in allowed_extensions:
            folder_path = pathlib.Path(folder_name)
            folder_path.mkdir(exist_ok=True)
            if file_extension in ['zip', 'tar', 'gz', 'bz2']:
                temp_dir = pathlib.Path(tempfile.mkdtemp())
                try:
                    patoolib.extract_archive(str(file_path), outdir=str(temp_dir))
                    for extracted_file in temp_dir.glob('**/*'):
                        if extracted_file.is_file():
                            extracted_file_extension = os.path.splitext(extracted_file)[-1].lower()[1:]
                            for folder_name, allowed_extensions in dict_folders.items():
                                if extracted_file_extension in allowed_extensions:
                                    new_file_path = pathlib.Path(folder_name) / normalize(extracted_file.name)
                                    shutil.move(str(extracted_file), str(new_file_path))
                                    print(f"Moved {extracted_file} to {new_file_path}")
                                    break
                            else:
                                new_file_path = pathlib.Path('other') / normalize(extracted_file.name)
                                shutil.move(str(extracted_file), str(new_file_path))
                                print(f"Moved {extracted_file} to {new_file_path}")
                except Exception as e:
                    print(f"Failed to extract {file_path}: {e}")
                finally:
                    shutil.rmtree(str(temp_dir))
            else:
                new_file_path = folder_path / normalize(file_path.name)
                shutil.move(str(file_path), str(new_file_path))
                print(f"Moved {file_path} to {new_file_path}")
                break
    else:
        new_file_path = pathlib.Path('other') / normalize(file_path.name)
        shutil.move(str(file_path), str(new_file_path))
        print(f"Moved {file_path} to {new_file_path}")


dict_folders = {
    'images': ['jpeg', 'png', 'jpg', 'svg'],
    'video': ['avi', 'mp4', 'mov', 'mkv'],
    'documents': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
    'audio': ['mp3', 'ogg', 'wav', 'amr'],
    'archives': ['zip', 'tar', 'gz', 'bz2'],
    'other': []         
}

source_folder = pathlib.Path(r'd:\testfolder')

for folder_name in dict_folders.keys():
    folder_path = pathlib.Path(folder_name)
    folder_path.mkdir(exist_ok=True)

for file_path in source_folder.glob('**/*'):
    if file_path.is_file():
        move(file_path)