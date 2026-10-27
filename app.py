"""Painel interativo do projeto de E-commerce (Dash + Plotly)."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

DATA_PATH = Path(__file__).resolve().parent / 'ecommerce_estatistica.csv'
df = pd.read_csv(DATA_PATH)
for campo in ['Preço', 'Nota', 'N_Avaliações', 'Desconto', 'Qtd_Vendidos_Cod']:
    df[campo] = pd.to_numeric(df[campo], errors='coerce')
for campo in ['Marca', 'Gênero']:
    df[campo] = df[campo].fillna('Não informado').astype(str)

NUMERICAS = ['Preço', 'Nota', 'N_Avaliações', 'Desconto', 'Qtd_Vendidos_Cod']
NOMES = {'Preço': 'Preço (R$)', 'Nota': 'Nota', 'N_Avaliações': 'Número de avaliações',
         'Desconto': 'Desconto (%)', 'Qtd_Vendidos_Cod': 'Quantidade vendida (aproximada)'}
CORES = px.colors.qualitative.Safe

app = Dash(__name__, title='E-commerce | Painel de Dados')
server = app.server  # servidor WSGI para deploy com gunicorn

app.layout = html.Div(className='page', children=[
    html.Div(className='header', children=[
        html.P('PROJETO FINAL · ANÁLISE DE DADOS', className='eyebrow'),
        html.H1('Painel de E-commerce'),
        html.P('Explore o catálogo, as avaliações e a relação com as vendas por meio de sete visualizações interativas.'),
    ]),
    html.Div(className='filters', children=[
        html.Div([html.Label('Filtrar por marca'), dcc.Dropdown(
            options=[{'label': m, 'value': m} for m in sorted(df['Marca'].unique())],
            id='filtro-marca', multi=True, placeholder='Todas as marcas')]),
        html.Div([html.Label('Filtrar por gênero'), dcc.Dropdown(
            options=[{'label': g, 'value': g} for g in sorted(df['Gênero'].unique())],
            id='filtro-genero', multi=True, placeholder='Todos os gêneros')]),
    ]),
    html.Div(id='resumo', className='metrics'),
    html.Div(id='aviso', className='hint'),
    html.Div(className='charts', children=[
        html.Div([html.H2('1. Histograma · Distribuição dos preços'), dcc.Graph(id='histograma')], className='chart'),
        html.Div([html.H2('2. Dispersão · Avaliações × vendas'), dcc.Graph(id='dispersao')], className='chart'),
        html.Div([html.H2('3. Mapa de calor · Correlações'), dcc.Graph(id='calor')], className='chart'),
        html.Div([html.H2('4. Barras · Top 10 marcas'), dcc.Graph(id='barras')], className='chart'),
        html.Div([html.H2('5. Pizza · Gênero dos produtos'), dcc.Graph(id='pizza')], className='chart'),
        html.Div([html.H2('6. Densidade · Notas'), dcc.Graph(id='densidade')], className='chart'),
        html.Div([html.H2('7. Regressão · Avaliações × vendas'), dcc.Graph(id='regressao')], className='chart full'),
    ]),
    html.P('Fonte: ecommerce_estatistica.csv · Quantidade vendida é aproximada/codificada; correlação não implica causalidade.', className='footer'),
])


def grafico_vazio(mensagem='Sem dados suficientes para este gráfico.'):
    fig = go.Figure()
    fig.add_annotation(text=mensagem, showarrow=False, x=0.5, y=0.5, xref='paper', yref='paper')
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig


def preparar(fig, x=None, y=None):
    fig.update_layout(template='plotly_white', margin=dict(l=45, r=25, t=28, b=55),
                      font=dict(family='Arial, sans-serif', size=12),
                      paper_bgcolor='white', plot_bgcolor='white',
                      legend_title_text='Categoria')
    fig.update_xaxes(title_text=x)
    fig.update_yaxes(title_text=y)
    return fig


def card(numero, titulo):
    return html.Div([html.Div(numero, className='metric-value'), html.Div(titulo, className='metric-label')], className='metric')


@app.callback(
    Output('resumo', 'children'), Output('aviso', 'children'),
    Output('histograma', 'figure'), Output('dispersao', 'figure'),
    Output('calor', 'figure'), Output('barras', 'figure'),
    Output('pizza', 'figure'), Output('densidade', 'figure'),
    Output('regressao', 'figure'),
    Input('filtro-marca', 'value'), Input('filtro-genero', 'value'),
)
def atualizar(marcas, generos):
    d = df.copy()
    if marcas:
        d = d[d['Marca'].isin(marcas)]
    if generos:
        d = d[d['Gênero'].isin(generos)]

    preco = d['Preço'].mean()
    nota = d['Nota'].mean()
    corr = d[['N_Avaliações', 'Qtd_Vendidos_Cod']].corr().iloc[0, 1] if len(d) > 1 else np.nan
    fmt = lambda v: f'{v:.2f}'.replace('.', ',') if pd.notna(v) else '—'
    resumo = [card(f'{len(d):,}'.replace(',', '.'), 'Produtos filtrados'),
              card(f'R$ {fmt(preco)}', 'Preço médio'),
              card(fmt(nota), 'Nota média'),
              card(fmt(corr), 'Correlação: avaliações × vendas')]
    if d.empty:
        vazio = grafico_vazio('Nenhum produto corresponde aos filtros escolhidos.')
        return resumo, 'Altere os filtros para visualizar registros.', *(vazio for _ in range(7))

    h = px.histogram(d.dropna(subset=['Preço']), x='Preço', nbins=20, color_discrete_sequence=[CORES[0]])
    preparar(h, 'Preço (R$)', 'Quantidade de produtos')

    s = px.scatter(d.dropna(subset=['N_Avaliações', 'Qtd_Vendidos_Cod']),
                   x='N_Avaliações', y='Qtd_Vendidos_Cod', hover_name='Título', opacity=0.7,
                   color_discrete_sequence=[CORES[1]])
    preparar(s, 'Número de avaliações', 'Quantidade vendida (aproximada)')

    matriz = d[NUMERICAS].corr()
    heat = go.Figure(go.Heatmap(z=matriz.values, x=[NOMES[x] for x in NUMERICAS],
                                y=[NOMES[x] for x in NUMERICAS], zmin=-1, zmax=1,
                                colorscale='RdBu', reversescale=True, zmid=0,
                                text=np.round(matriz.values, 2), texttemplate='%{text}',
                                hovertemplate='%{x} × %{y}: %{z:.2f}<extra></extra>'))
    preparar(heat, 'Indicadores', 'Indicadores')
    heat.update_layout(margin=dict(l=140, r=25, t=28, b=100))

    top = d['Marca'].value_counts().head(10).sort_values()
    b = px.bar(x=top.values, y=top.index, orientation='h', color_discrete_sequence=[CORES[2]])
    preparar(b, 'Quantidade de produtos', 'Marca')

    conta = d['Gênero'].value_counts()
    pequeno = conta[conta < 10].sum()
    conta = conta[conta >= 10]
    if pequeno:
        conta.loc['Outros'] = pequeno
    p = px.pie(values=conta.values, names=conta.index, hole=0.18,
               color_discrete_sequence=CORES)
    preparar(p)
    p.update_traces(hovertemplate='%{label}: %{value} produtos (%{percent})<extra></extra>')

    notas = d['Nota'].dropna().to_numpy(dtype=float)
    if len(notas) >= 3 and np.std(notas) > 0:
        # KDE em NumPy, evitando dependência de scipy, para um deploy leve.
        n = len(notas)
        sigma = np.std(notas, ddof=1)
        h_bw = max(1.06 * sigma * n ** (-1/5), 0.035)
        xx = np.linspace(max(0, notas.min() - .35), min(5, notas.max() + .35), 240)
        yy = np.exp(-.5 * ((xx[:, None] - notas[None, :]) / h_bw) ** 2).sum(axis=1)
        yy /= (n * h_bw * np.sqrt(2 * np.pi))
        kde = go.Figure(go.Scatter(x=xx, y=yy, mode='lines', fill='tozeroy',
                                   line=dict(color='#20a486', width=3), name='Densidade'))
    else:
        kde = grafico_vazio('É preciso ter ao menos três notas variadas para a densidade.')
    preparar(kde, 'Nota dos produtos', 'Densidade estimada')

    pontos = d[['N_Avaliações', 'Qtd_Vendidos_Cod']].dropna()
    if len(pontos) >= 2 and pontos['N_Avaliações'].nunique() >= 2:
        reg = px.scatter(pontos, x='N_Avaliações', y='Qtd_Vendidos_Cod',
                         opacity=.55, color_discrete_sequence=[CORES[3]])
        x = pontos['N_Avaliações'].to_numpy(dtype=float)
        y = pontos['Qtd_Vendidos_Cod'].to_numpy(dtype=float)
        a, c = np.polyfit(x, y, 1)
        xfit = np.linspace(x.min(), x.max(), 100)
        reg.add_trace(go.Scatter(x=xfit, y=a*xfit+c, mode='lines', name='Regressão linear',
                                 line=dict(color='#d74c42', width=3)))
    else:
        reg = grafico_vazio('São necessários dois valores distintos de avaliações para a regressão.')
    preparar(reg, 'Número de avaliações', 'Quantidade vendida (aproximada)')
    return resumo, f'Exibindo {len(d)} de {len(df)} produtos. Os gráficos são atualizados conforme os filtros.', h, s, heat, b, p, kde, reg


if __name__ == '__main__':
    app.run(debug=True)
