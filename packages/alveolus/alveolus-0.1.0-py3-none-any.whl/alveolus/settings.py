import os
from configparser import RawConfigParser
from shutil import copy2
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKING_DIR = os.getcwd()
DOXYGEN_OUT_DIR = 'doxygen'


def delete_files_safe(files):
    for file in files:
        if os.path.isfile(file):
            os.remove(file)


def _delete_dirs_safe_(dirs):
    for directory in dirs:
        if os.path.isdir(directory):
            os.system("rm -rf " + directory)


class Settings:
    proj_name = "Alveolus Project"
    proj_version = "0.0.0"
    proj_src_input = "./"
    proj_exclude = ""
    proj_output = "./output"
    proj_api = "./doc_src"

    def __init__(self):
        main_conf_parser = RawConfigParser()
        main_conf_parser.optionxform = str
        try:
            if os.path.isfile(os.path.join(WORKING_DIR, 'alveolus-config.ini')):
                config_file = os.path.join(WORKING_DIR, 'alveolus-config.ini')
                print('alveolus: Using custom configuration file')
            else:
                config_file = os.path.join(SOURCE_DIR, 'alveolus-config.ini')
                print('alveolus: Using default configuration file')

            main_conf_parser.read(config_file)
            self.proj_name = main_conf_parser['PROJECT']['name']
            self.proj_version = main_conf_parser['PROJECT']['version']
            self.proj_src_input = main_conf_parser['CONFIG_DIRECTORIES']['src_code']
            self.proj_exclude = main_conf_parser['CONFIG_DIRECTORIES']['exclude']
            self.proj_output = main_conf_parser['CONFIG_DIRECTORIES']['output']
            self.proj_api = main_conf_parser['CONFIG_DIRECTORIES']['src_api']
        except Exception as e:
            print("alveolus: Failed to read .ini file- REASON: " + str(e))
            print("alveolus: Using default config values")

    def create_alveolus_cofig(self):
        if os.path.isdir(self.proj_api):
            print('alveolus: Docs source Folder Found')
        else:
            os.mkdir(self.proj_api)

    def clean_config(self):
        _delete_dirs_safe_([os.path.join(*[self.proj_api, "doxygen_src"]), self.proj_output])
        delete_files_safe(['index.rst', 'doxygen.conf', 'Makefile', 'make.bat', 'conf.py'])

    def parse_doxy_config(self):
        doxy_parser = RawConfigParser()
        doxy_parser.optionxform = str

        with open(os.path.join(SOURCE_DIR, "tools/doxygen.conf.in")) as stream:
            doxy_parser.read_string("[DEFAULT]\n" + stream.read())
            doxy_parser.set('DEFAULT', 'PROJECT_NAME', self.proj_name)
            doxy_parser.set('DEFAULT', 'PROJECT_NUMBER', self.proj_version)
            doxy_parser.set('DEFAULT', 'OUTPUT_DIRECTORY', os.path.join(self.proj_output, DOXYGEN_OUT_DIR))
            doxy_parser.set('DEFAULT', 'INPUT', self.proj_src_input)
            doxy_parser.set('DEFAULT', 'EXCLUDE', self.proj_exclude)
        with open('doxygen.conf', 'w') as doxyfile:
            doxy_parser.write(doxyfile)
        print("alveolus: Doxygen Config file created")

    def parse_sphinx_config(self):
        proj_rsts = ""
        for file in os.listdir(self.proj_api):
            if file.endswith(".rst"):
                proj_rsts += " " + os.path.join(self.proj_api, file) + '\n'
        proj_rsts += " " + os.path.join(*[self.proj_api, "doxygen_src", "library_root"])

        with open(os.path.join(SOURCE_DIR, "tools/index.rst.in"), "rt") as sphinxIndex:
            with open("index.rst", "wt") as parsed_index:
                new_index = sphinxIndex.read() \
                    .replace("@Title", self.proj_name) \
                    .replace("@toctree_depth", "1") \
                    .replace("@MainDescription", "")
                if proj_rsts is not None:
                    new_index = new_index.replace("@toctree_include", proj_rsts)
                else:
                    new_index.replace("@toctree_include", " ")
                parsed_index.write(new_index)

        with open(os.path.join(SOURCE_DIR, "tools/Makefile.in"), "rt") as sphinxMakefile:
            with open("Makefile", "wt") as parsed_makefile:
                new_makefile = sphinxMakefile.read() \
                    .replace("@source", self.proj_api) \
                    .replace("@output", self.proj_output) \
                    .replace("@exhale", self.proj_api + "/doxygen_src")
                parsed_makefile.write(new_makefile)

        copy2(os.path.join(SOURCE_DIR, "conf.py"), os.path.join(WORKING_DIR, "conf.py"))

        # IF WINDOWS
        # with open("./tools/make.bat.in", "rt") as sphinxbat:
        #     with open("./make.bat", "wt") as parsed_bat:
        #         new_index = sphinxMakefile.read() \
        #             .replace("@source", proj_api) \
        #             .replace("@output", proj_output) \
        #         parsed_makefile.write(new_index)
        #
        # print("doxygen config file created")
