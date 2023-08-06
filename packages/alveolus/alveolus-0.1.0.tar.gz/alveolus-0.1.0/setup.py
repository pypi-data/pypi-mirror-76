import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="alveolus",
    version="0.1.0",
    author="Ioannis Kozaris",
    author_email="ioanniskozaris@gmail.com",
    description="Alveolus Docs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnkozaris/alveolus",
    packages=['alveolus', 'exhale'],
    package_dir={'alveolus': 'alveolus', 'exhale': 'exhale'},
    package_data={"alveolus": ["tools/*"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Environment :: MacOS X",
        "Framework :: Sphinx",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Programming Language :: C++",
        "Operating System :: OS Independent",
        "Topic :: Documentation",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Software Development :: Documentation"
    ],
    license='MIT',
    keywords='documentation sphinx doxygen C++ docs',
    install_requires=['sphinx', 'breathe'],
    python_requires='~=3.3',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'alveolus-build=alveolus.main:build',
            'alveolus-create=alveolus.main:create',
            'alveolus-clean=alveolus.main:clean',
            'alveolus-cli=alveolus.main:main',
        ],
    },

)
