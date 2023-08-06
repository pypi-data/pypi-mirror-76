import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tamagotchi_tandersen", # Replace with your own username
    version="1.0.1",
    author="Tristan Andersen",
    description="My attempt at the Tamagotchi challenge",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tristan-Andersen/Tamagotchi-challenge",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['*.jpg'],
    '': ['*.png']
    },
    install_requires=['pygame'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='==3.6'
)