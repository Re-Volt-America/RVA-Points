import setuptools
import os

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

content = {}
with open(os.path.join("rv_launcher", "version.py")) as f:
    exec(f.read(), content)

setuptools.setup(
    name="rva-points",
    version=content["__version__"],
    author="BGM",
    author_email="jose@bgmp.cl",
    description="Points calculator for Re-Volt America",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Re-Volt-America/RVA-Points",
    packages=setuptools.find_packages(),
    py_modules=["rvgl_launcher"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License",
        "Operating System :: OS Independent",
        "Development Status :: alpha"
    ],
    python_requires='>=3.8',
    install_requires=['wx', 'yaml', 'pyinstaller']
)
