# Relatório Votometro A Volta a Portugal em Eleicoes

## Introdução

O presente projeto foi desenvolvido no âmbito da unidade curricular de programação IV da Licenciatura em Engenharia Informática do Instituto de Tecnologias Avançadas de Lisboa, pelos alunos **Eduardo Maio, Rodrigo Courela e Diogo Oliveira**. O objetivo principal consiste na simulação de eleições legislativas em Portugal, abrangendo a votação aleatória por concelho e distrito, o cálculo de totais nacionais e distritais, e a apresentação dos resultados através de uma aplicação web interativa.
Com este trabalho pretendeu-se não só consolidar os conhecimentos adquiridos em Python, mas também aplicar técnicas de manipulação de dados, criação de ficheiros e visualização gráfica, recorrendo a bibliotecas e boas práticas de desenvolvimento e promovendo o trabalho em equipa.

---

## Estrutura e Funcionamento do Projeto

O projeto está dividido em 3 módulos, cada um com responsabilidades bem definidas:

### 1. Simulação dos Votos (`simular_votos.py`)

- **Geração dos Pesos por Partidos:** Cada partido recebe um peso aleatório, simulando cenários eleitorais realistas onde alguns partidos são mais populares que outros.
- **Distribuição dos Votos:** Para cada concelho, os votos são distribuídos proporcionalmente por partidos, garantindo que o número total de votos não ultrapasse o numero total de inscritos por concelho.
- **Persistência dos Resultados:** Os resultados são guardados em ficheiros Excel e JSON, organizados por concelho e distrito.

### 2. Validação dos Resultados (`validacao_votos.py`)

- **Validação de Ficheiros:** Permite revalidar e reprocessar os resultados de forma a garantir que não existe duplicação de dados para o mesmo concelho, de forma a assegurar que os ficheiros gerados correspondem ao esperado e garantindo ao utilizador a opção de sobrescrever os dados antigos.
- **Cálculo de Totais:** São calculados e adicionados totais por distrito e a nível nacional, facilitando a análise agregada dos resultados.


### 3. Visualização dos Resultados (`apresentacao_resultados.py`)

- **Aplicação Web com Streamlit:** Permite ao utilizador explorar os resultados das eleições de forma interativa, escolhendo distrito e concelho.
- **Gráficos Interativos:** Utilização da biblioteca Plotly para apresentar os resultados em diferentes tipos de gráficos (barras, circular, linha).
- **Identificação dos Vencedores:** O sistema destaca o partido vencedor a nível nacional e apresenta o respetivo candidato, sendo este o novo primeiro ministro de portugal.
- **Filtros e Totais Especiais:** Inclui funcionalidades para visualizar totais nacionais, distritais e casos especiais como votos “Fora de Portugal” na Europa ou Fora da Europa.

---

## Tecnologias e Bibliotecas Utilizadas

- **Python 3**
- **Pandas:** Para manipulação e análise de dados.
- **Streamlit:** Para criação da interface web interativa.
- **Plotly:** Para visualização gráfica dos resultados.
- **Excel/JSON:** Para armazenamento e partilha dos resultados.

---

## Pontos de Destaque

- **Simulação aleatória realista :** O sistema simula cenários eleitorais plausíveis, permitindo explorar diferentes distribuições de votos.
- **Flexibilidade:** Permite re-simular, validar e analisar resultados a vários níveis.
- **Visualização Moderna:** A interface gráfica facilita a compreensão dos resultados e torna a experiência do utilizador mais rica.
- **Organização Modular:** O código está segmentado em módulos, facilitando a manutenção e a evolução futura do projeto.

---

## Estrutura do Projeto

A estrutura do projeto é a seguinte:

- **README.md:** Documento de apresentação do projeto, com instruções de instalação, execução e descrição geral do funcionamento.
- **TODO.md:** Lista de tarefas pendentes, melhorias e sugestões para desenvolvimento futuro.
- **simular_votos.py:** Código responsável pela geração dos votos aleatórios e distribuição pelos partidos.
- **validacao_votos.py:** Código dedicado à validação e revalidação dos votos simulados.
- **apresentacao_resultados.py:** Código dedicado à visualização interativa dos resultados.
- **apresentacao_resultados_test.py, simular_votos_test.py:** Scripts de teste para garantir o correto funcionamento dos módulos principais.
- **Docs/**: Pasta com ficheiros de configuração (partidos, distritos, concelhos).
- **ResultadoEleicoesDistritos/**: Pasta onde são guardados os resultados por concelho e distrito (Excel, JSON).
- **ResultadosFinais/**: Pasta para os ficheiros finais agregados e prontos para visualização.

A existência dos ficheiros `README.md` e `TODO.md` demonstra a preocupação com a documentação e o planeamento do desenvolvimento, facilitando a manutenção e a futura evolução do projeto.

---

## Conclusão

Este projeto permitiu aos autores aplicar e aprofundar os conhecimentos de Python Adquiridos na disciplina de Programação IV, especialmente nas áreas de manipulação de dados, automação de tarefas e visualização gráfica. A simulação de eleições legislativas em Portugal revelou-se um excelente exercício prático, integrando conceitos de random, persistência de dados e desenvolvimento de interfaces gráfica.

Acreditamos que o sistema desenvolvido pode servir como base para futuras simulações, análises ou até mesmo para fins educacionais noutras cadeiras.
O trabalho em equipa, a divisão de tarefas e a resolução de desafios técnicos contribuíram de forma significativa para o nosso crescimento académico e profissional.

---

**Autores:**  
Eduardo Maio, Rodrigo Courela, Diogo Oliveira  
Disciplina de Programação IV 
Licenciatura em Engenharia Informática — ISTEC Lisboa  
Junho de 2025