import setuptools

with open("README.md", "r", encoding ='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="contexto", # Replace with your own username
    version="0.0",
    author="Departamento Nacional de Planeación - DNP",
    author_email="ucd@dnp.gov.co",
    description="Librería de análisis de texto",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ucd-dnp/contexto",
    packages=setuptools.find_packages(),
    include_package_data = True,
    license = 'MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6',
)