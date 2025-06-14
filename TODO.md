## TODO

## 📁 Estrutura Inicial
- [x] Criar estrutura de diretórios:
  - [x] `Docs/`
  - [x] `resultadosEleicoesDistritos/`
  - [x] `resultadosFinais/`
  - [x] `Tests/`
- [x] Criar `requirements.txt` com bibliotecas necessárias:
    - [x] `pandas`, `matplotlib`, `openpyxl`, `json`, etc.

---

## 🗳️ Módulo: Simulação dos Votos
- [x] Obter dados reais dos inscritos por concelhos e distritos-
- [x] Criar script que simule votos por:
  - [x] Partido político
  - [x] Votos brancos
  - [x] Votos nulos
- [x] Armazenar resultados por:
  - [x] Distrito
- [x] Exportar resultados em:
  - [x] JSON
  - [x] Xlsx
- [x] Adicionar delays durante a simulação dos dados (opcional)
- [x] Enviar dados ao servidor da CNE (ficheiro, API ou socket)

---

## ✅ Módulo: Verificação dos Votos
- [x] Receber dados das votações
- [x] Validar dados recebidos
- [x] Calcular:
  - [x] Abstenção por concelho/distrito
  - [x] Abstenção total
- [x] Exportar resultados em:
  - [x] Xlsx

---

## 🖥️ Módulo: Apresentação dos Resultados
- [x] Apresentação dos resultados - Distrito
- [x] Apresentação dos resultados - Concelho
- [x] Apresentação dos resultados - Fora da Europa
- [x] Apresentação dos resultados - Europa
- [x] Apresentação dos resultados totais - Portugal
- [x] Apresentação grafica
  - [x] Barras
  - [x] Circular
  - [x] Linhas
- [x] Apresentação Deputado Eleito
- [ ] Geo referênciados com cores distintas para os “vencedores”
- [ ] Comparação com uma outra eleição
