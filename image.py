import os
import tempfile
import subprocess

def imageToStr(path):
    temp = tempfile.NamedTemporaryFile(delete=False)
    process = subprocess.Popen(['tesseract', path, temp.name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.communicate()
    with open(temp.name + '.txt', 'r') as handle:
        contents = handle.read()
    os.remove(temp.name + '.txt')
    os.remove(temp.name)
    return contents

