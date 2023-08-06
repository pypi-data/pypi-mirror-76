import subprocess
import importlib.util

def check_dependencies():
    try:
        result = subprocess.run(['doxygen', '-v'], stdout=subprocess.PIPE)
    except OSError as e:
        print(e)
        print("Doxygen not installed or not in path. Cannot continue")
    else:
        doxygen_version = str(result.stdout).replace("\\n", "").strip('b')
        print("Doxygen Version " + doxygen_version)

    spam_spec = importlib.util.find_spec('sphinx')
    if spam_spec is not None:
        try:
            result = subprocess.run(['sphinx-build', '--version'], stdout=subprocess.PIPE)
        except OSError as e:
            print(e)
            print("Sphinx not in path. Cannot continue")
        else:
            sphinx_version = str(result.stdout).replace("\\n", "").strip('b\'sphinx-build')
            print("Sphinx Version " + sphinx_version)
    else:
        print("Sphinx not installed. Cannot continue")