import setuptools

setuptools.setup(
    name="vavvy-sent-encoder", 
    version="0.0.1",
    author="Vavvy",
    author_email="vavvyox@gmail.com",
    description="This package contains the sentence encoder client implementation.",

    url="",
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)