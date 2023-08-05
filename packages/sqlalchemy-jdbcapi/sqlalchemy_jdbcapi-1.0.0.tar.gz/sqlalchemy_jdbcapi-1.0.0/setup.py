import os
import re

from setuptools import setup, find_packages

v = open(
    os.path.join(
        os.path.dirname(__file__), "sqlalchemy_jdbcapi", "__init__.py"
    )
)
VERSION = re.compile(r'.*__version__ = "(.*?)"', re.S).match(v.read()).group(1)
v.close()

readme = os.path.join(os.path.dirname(__file__), "README.rst")

DESCRIPTION = "Python SQLAlchemy Dialect for JDBCAPI."

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="sqlalchemy_jdbcapi",
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Danesh Patel",
    author_email="danesh_patel@outlook.com",
    license="Apache",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Database :: Front-Ends",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(include=["sqlalchemy_jdbcapi"]),
    include_package_data=True,
    install_requires=["SQLAlchemy", "JayDeBeApi"],
    zip_safe=False,
    keywords="SQLAlchemy JDBCAPI Dialect",
    entry_points={
        "sqlalchemy.dialects": [
            "jdbcapi.pgjdbc = sqlalchemy_jdbcapi.pgjdbc:PGJDBCDialect",
            "jdbcapi.oraclejdbc = sqlalchemy_jdbcapi.oraclejdbc:OracleJDBCDialect",
        ]
    },
)
