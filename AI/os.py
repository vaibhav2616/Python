import os
directory_path = '/Games'
files = os.listdir(directory_path)  
for file in files:
    print(file)