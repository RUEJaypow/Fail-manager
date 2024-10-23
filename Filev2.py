import os
import shutil
import errno
import configparser
import PySimpleGUI as sg
from datetime import datetime

def move_files(source_folder, destination_base, config_path='config.ini'):
    config = configparser.ConfigParser()

    if not os.path.exists(config_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_path)

    config.read(config_path)

    if not config.has_section('Path'):
        config.add_section('Path')

    destination_folders = config['Path']

    for filename in os.listdir(source_folder):
        base, ext = os.path.splitext(filename)
        ext = ext.lstrip('.').lower()

        if ext not in destination_folders:
            new_folder = os.path.join(destination_base, ext)
            os.makedirs(new_folder, exist_ok=True)
            config['Path'][ext] = new_folder
            with open(config_path, 'w') as configfile:
                config.write(configfile)
            print(f"{ext} folder is created")

        destination_folder = destination_folders.get(ext)
        if destination_folder:
            source_path = os.path.join(source_folder, filename)
            destination_path = os.path.join(destination_folder, filename)

            try:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                new_file_name = f"{base}_{timestamp}{ext}"
                new_destination_path = os.path.join(destination_path, new_file_name)
                shutil.move(source_path, new_destination_path)
                print(f"{ext} file transported")
            except FileNotFoundError:
                os.makedirs(destination_folder, exist_ok=True)
                shutil.move(source_path, destination_path)
                print(f"{ext} file transported and missing folder was created")
            except FileExistsError:
                print("File Exists Error")
            except Exception as e:
                print(f"Error: {e}")

def main():
    config = configparser.ConfigParser()
    sg.theme('Black')
    config_path = 'config.ini'
    if os.path.exists(config_path):
        config.read(config_path)
        if 'Source' in config:
            source_path=config['Source'].get('source','')
            destination_path=config['destination_base'].get('base','')
        else:
            source_path=''
            destination_path=''

        layout = [
        [sg.Text('ファイルを集めるフォルダパスを入力してください　　　'), sg.InputText(source_path)],
        [sg.Text('ファイルの移動先となるフォルダパスを入力してください'), sg.InputText(destination_path)],
        [sg.Button('OK'), sg.Button('終了')]
        ]

        window = sg.Window('sample', layout)

    config_path = 'config.ini'

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '終了':
            break
        elif event == 'OK':
            source_folder = values[0].replace('"', '')
            destination_base = values[1].replace('"', '')

            print('Source_folder:', source_folder)
            print('destination_base:', destination_base)

            if os.path.exists(config_path):
                config.read(config_path)

            if 'Source' not in config:
                config['Source'] = {}
            config['Source']['source'] = source_folder

            if 'destination_base' not in config:
                config['destination_base'] = {}
            config['destination_base']['base'] = destination_base

            with open(config_path, 'w') as configfile:
                config.write(configfile)

            try:
                move_files(source_folder, destination_base, config_path)
            except Exception as e:
                print("エラーが発生しました:", e)

            break

    window.close()

if __name__ == "__main__":
    main()