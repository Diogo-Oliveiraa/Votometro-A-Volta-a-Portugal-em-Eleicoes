# Makefile Votometro para Windows PowerShell

VENV_DIR = .venv
PYTHON = $(VENV_DIR)\Scripts\python.exe
PIP = $(VENV_DIR)\Scripts\pip.exe

.DEFAULT_GOAL := all

.PHONY: venv install-deps simular validar streamlit lint all clean

# Criar ambiente virtual se não existir
venv:
	@if not exist "$(VENV_DIR)" ( \
		echo Criando ambiente virtual $(VENV_DIR)... & \
		python -m venv $(VENV_DIR) \
	) else ( \
		echo Ambiente virtual $(VENV_DIR) já existe. \
	)

# Instalar dependências com o script requirements.py
install-deps: venv
	@echo Instalando dependências com $(PYTHON) Documentação\requirements.py
	$(PYTHON) Documentação\requirements.py
	@echo Dependências instaladas.

# Simular votos (resposta automática 's')
simular: install-deps
	@echo A simular votos...
	echo s | $(PYTHON) simular_votos.py

# Validar votos
validar: install-deps
	@echo A validar votos...
	$(PYTHON) validacao_votos.py

# Executar app Streamlit em background
streamlit: install-deps
	@echo A executar Streamlit em background...
	start /b $(PYTHON) -m streamlit run apresentacao_resultados.py > streamlit.log 2>&1

# Executar pylint nos ficheiros principais
lint: install-deps
	@echo Executar pylint...
	$(PYTHON) -m pylint apresentacao_resultados.py simular_votos.py validacao_votos.py

# Fazer tudo em sequência
all: install-deps simular validar streamlit lint
	@echo === Tudo concluído ===

# Limpar ambiente virtual (opcional)
clean:
	@echo Removendo ambiente virtual $(VENV_DIR)...
	rmdir /s /q $(VENV_DIR)
	@echo Limpeza concluída.