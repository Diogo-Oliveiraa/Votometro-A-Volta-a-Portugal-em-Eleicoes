## TODO

## 📁 Estrutura Inicial
- [ ] Criar estrutura de diretórios:
    - [ ] `produtor/`
    - [ ] `servidor_cne/`
    - [ ] `servidor_publico/`
    - [ ] `dados/`
    - [ ] `docs/`
    - [ ]`testes/`
- [ ] Criar `requirements.txt` com bibliotecas necessárias:
    - [ ] `pandas`, `matplotlib`, `openpyxl`, `json`, etc.

---

## 🗳️ Módulo: Produtor (Simulação de Votos)
- [x] Obter dados reais de concelhos e distritos-
- [x] Criar script que simule votos por:
  - [x] Partido político
  - [x] Votos brancos
  - [x] Votos nulos
  - [x] Abstenção (calculada com base em nº de eleitores)
- [ ] Adicionar delays durante a simulação dos dados (opcional)
- [ ] Enviar dados ao servidor da CNE (ficheiro, API ou socket)

---

## 🖥️ Módulo: Servidor da CNE
- [ ] Receber dados das votações
- [ ] Validar dados recebidos
- [ ] Armazenar resultados por:
  - [ ] Concelho
  - [ ] Distrito
- [ ] Calcular:
  - [ ] Abstenção por concelho/distrito
  - [ ] Abstenção total
- [ ] Exportar resultados em:
  - [ ] JSON
  - [ ] xls
  - [ ] Form