import os
from alveolus import settings
import subprocess


def doxy_build(current_settings=settings.Settings):
    try:
        subprocess.run(['doxygen', '-v'], stdout=subprocess.PIPE)
    except OSError as e:
        print(e)
        print("alveolus: Doxygen not installed or not in PATH. Cannot continue")
        return False
    else:
        if not os.path.isdir(current_settings.proj_output):
            os.mkdir(current_settings.proj_output)
        if not os.path.isdir(os.path.join(current_settings.proj_output, settings.DOXYGEN_OUT_DIR)):
            os.mkdir(os.path.join(current_settings.proj_output, settings.DOXYGEN_OUT_DIR))
        if os.path.isfile(os.path.join(settings.WORKING_DIR, 'doxygen.conf')):
            subprocess.run(['doxygen', 'doxygen.conf'])
            return True
        else:
            print("doxygen.conf could not be created")
        return False


def sphinx_build(current_settings=settings.Settings):
    from sphinx.application import Sphinx
    srcdir = settings.WORKING_DIR
    confdir = settings.WORKING_DIR
    builddir = current_settings.proj_output
    doctreedir = os.path.join(builddir, "doctrees/")
    builder = "html"
    app = Sphinx(srcdir, confdir, builddir, doctreedir, builder)
    app.build()
