## Votómetro: A Volta a Portugal em Eleições

## Simulação de Eleições Legislativas em Portugal (ISTEC - PIV)

Este projeto foi desenvolvido no âmbito da unidade curricular de **Programação 4 (PIV)** da Licenciatura em Engenharia Informática do **ISTEC**. O objetivo principal é consolidar os conhecimentos de **Python** através da construção de uma aplicação que **simula eleições legislativas em Portugal**.

---

## Objetivos do Projeto

- Simular o envio de resultados à **CNE** através de um sistema de votações
- Gerar votos em todos os níveis administrativos: freguesias, concelhos e distritos.
- Permitir a votação em partidos políticos, votos brancos e nulos.
- Calcular a taxa de abstenção e apresentar os resultados em vários formatos.

---

## Funcionalidades

### Simulação das Votações

- Gerar automáticamente os resultados da votação.
- Ligação de concelhos e distritos baseada em dados reais.
- Consideração de:
  - Votos válidos
  - Votos brancos
  - Votos nulos

### Servidor da CNE (Simulado)

- Aceite os resultados gerados da votação.
- Validação e arquivo dos dados.
- Calcula a abstenção por total nacional.
- Gera ficheiros de resultados em:
  - `.json`
  - `.xls`
  - Apresente os dados em Gráficos

### Servidor Público da CNE

- Permite consultas por:
  - Partido político
  - Votos brancos e nulos
- Decomposição dos resultados por:
  - Total nacional
  - Distritos
  - Concelhos