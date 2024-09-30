import os
import shutil

source_folder = R"C:\Users\Itsuki\Desktop\Project files"
destination_folders = {
    ".aep": R"C:\Users\Itsuki\Documents\aep",
    ".prproj": R"C:\Users\Itsuki\Documents\prproj",
    ".pdf": R"C:\Users\Itsuki\Documents\pdf",
}

for filename in os.listdir(source_folder):
    base, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext in destination_folders:
        destination_folder = destination_folders[ext]
        source_path = os.path.join(source_folder, filename)
        destination_path = os.path.join(destination_folder, filename)

        try:
            shutil.move(source_path, destination_path)
            print(f"{ext} file transported")
        except Exception as e:
            os.mkdir(destination_folders[ext])
            shutil.move(source_path, destination_path)
            print(f"{e}")
            print(f"{ext} file transported and make fails")