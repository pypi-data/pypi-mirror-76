import logging
import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
project_path = here
readme_path = os.path.join(project_path, "README.md")

sys.path.insert(0, here)

logging.basicConfig(stream=sys.stderr, level=logging.INFO)


def read_file(path):
    with open(path, "r") as fp:
        return fp.read()


def install_requires():
    requirements = read_file(os.path.join(project_path, "requirements.txt")).split("\n")
    requirements = list(filter(lambda s: not not s, map(lambda s: s.strip(), requirements)))

    return requirements


def main():
    import hathor.__about__ as __about__

    setup(
        name="hathor",
        author=__about__.author_name,
        author_email=__about__.author_email,
        version=__about__.package_version,
        description=__about__.package_description,
        license=__about__.package_license,
        long_description=read_file(readme_path),
        long_description_content_type="text/markdown",
        url=__about__.package_repository,
        classifiers=[
            "Development Status :: 4 - Beta",
            "Programming Language :: Python :: 3.8"
        ],
        keywords=["roblox", "studio", "lua", "build-tool", "build", "tool"],
        packages=find_packages(".", exclude=[
            "tests",
            "tests.*"
        ]),
        package_dir={"": "."},
        include_package_data=True,
        python_requires=">=3.8",
        install_requires=install_requires(),
        entry_points={
            "console_scripts": [
                "hathor=hathor.__main__:cli",
            ]
        }
    )


if __name__ == '__main__':
    main()
