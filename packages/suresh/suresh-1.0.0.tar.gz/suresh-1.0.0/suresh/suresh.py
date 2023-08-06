import sys
import subprocess
import os


def checkRequiredPackagesForsetAvailableMemory():
    """
    To install required packages if not exist
    """
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'psutil'])


def setAvailableMemory(reduceTo):
    """
    This method is used to reduce the available memory
    """
    checkRequiredPackagesForsetAvailableMemory()
    import psutil
    a = []
    while True:
        currentMemory = psutil.virtual_memory().available
        currentMemory = (currentMemory) / (1024 * 1024 * 1024)
        if currentMemory >= reduceTo:
            a.append(' ' * 10 ** 6)


def createEmptyFile(fileName, sizeOfTheFile):
    """
    Creates a empty file in the given file name
    """
    f = open(fileName, "wb")
    f.seek(int(sizeOfTheFile) * 1024 * 1024 * 1024 - 1)
    f.write(b"\0")
    f.close()


def FindBigFile(path):
    path = os.path.abspath(path)

    # for storing the size of
    # the largest file
    max_size = 0

    # for storing the path to the
    # largest file
    max_file = ""

    # walking through the entire folder,
    # including subdirectories

    for folder, subfolders, files in os.walk(path):

        # checking the size of each file
        for file in files:
            size = os.stat(os.path.join(folder, file)).st_size

            # updating maximum size
            if size > max_size:
                max_size = size
                max_file = os.path.join(folder, file)

    return max_file, str(max_size)


def FindSmallFile(path):
    path = os.path.abspath(path)

    # for storing the size of
    # the largest file
    min_size = 0

    # for storing the path to the
    # largest file
    min_file = ""
    executeOnce = True
    # walking through the entire folder,
    # including subdirectories

    for folder, subfolders, files in os.walk(path):

        # checking the size of each file
        for file in files:
            size = os.stat(os.path.join(folder, file)).st_size
            if executeOnce == True:
                min_size = size
                min_file = os.path.join(folder, file)
                executeOnce = False
            # updating maximum size
            if min_size > size:
                min_size = size
                min_file = os.path.join(folder, file)

    return min_file, str(min_size)


def aboutPackage():
    """
    To print the version and the owner of the package
    """
    print("Version - 1.0.0, Developed by Suresh Arunachalam T")
