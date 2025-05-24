# 🕵️‍♂️ Tunga – Webscraper de Produtos Proibidos (Predecessor do Regulatron)

Este repositório apresenta uma coleção de protótipos de **web scraping** desenvolvidos para identificar produtos cuja **venda não é permitida no Brasil**, com foco inicial em grandes marketplaces.

O projeto teve início em **2023**, com o primeiro protótipo funcional implementado no notebook `tunga_mercado_livre.ipynb`, que realiza a coleta e análise de dados do site da Amazon Brasil.

---

## 🎯 Objetivo

O sistema Tunga tem como objetivo auxiliar a fiscalização e o monitoramento de produtos comercializados em plataformas online, especialmente aqueles que estejam em desacordo com a regulamentação nacional.

---

## 🧩 Módulos disponíveis

- `tunga_amazon` – Coleta e identifica produtos da [Amazon Brasil](https://www.amazon.com.br)
- `tunga_carrefour` – Coleta de produtos do [Carrefour Brasil](https://www.carrefour.com.br)
- `tunga_mercado_livre` – Coleta de produtos do [Mercado Livre](https://www.mercadolivre.com.br)
- `tunga_shopee` – Coleta de produtos da [Shopee Brasil](https://shopee.com.br)

> ⚠️ Os notebooks ainda não foram alterados desde sua última utilização e podem demandar ajustes conforme alterações nos sites-alvo, graças a mudanças ocorridas em suas diagramações ou atualizações das bibliotecas python

---

## 🛠️ Tecnologias utilizadas

- **Python 3.x**
- Bibliotecas principais:
  - `selenium`
  - `requets`
  - `BeautifulSoup`
  - `pandas`
  - `re`
  - `json`
  - `IPython.display` (para visualização interativa)

---

## 🚀 Como usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu_usuario/tunga.git
   cd tunga

2. Abra o notebook desejado com Jupyter:
   ```bash
     jupyter notebook tunga_amazon.ipynb

3. Siga as instruções no notebook para executar o scraper e visualizar os resultados.
