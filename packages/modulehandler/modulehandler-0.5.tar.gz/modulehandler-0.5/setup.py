import setuptools

setuptools.setup(
    name="modulehandler",
    version="0.5",
    author="Gallay David",
    author_email="davidtennis96@hotmail.com",
    description="A dynamic module handler, with standalone tools",
    setup_requires=['setuptools-markdown'],
    long_description_content_type="text/markdown",
    long_description_markdown_filename='README.md',
    url="https://github.com/divad1196/ModuleHandler",
    packages=setuptools.find_packages(),
    install_requires=[
        "markdown",
        "pydantic",
        "typing",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
