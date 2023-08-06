PYV=$(python -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)")

if [ -z "${PYV}" ]; then
  echo "Python in not Installed"
else
  echo "Python Version" "$PYV"
fi

DOV=$(doxygen -v)
if [ -z "${DOV}" ]; then
  echo "Doxygen in not Installed"
else
  echo "Doxygen Version" "$DOV"
fi

SPV=$(python -c "import pkg_resources;print(pkg_resources.get_distribution('sphinx').version)")
if [ -z "${SPV}" ]; then
  echo "Sphinx in not Installed"
else
  echo "Sphinx Version" "$SPV"
fi

BRV=$(python -c "import pkg_resources;print(pkg_resources.get_distribution('breathe').version)")
if [ -z "${BRV}" ]; then
  echo "Breathe in not Installed"
else
  echo "Breathe Version" "$BRV"
fi

EXV=$(python -c "import pkg_resources;print(pkg_resources.get_distribution('exhale').version)")
if [ -z "${EXV}" ]; then
  echo "Exhale in not Installed"
else
  echo "Exhale Version" "$EXV"
fi
