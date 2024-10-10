import os
import configparser
import PySimpleGUI as sg


config = configparser.ConfigParser()
sg.theme('DarkAmber')

# ウィンドウに配置するコンポーネント
layout = [  [sg.Text('ファイルを集めるフォルダパスを入力してください　　　'),sg.InputText()],
            [sg.Text('ファイルの移動先となるフォルダパスを入力してください'), sg.InputText()],
            [sg.Button('OK'), sg.Button('終了')] ]

# ウィンドウの生成
window = sg.Window('初期設定', layout)

# イベントループ
config_path='config.ini'
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == '終了':
        break
    elif event == 'OK':
        if os.path.exists(config_path):
            config.read(config_path)
        print('Source_folder:', values[0])
        print('destination_base:', values[1])

    if 'Source'not in config:
        config['Source'] = {}
    config['Source']['source'] = str(values[0])

    if 'destination_base'not in config:
        config['destination_base']={}
    config['destination_base']['base']=str(values[1])

    with open(config_path, 'w') as configfile:
            config.write(configfile)

    break

window.close()