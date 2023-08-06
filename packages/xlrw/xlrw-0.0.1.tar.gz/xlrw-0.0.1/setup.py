import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xlrw",  # Replace with your own username
    version="0.0.1",
    author="Liuke",
    author_email="",
    keywords=['python', 'xlrw'],
    description="xlrw is a Python library to read/write Excel files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liukecode/xlrw.git",
    packages=setuptools.find_packages(),
	include_package_data=True,
	install_requires = [
    'xlrd',
    'xlwt',
	'xlutils',
	'openpyxl',
    ],
    platforms=["any"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
