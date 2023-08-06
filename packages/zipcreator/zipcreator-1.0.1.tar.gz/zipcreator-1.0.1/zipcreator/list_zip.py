import os
import zipfile


def create(items, destination, compression=zipfile.ZIP_DEFLATED):
    """
    Create the zipfile located at the given destination with the files specified.

    :param items: List of files ad directories as strings. Directories must end in /
    :param destination: path and filename of desired zip destination
    :param compression: Compression format for zip handler
    """
    zip_handler = zipfile.ZipFile(destination, 'w', compression)
    if len(items) > 0:
        for item in items:
            if item[-1] == '/':
                # Directory
                for root, dirs, files in os.walk(item):
                    zip_handler.write(root)
                    for file in files:
                        zip_handler.write(os.path.join(root, file))
            else:
                # File
                zip_handler.write(item)
    zip_handler.close()
