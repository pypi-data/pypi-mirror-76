import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ketool",  # Replace with your own username
    version="0.0.3",
    author="Liuke",
    author_email="821711401@qq.com",
    keywords=['python', 'KeTool'],
    description="A set of tools that make coding more simpler for python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liukecode/ketool.git",
    packages=setuptools.find_packages(),
    platforms=["all"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
