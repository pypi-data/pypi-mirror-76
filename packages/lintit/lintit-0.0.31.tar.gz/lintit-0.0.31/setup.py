import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

dependencies = [
    "click>7.1.2",
    "flake8>3.8.3",
    "black>19.10b0",
    "isort>5.0.9",
    "mypy>0.782",
    "autoflake>1.3.1",
]

setuptools.setup(
    name="lintit",
    version="0.0.31",
    author="Everton Tomalok",
    author_email="evertontomalok123@gmail.com",
    description="A cli linter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EvertonTomalok/lint-it",
    packages=setuptools.find_packages(exclude="tests"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'lintit = lint_it.linter:main',
        ],
    },
)
