from pathlib import Path
import setuptools

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="Kingfish",
    version="0.1.1",
    description="My first published package",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Geulmaster/Kingfish",
    author="Eyal Geulayev",
    author_email="eyal.geulayev@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["Core", "DBs", "Special", "Wrapper"],
    include_package_data=True,
    install_requires=["pymongo", "paramiko", "psycopg2-binary"],
    python_requires='>=3.6',
    entry_points={
    },
)