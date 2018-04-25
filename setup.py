import pip
import sys

def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])

# Install required dependencies.
import_or_install('requests')
import_or_install('selenium')

import os.path
from requests import get
from io import BytesIO
from zipfile import ZipFile
import sys
from sys import platform

if __name__ == "__main__":
    # Determine the latest release version.
    latest_release_url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    version = get(latest_release_url).content

    filename = 'chromedriver'
    url = 'https://chromedriver.storage.googleapis.com/' + version + '/chromedriver_'
    is_64bits = sys.maxsize > 2**32

    if platform == "linux" or platform == "linux2":
        # linux
        url += 'linux'
        url += '64' if is_64bits else '32'
    elif platform == "darwin":
        # OS X
        url += 'mac64'
    elif platform == "win32":
        # Windows...
        url += 'win32'
        filename += '.exe'

    url += '.zip'

    if not os.path.isfile(filename) or (len(sys.argv) > 1 and sys.argv[1] == '-update'):
        downloadFilename = url.split('/')[-1]

        print 'Downloading ' + downloadFilename + ' from ' + url

        request = get(url)

        print 'Unzipping ' + downloadFilename

        zip_file = ZipFile(BytesIO(request.content))
        zip_file.extractall()

    print 'Done!'
