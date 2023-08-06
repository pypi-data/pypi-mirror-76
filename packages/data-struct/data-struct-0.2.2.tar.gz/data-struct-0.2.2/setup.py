import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data-struct",
    version="0.2.2",
    author="Eddie Breeg",
    license="GPLv3",
    author_email="eddiebreeg0@protonmail.com",
    description="A class to help you handling complex JSON-like objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EddieBreeg/structLib",
    py_modules=['structLib'],
    package_dir={'': "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        # eg: "aspectlib==1.1.1", "six>=1.7",
    ],
    extras_require={
        'dev': ["pytest>=6.0.1"],
    },
)
