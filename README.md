# Dashboard de E-commerce — Dash + Plotly

Aplicação de análise exploratória do arquivo `ecommerce_estatistica.csv`, com filtros por marca e gênero, quatro indicadores e os sete gráficos solicitados: **histograma, dispersão, mapa de calor, barras, pizza, densidade e regressão linear**.

## Executar no computador

Requer Python 3.10 ou mais recente.

```bash
pip install -r requirements.txt
python app.py
```

Abra `http://127.0.0.1:8050` no navegador.

## Enviar ao GitHub

1. Crie um repositório no GitHub.
2. Na opção **Add file > Upload files**, envie os arquivos `app.py`, `ecommerce_estatistica.csv`, `requirements.txt`, `render.yaml`, `.gitignore` e `README.md` (extraia o ZIP antes).
3. Clique em **Commit changes**.
4. Copie o link do repositório para a atividade.

## Disponibilizar um link para o cliente (Render)

O link do GitHub **mostra o código**, mas **não executa** o painel. Para permitir que alguém use o dashboard apenas no navegador:

1. Acesse [render.com](https://render.com/) e entre na sua conta.
2. Escolha **New > Web Service** e conecte o repositório GitHub.
3. Configure ambiente **Python**, instalação `pip install -r requirements.txt` e comando de inicialização `gunicorn app:server --bind 0.0.0.0:$PORT` (ou utilize o blueprint `render.yaml`).
4. Selecione um plano disponível e confirme a publicação. Verifique os custos atuais antes de contratar.
5. Abra a URL pública `https://<nome-do-servico>.onrender.com` informada pelo Render. Não use esse exemplo como link final.

Nota: o Render pode levar algum tempo para ativar serviços suspensos conforme o plano escolhido.

## Observações analíticas

- `Qtd_Vendidos_Cod` representa quantidade vendida codificada/aproximada a partir da base.
- Correlação/regressão são **associações**, não prova de causa e efeito.
- Os filtros afetam tanto os indicadores quanto os sete gráficos.
