import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="rva-points",
    version="0.0.1-alpha",
    author="BGM",
    author_email="jose@bgmp.cl",
    description="Points calculator for Re-Volt America",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Re-Volt-America/RVA-Points",
    packages=setuptools.find_packages(),
    py_modules=["rva_points"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License AGPL-3.0",
        "Operating System :: OS Independent",
        "Development Status :: alpha"
    ],
    python_requires='>=3.8',
    install_requires=['wx', 'yaml', 'pyinstaller']
)
