import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rasa-plus",
    version="0.3.1",
    author="Alexandre Augusto de Sá dos Santos",
    author_email="alexandrebarbaruiva@gmail.com",
    description="An organizer for your rasa bot dialogs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexandrebarbaruiva/rasa-plus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    py_modules=["rasa_plus.__main__"],
    install_requires=["Click"],
    entry_points="""
        [console_scripts]
        rasa_plus=rasa_plus.__main__:rasa_plus
    """,
)
