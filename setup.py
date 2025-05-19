from setuptools import setup, find_packages

setup(
    name="architectum-new",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "arch=arch_blueprint_generator.cli.commands:app",
        ],
    },
)
