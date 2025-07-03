import os

# Conteúdo das bibliotecas
bibliotecas = """
altair==5.5.0
astroid==3.3.9
attrs==25.3.0
blinker==1.9.0
cachetools==5.5.2
certifi==2025.4.26
charset-normalizer==3.4.2
click==8.2.1
contourpy==1.3.2
coverage==7.9.1
cycler==0.12.1
dill==0.3.9
elections==0.0.2
et_xmlfile==2.0.0
fonttools==4.58.0
geopandas==1.0.1
gitdb==4.0.12
GitPython==3.1.44
idna==3.10
isort==6.0.1
Jinja2==3.1.6
jsonschema==4.24.0
jsonschema-specifications==2025.4.1
kiwisolver==1.4.8
MarkupSafe==3.0.2
matplotlib==3.10.3
mccabe==0.7.0
narwhals==1.41.0
numpy==2.2.6
openpyxl==3.1.5
packaging==24.2
pandas==2.2.3
pillow==11.2.1
platformdirs==4.3.7
plotly==6.1.1
protobuf==6.31.0
pyarrow==20.0.0
pydeck==0.9.1
pylint==3.3.6
pyogrio==0.11.0
pyparsing==3.2.3
pyproj==3.7.1
python-dateutil==2.9.0.post0
pytz==2025.2
referencing==0.36.2
requests==2.32.3
rpds-py==0.25.1
setuptools==78.1.0
shapely==2.1.1
six==1.17.0
smmap==5.0.2
streamlit==1.45.1
tenacity==9.1.2
toml==0.10.2
tomlkit==0.13.2
tornado==6.5.1
typing_extensions==4.13.2
tzdata==2025.2
urllib3==2.4.0
"""

# Gravar no ficheiro requirements.txt
with open("requirements.txt", "w", encoding="utf-8") as f:
    f.write(bibliotecas.strip())

# Instalar com pip
print("A instalar as bibliotecas do requirements.txt...")
os.system("pip install -r requirements.txt")
print("Instalação completa.")
