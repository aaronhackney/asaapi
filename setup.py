import setuptools
import codecs
import os


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="asaapi",
    packages=setuptools.find_packages(),
    version=get_version("asaapi/__init__.py"),
    license="GPL 3.0 https://www.gnu.org/licenses/gpl-3.0.txt",
    description="Make api calls to a Cisco ASA",
    author="Aaron K. Hackney",
    author_email="aaron_309@yahoo.com",
    url="https://github.com/aaronhackney/asaapi",
    download_url="",
    install_requires=["requests>=2.26.0"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
