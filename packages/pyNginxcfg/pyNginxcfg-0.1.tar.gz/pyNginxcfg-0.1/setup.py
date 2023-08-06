import setuptools

setuptools.setup(
    name='pyNginxcfg',
    version='0.1',
    author="Gallay David",
    author_email="davidtennis96@hotmail.com",
    description="A tool to handle nginx configuration",
    setup_requires=['setuptools-markdown'],
    long_description_content_type="text/markdown",
    long_description_markdown_filename='README.md',
    url="https://github.com/divad1196/pyNginx",
    packages=setuptools.find_packages(),
    install_requires=[
        "schema",
        "validators",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
)