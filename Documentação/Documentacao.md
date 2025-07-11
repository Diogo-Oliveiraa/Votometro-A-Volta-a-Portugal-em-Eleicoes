# Documentação Votometro A Volta a Portugal em Eleicoes

### Descrição

Este projeto simula votos, valida os dados e apresenta os resultados numa interface interativa.

---

### Bibliotecas utilizadas

O projeto usa as seguintes bibliotecas Python:

```python
import os
import time
import unicodedata
import pandas
import plotly.express
import streamlit
import random
import json
```

Destas, as seguintes são externas e precisam de instalação manual:

- `pandas`
- `plotly`
- `streamlit`

### Instalação das bibliotecas externas

Para instalar as bibliotecas externas, executa:

```bash
pip3 install -r requirements.txt # Para Python 3
ou
pip install -r requirements.txt
```

Caso já tenha a biblioteca OS instalada pode correr o ficheiro Bibliotecas.py

```bash
python3 requirements.py
ou
python requirements.py
```

Caso pretenda criar um ambiente virtual

No terminal, execute a seguinte linha
```bash
python3 -m venv venv
```
---
### Como executar de forma simples e automática 

Executar o script.

```bash
   make all
   ```
Este cria um ambiente virtual e instala todas as bibliotecas necessárias para a execução do projeto
e executa o mesmo automaticamente.

Apos terminar executar o seguinte script

```bash
   make clean
   ```

Este limpa e elemina o ambiente virtual criado bem como todos os dados gerados nessa sessão.

### Como executar o projeto passo a passo 

Execute os scripts pela seguinte ordem para garantir o funcionamento correto:

1. **Simular votos**  
   Executar o script que gera a simulação dos votos:  
   ```bash
   python simular_votos.py
   ```

2. **Validar votos**  
   Executar o script que valida os dados simulados:  
   ```bash
   python validacao_votos.py
   ```

3. **Apresentar resultados**  
   Executar a interface gráfica para visualização dos resultados:  
   ```bash
   streamlit run apresentacao_resultados.py
   ```

---

### Obrigado por testares o nosso projeto!
