import os
import shutil
import errno
import configparser

config = configparser.ConfigParser()
config_path = 'config.ini'

if not os.path.exists(config_path):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_path)

config.read(config_path)

source_folder = config['Source']['source']
destination_base = config['destination_base']['base']
destination_folders = config['Path']

# Ensure 'Path' section exists
if not config.has_section('Path'):
    config.add_section('Path')

for filename in os.listdir(source_folder):
    base, ext = os.path.splitext(filename)
    ext = ext.lstrip('.').lower()  # Remove leading '.' from extension

    # If extension folder does not exist, create it and update config
    if ext not in destination_folders:
        new_folder = os.path.join(destination_base, ext)
        os.makedirs(new_folder, exist_ok=True)  # Create folder if it doesn't exist
        config['Path'][ext] = new_folder
        with open(config_path, 'w') as configfile:
            config.write(configfile)
        print(f"{ext} folder is created")

    # Move file to the corresponding folder
    destination_folder = destination_folders.get(ext)
    if destination_folder:
        source_path = os.path.join(source_folder, filename)
        destination_path = os.path.join(destination_folder, filename)

        try:
            shutil.move(source_path, destination_path)
            print(f"{ext} file transported")
        except FileNotFoundError:
            os.makedirs(destination_folder, exist_ok=True)
            shutil.move(source_path, destination_path)
            print(f"{ext} file transported and missing folder was created")
        except FileExistsError:
            print("File Exists Error")
        except Exception as e:
            print(f"Error: {e}")
