from setuptools import setup, find_packages

setup(
    name="PaperPlumber",
    version="0.0.1",
    author="Carlos Outeiral, Shuxiang Cao",
    author_email="carlos.outeiral@stats.ox.ac.uk, shuxiang.cao@physics.ox.ac.uk",
    description="A package for LLM-powered paper data mining.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/OxfordSchmidtAIFellows/paper-plumber",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires='>=3.9',
    install_requires=[
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.4',
        ]
    },
    include_package_data=True,
)
