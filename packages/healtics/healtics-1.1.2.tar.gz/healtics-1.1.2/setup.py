from setuptools import setup

setup(
        name='healtics',
        version='1.1.2',
        packages = [
                "healtics",
            ],
        package_data     = {
            "": [
                "*.txt",
                "*.md",
                "*.rst",
                "*.py"
                ]
            },
        install_requires = [
                "healpy",
                "matplotlib",
            ],
        license='Creative Commons Attribution-Noncommercial-Share Alike license',
        long_description=open('README.md').read(),
        )
