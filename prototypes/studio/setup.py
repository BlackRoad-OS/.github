from setuptools import setup, find_packages

setup(
    name="blackroad-studio",
    version="0.1.0",
    description="BlackRoad Studio - Form Builder & Project Studio CLI",
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "studio=studio.cli:main",
        ],
    },
)
