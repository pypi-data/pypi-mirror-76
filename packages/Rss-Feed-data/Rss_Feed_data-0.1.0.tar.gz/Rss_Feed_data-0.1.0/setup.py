import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
#README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Rss_Feed_data",
    version="0.1.0",
    description="Fecha data from rss feed urls",
   # long_description=README,
   # long_description_content_type="text/markdown",
   # url="https://github.com/realpython/reader",
    author="Ramkiran",
   # author_email="office@realpython.com",
    license="MIT",
    classifiers=[
        #"License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        #"Programming Language :: Python :: 3.7",
    ],
    packages=["Rss_Feed_data"],
    #include_package_data=True,
    install_requires=["logging", "datetime","os","urllib","validators","BeautifulSoup","pandas","socket"],
   # entry_points={
    # "console_scripts": [
    #        "realpython=reader.__main__:main",
    #    ]
    #},
)
