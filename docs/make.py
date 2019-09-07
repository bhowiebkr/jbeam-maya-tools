import subprocess
import os


# This code needs to be run from inside of Maya because
# Maya python access maya specific libararies, ie maya.cmds, pyside2..
"""
sys.path.append('PATH_TO_DOCS_FOLDER')

import make
reload(make)
make.make()
"""

si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW


def make(load_chrome=False):
    # Change the directory to run the commands
    root = os.path.dirname(__file__)
    os.chdir(root)

    # Clean the output
    print(subprocess.check_output('make.bat clean'.split(), startupinfo=si))

    # Generate the apidoc
    print(subprocess.check_output(
        'sphinx-apidoc -f -o source ..\\jbeamMayaTools\\ --separate'.split(), startupinfo=si))

    # Generate the HTML
    print(subprocess.check_output('make.bat html'.split(), startupinfo=si))

    if load_chrome:
            # Change if your path to chrome is different
        CHROME = os.path.join('C:\\', 'Program Files (x86)',
                              'Google', 'Chrome', 'Application', 'chrome.exe')

        # The path to the index.html file (documentation root)
        index_html = os.path.join(root, '_build', 'html', 'index.html')

        # launch Chrome to the Asset Manager API documentation
        subprocess.call([CHROME, '/new-window', index_html], startupinfo=si)

    print('Finished creating the Docs.')


if __name__ == '__main__':
    make()
