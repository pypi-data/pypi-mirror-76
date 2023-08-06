import setuptools


setuptools.setup(
    name='cd-utils-logger',
    version='1.0.0',
    packages=setuptools.find_packages(),
    url='https://github.com/herculanocm/cd-utils-logger',
    download_url='https://github.com/herculanocm/cd-utils-logger/archive/master.zip',
    license='MIT',
    author='Herculano Cunha',
    author_email='herculanocm@outlook.com',
    description='Utilitário para Log',
    keywords='tools utils logger',
    install_requires=['colorama'],
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
