# 📊 Dashboard Interativo de E-commerce

**Projeto final de Análise de Dados | Python, Pandas, Plotly e Dash**

## 1. Sobre o projeto

Este projeto transforma uma análise exploratória de dados de produtos de e-commerce em uma **aplicação web interativa**. Em vez de executar códigos Python ou abrir um notebook, o usuário final pode acessar um dashboard pelo navegador, consultar indicadores, aplicar filtros e explorar os gráficos.

A aplicação utiliza a base `ecommerce_estatistica.csv`, trabalhada nas etapas anteriores do projeto. O painel foi desenvolvido com **Dash** para a interface, **Plotly** para os gráficos, **Pandas** para a manipulação de dados e **NumPy** para os cálculos numéricos.

> **Objetivo:** facilitar a compreensão do catálogo de produtos e investigar como preços, avaliações, marcas, gênero e quantidade vendida se relacionam.

## 2. Funcionalidades

O painel apresenta quatro indicadores calculados de acordo com os filtros ativos:

| Indicador | O que representa |
|---|---|
| Produtos filtrados | Total de produtos na seleção atual |
| Preço médio | Média dos preços dos produtos selecionados |
| Nota média | Média das notas atribuídas aos produtos |
| Correlação: avaliações × vendas | Coeficiente de correlação linear entre número de avaliações e quantidade vendida codificada |

Há **dois filtros de seleção múltipla**, por **marca** e por **gênero**. Ao selecionar opções, os indicadores e os sete gráficos são atualizados automaticamente, sem recarregar a página. Se não houver registros correspondentes à combinação escolhida, o painel informa que não há dados para exibir.

## 3. Gráficos e perguntas respondidas

| Visualização | Dados utilizados | Finalidade |
|---|---|---|
| **1. Histograma** | `Preço` | Mostrar a distribuição dos preços e as faixas mais frequentes |
| **2. Dispersão** | `N_Avaliações` × `Qtd_Vendidos_Cod` | Examinar a associação entre número de avaliações e quantidade vendida |
| **3. Mapa de calor** | `Preço`, `Nota`, `N_Avaliações`, `Desconto`, `Qtd_Vendidos_Cod` | Comparar correlações entre indicadores numéricos |
| **4. Barras** | `Marca` | Mostrar as dez marcas com mais produtos na seleção |
| **5. Pizza** | `Gênero` | Visualizar a proporção de produtos por gênero; categorias com menos de dez registros são reunidas em “Outros” |
| **6. Densidade** | `Nota` | Visualizar a concentração das notas por estimativa de densidade (KDE) |
| **7. Regressão linear** | `N_Avaliações` × `Qtd_Vendidos_Cod` | Exibir os pontos observados e uma reta ajustada por mínimos quadrados |

Todos os gráficos apresentam títulos e identificação dos eixos quando aplicável. A visualização de densidade é calculada por uma estimativa de kernel gaussiano; a regressão utiliza `numpy.polyfit`.

**Importante sobre a interpretação:** `Qtd_Vendidos_Cod` é um indicador codificado/aproximado de vendas, não necessariamente uma contagem exata de unidades comercializadas. Correlações e a reta de regressão identificam associações nos dados, mas **não comprovam relações de causa e efeito**.

## 4. Base de dados e tratamento

A fonte de dados é o arquivo **`ecommerce_estatistica.csv`**, incluído na pasta do projeto.

O programa lê o CSV com `pandas.read_csv()` e:

- converte `Preço`, `Nota`, `N_Avaliações`, `Desconto` e `Qtd_Vendidos_Cod` para tipos numéricos, tratando valores inválidos como ausentes;
- substitui valores ausentes nas colunas `Marca` e `Gênero` por **“Não informado”**;
- aplica os filtros escolhidos aos registros antes de recalcular indicadores e gráficos;
- desconsidera valores numéricos ausentes nos cálculos e gráficos que dependem deles.

Essas operações são feitas em memória, **sem alterar o arquivo CSV original**.

## 5. Estrutura do projeto

```text
dashboard-ecommerce/
├── app.py                    # Aplicação Dash, filtros, indicadores e gráficos
├── ecommerce_estatistica.csv # Dados utilizados no painel
├── requirements.txt          # Bibliotecas necessárias
├── render.yaml               # Configuração de hospedagem no Render
├── .gitignore                # Arquivos ignorados pelo Git
└── README.md                 # Documentação do projeto
```

## 6. Tecnologias utilizadas

- **Python:** linguagem de programação principal;
- **Pandas:** leitura, limpeza e manipulação do conjunto de dados;
- **NumPy:** operações estatísticas e ajuste da regressão;
- **Plotly:** construção dos gráficos interativos;
- **Dash:** interface web e atualização dinâmica dos componentes;
- **Gunicorn:** servidor para execução em ambiente de produção;
- **Render:** opção de hospedagem da aplicação na internet;

## 7. Como executar no computador

**Pré-requisito:** ter Python 3.10 ou superior e `pip` instalados.

1. Extraia a pasta do projeto (caso tenha recebido um arquivo ZIP) e abra um terminal dentro dela.

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Inicie a aplicação:

   ```bash
   python app.py
   ```

4. Abra no navegador:

   **http://127.0.0.1:8050/**

Mantenha o CSV na mesma pasta que `app.py`. Para encerrar a execução local, pressione `Ctrl + C` no terminal.

## 8. Como utilizar o painel

1. Acesse a aplicação no navegador pelo endereço local indicado na seção 7.
2. Observe os quatro indicadores no topo.
3. Selecione uma ou várias **marcas** e/ou opções de **gênero** nos filtros.
4. Compare como os indicadores e os sete gráficos mudam para a seleção feita.
5. Passe o cursor sobre os gráficos para consultar informações detalhadas dos pontos, barras e setores.
6. Limpe os filtros para voltar à visão geral dos dados.

## 9. Resultados esperados e conclusão

O dashboard permite compreender rapidamente o comportamento do catálogo: concentração de preços, distribuição das notas, marcas com maior representação e associações entre avaliações e vendas. O mapa de calor destaca variáveis correlacionadas, enquanto o gráfico de regressão ajuda a visualizar a tendência linear entre avaliações e quantidade vendida codificada.

A principal contribuição do projeto é **tornar a análise de dados mais acessível e intuitiva**, reunindo indicadores, filtros e visualizações interativas em uma única interface, sem que o usuário precise manipular o CSV ou trabalhar diretamente com código Python.

---

**Status:** projeto documentado e preparado para execução local.
