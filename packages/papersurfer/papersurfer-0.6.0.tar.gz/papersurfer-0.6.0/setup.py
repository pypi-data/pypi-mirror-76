import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="papersurfer",
    version="0.6.0",
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Johann Jacobsohn",
    author_email="johann.jacobsohn@uni-hamburg.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["papersurfer"],
    include_package_data=True,
    install_requires=["requests", "mattermostdriver", "urwid", "configargparse"],
    entry_points={
        "console_scripts": [
            "papersurfer=papersurfer.papersurfer:main",
        ]
    },
)
