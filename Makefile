# Makefile  Votometro - execução automatizada

VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
COVERAGE = $(VENV_DIR)/bin/coverage

.DEFAULT_GOAL := all

.PHONY: venv install-deps lint coverage simular validar streamlit all clean

# Criar ambiente virtual se não existir
venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "A criar ambiente virtual $(VENV_DIR)..."; \
		python3 -m venv $(VENV_DIR); \
	else \
		echo "Ambiente virtual $(VENV_DIR) já existe."; \
	fi

run-script:
	source $(VENV_DIR)/bin/activate && python3 meu_script.py

# Instalar dependências com o script requirements.py
install-deps: venv
	@echo "Instalar dependências com $(PYTHON) Documentação/requirements.py"
	source $(VENV_DIR)/bin/activate && $(PYTHON) Documentação/requirements.py
	@echo "Dependências instaladas."

# Simular votos
simular: install-deps
	@echo "A simular votos..."
	source $(VENV_DIR)/bin/activate && yes s | $(PYTHON) simular_votos.py

# Validar votos
validar: install-deps
	@echo "A validar votos..."
	source $(VENV_DIR)/bin/activate && $(PYTHON) validacao_votos.py

# Executar app Streamlit em background
streamlit: install-deps
	@echo "A executar Streamlit em background..."
	source $(VENV_DIR)/bin/activate && nohup streamlit run apresentacao_resultados.py > streamlit.log 2>&1 &

# Executar pylint nos ficheiros principais
lint: install-deps
	@echo "Executar pylint..."
	source $(VENV_DIR)/bin/activate && pylint apresentacao_resultados.py simular_votos.py validacao_votos.py

coverage: install-deps
	@echo Executar testes com coverage...
	PYTHONPATH=. venv/bin/coverage run -m unittest discover -s Tests -p "*.py"; \
	venv/bin/coverage report; \
	venv/bin/coverage html -d tmp

# Fazer tudo em sequência
all: install-deps simular validar streamlit lint coverage 
	@echo "=== Tudo concluído ==="

# Limpar ambiente virtual (opcional)
clean:
	@echo "Remove ambiente virtual $(VENV_DIR)..."
	rm -rf $(VENV_DIR)
	@echo "Limpeza concluída."
