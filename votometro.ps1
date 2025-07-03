# votometro.ps1
#requires -version 5.0

param (
    [string]$target = "all"
)

# Variáveis
$VENV_DIR = ".venv"
$PYTHON = "$VENV_DIR\Scripts\python.exe"
$PIP = "$VENV_DIR\Scripts\pip.exe"

function Criar-Venv {
    if (-Not (Test-Path $VENV_DIR)) {
        Write-Output "A criar ambiente virtual $VENV_DIR..."
        python -m venv $VENV_DIR
    } else {
        Write-Output "Ambiente virtual $VENV_DIR já existe."
    }
}

function Instalar_Dependencias {
    Write-Output "A Instalar dependências com $PYTHON Documentação\requirements.py"
    & $PYTHON Documentação\requirements.py
    Write-Output "Dependências instaladas."
}

function Simular_Votos {
    Write-Output "A simular votos..."
    "s" | & $PYTHON simular_votos.py
}

function Validar_Votos {
    Write-Output "A validar votos..."
    & $PYTHON validacao_votos.py
}

function Run-Streamlit {
    Write-Output "A executar Streamlit em background..."
    Start-Process -NoNewWindow -FilePath $PYTHON -ArgumentList "-m streamlit run apresentacao_resultados.py" -RedirectStandardOutput "streamlit.log" -RedirectStandardError "streamliterror.log"
}

function Run-Lint {
    Write-Output "A executar pylint..."
    $files = @(
        "apresentacao_resultados.py",
        "simular_votos.py",
        "validacao_votos.py"
    )
    foreach ($file in $files) {
        if (Test-Path $file) {
            Write-Output "`n-- $file --"
            & $PYTHON -m pylint $file
        } else {
            Write-Warning "Ficheiro não encontrado: $file"
        }
    }
}

function Run-Coverage {
    Write-Output "A correr testes com coverage..."
    & $PYTHON -m coverage erase
    & $PYTHON -m coverage run -m unittest discover
    & $PYTHON -m coverage report
    & $PYTHON -m coverage html
    if (Test-Path "htmlcov\index.html") {
        Start-Process "htmlcov\index.html"
    } else {
        Write-Warning "Relatório HTML não foi gerado."
    }
}

function Clean-Venv {
    Write-Output "Removendo ambiente virtual $VENV_DIR..."
    Remove-Item -Recurse -Force $VENV_DIR
    Write-Output "Limpeza concluída."
}

function Run-All {
    Criar-Venv
    Instalar_Dependencias
    Simular_Votos
    Validar_Votos
    Run-Streamlit
    Run-Lint
    Run-Coverage
    Write-Output "=== Tudo concluído ==="
}

switch ($target.ToLower()) {
    "venv"           { Criar-Venv }
    "install-deps"   { Criar-Venv; Instalar_Dependencias }
    "simular"        { Criar-Venv; Instalar_Dependencias; Simular_Votos }
    "validar"        { Criar-Venv; Instalar_Dependencias; Validar_Votos }
    "streamlit"      { Criar-Venv; Instalar_Dependencias; Run-Streamlit }
    "lint"           { Criar-Venv; Instalar_Dependencias; Run-Lint }
    "coverage"       { Criar-Venv; Instalar_Dependencias; Run-Coverage }
    "all"            { Run-All }
    "clean"          { Clean-Venv }
    default          { Write-Output "Target desconhecido: $target" }
}