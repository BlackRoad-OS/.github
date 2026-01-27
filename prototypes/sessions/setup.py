from setuptools import setup, find_packages

setup(
    name="blackroad-sessions",
    version="0.1.0",
    description="Session management, collaboration, and shared memory for BlackRoad mesh",
    author="BlackRoad OS",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - uses only stdlib
    ],
    entry_points={
        "console_scripts": [
            "blackroad-sessions=sessions.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
