from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='chunkyp',
    version='0.0.2',
    license='apache-2.0',
    description='Ray-based preprocesisng pipeline.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/neophocion/chunkyp',
    download_url='https://github.com/neophocion/chunkyp/releases',
    author='Neo Phocion',
    author_email='neophocion@protonmail.com',
    keywords=['ray', 'preprocessing', 'nlp', 'cleaning', 'workflow'],
    packages=find_packages(),  # Required
    python_requires='>=3.5, <4',
    install_requires=[
        "ray>=0.8.6",
        "psutil>=5.7.0"
    ],
    extras_require={
        'dev': ["pytest"],
        'test': [],
    },

    package_data={
        'sample': [],
    },

    entry_points={
    },
    project_urls={
        'Repo': 'https://github.com/neophocion/chunkyp',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
      ],
)