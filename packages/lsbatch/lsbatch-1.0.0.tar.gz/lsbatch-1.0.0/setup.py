from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='lsbatch',
    version='1.0.0',
    packages=setuptools.find_packages(),
    package_data={
        'lsbatch': ['*'],
        'lsbatch.lsq_batch_template': ['*']
    },
    author="MarketXpander Services Pvt. Ltd.",
    author_email="mangesh@leadsquared.com",
    description="lsbatch LeadSuared provided Batch Jobs software development kit. This allows developers to code and test Batch Jobs offline.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'lsbatch = lsbatch.__main__:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
