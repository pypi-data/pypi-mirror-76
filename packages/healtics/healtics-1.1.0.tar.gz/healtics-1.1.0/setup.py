from setuptools import setup

setup(
        name='healtics',
        version='1.1.0',
        py_modules= ['healtics','setup_matplotlib'],
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
