from alveolus import hooks
from alveolus.settings import Settings
from alveolus import settings
from shutil import copy2
import sys
import os


def main():
    val = input("--------Welcome to Alveolus----------------------------------------------\n"
                "*)(Quickstart)Setup alveolus(Beta)(Manually edit the created .ini file):1\n"
                "*)Build Alveolus Documentation:2\n"
                "*)Clean Alveolus Documentation:3\n"
                "-------------------------------------------------------------------------\n"
                "Choose a command:")
    print(val)
    if val == '1':
        create()
    elif val == '2':
        build()
    elif val == '3':
        if os.path.isfile(os.path.join(settings.WORKING_DIR, 'alveolus-config.ini')):
            clean()
        else:
            print("alveolus: Configuration file not found, try alveolus-create first.")
    else:
        print("alveolus: Not a command")
    sys.exit()


def build():
    new_settings = Settings()
    new_settings.create_alveolus_cofig()
    new_settings.clean_config()
    new_settings.parse_doxy_config()
    new_settings.parse_sphinx_config()

    if hooks.doxy_build(new_settings):
        hooks.sphinx_build(new_settings)
    settings.delete_files_safe(['index.rst', 'doxygen.conf', 'Makefile', 'make.bat', 'conf.py'])

    sys.exit()


def create():
    copy2(os.path.join(settings.SOURCE_DIR, "alveolus-config.ini"),
          os.path.join(settings.WORKING_DIR, "alveolus-config.ini"))

    sys.exit()


def clean():
    new_settings = Settings()
    new_settings.clean_config()


if __name__ == '__main__':
    main()
