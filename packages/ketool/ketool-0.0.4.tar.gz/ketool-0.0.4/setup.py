import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ketool",  # Replace with your own username
    version="0.0.4",
    author="Liuke",
    author_email="",
    keywords=['python', 'KeTool'],
    description="A set of tools that make coding more simpler for python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liukecode/ketool.git",
    packages=setuptools.find_packages(),
	install_requires = [
    'xlrd',
    'xlwt',
	'xlutils',
	'openpyxl',
    ],
    platforms=["all"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
