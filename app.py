######-----Import Dash-----#####
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px

#####-----Create a Dash app instance-----#####
app = dash.Dash(
    external_stylesheets=[dbc.themes.LITERA],
    name = 'Ship Particular'
    )
app.title = 'Ship Particular Dashboard'

##-----Navbar
navbar = dbc.NavbarSimple(
    brand="Ship Particular Dashboard",
    brand_href="#",
    color="#500F0F",
    dark=True,
)

##-----Import Data Ditkapel
df = pd.read_excel('df_kapal_cleaned.xlsx')
df[['Jenis Kapal', 'Nama Pemilik']] = df[['Jenis Kapal', 'Nama Pemilik']].astype('category')
df['Umur Kapal'] = 2023-df['Tahun Pembuatan']
list_nama_pemilik = list(df['Nama Pemilik'].sort_values().unique())
list_nama_pemilik.insert(0, 'ALL')
list_jenis_kapal = list(df['Jenis Kapal'].sort_values().unique())
list_jenis_kapal.insert(0, 'ALL')

##----- Jenis Kapal
df_jenis_kapal_all = df.groupby('Jenis Kapal')['Jenis Kapal'].count().reset_index(name='Jumlah Kapal').sort_values(by='Jumlah Kapal').tail(10)
    
# Visualize
plot_rank_jenis_kapal_all = px.bar(df_jenis_kapal_all, 
                                    x='Jumlah Kapal', 
                                    y='Jenis Kapal', 
                                    orientation='h',
                                    color_discrete_sequence=['#9A2041'], 
                                    template = 'ggplot2',
                                    title='TOP 10 Jumlah Kapal Berdasarkan Jenis Kapal')
plot_rank_jenis_kapal_all.update_xaxes(tickangle= 45)

##----- Nama Pemilik
df_nama_pemilik_all = df.groupby('Nama Pemilik')['Nama Pemilik'].count().reset_index(name='Jumlah Kapal').sort_values(by='Jumlah Kapal').tail(10)
df_nama_pemilik_all['Nama Pemilik'] = df_nama_pemilik_all['Nama Pemilik'].replace(['PT BATULICIN NUSANTARA MARITIM',
                                                                            'PT BINTANG SAMUDERA MANDIRI LINES',
                                                                            'PT HABCO TRANS MARITIMA',
                                                                            'PT KARTIKA SAMUDERA ADIJAYA', 
                                                                            'PT MITRABAHTERA SEGARA SEJATI', 
                                                                            'PT PELAYARAN NASIONAL EKALYA PURNAMASARI',
                                                                            'PT PELAYARAN NELLY DWI PUTRI', 
                                                                            'PT PELITA SAMUDERA SHIPPING',
                                                                            'PT PULAU SEROJA JAYA', 
                                                                            'PT TRANS POWER MARINE', 
                                                                            'PT TRANSCOAL PACIFIC',], 
                                                                            ['IDX:BESS', 
                                                                            'IDX:BSML', 
                                                                            'IDX:HATM', 
                                                                            'KSA', 
                                                                            'IDX:MBSS', 
                                                                            'IDX:ELPI', 
                                                                            'IDX:NELY', 
                                                                            'IDX:PSSI', 
                                                                            'PSS', 
                                                                            'IDX:TPMA', 
                                                                            'IDX:TCPI'])

# Visualize
plot_rank_nama_pemilik_all = px.bar(df_nama_pemilik_all, 
                                    x='Jumlah Kapal',
                                    y='Nama Pemilik',
                                    orientation='h',
                                    color_discrete_sequence=['#9A2041'], 
                                    template = 'ggplot2',
                                    title='TOP 10 Jumlah Kapal Berdasarkan Nama Pemilik')
plot_rank_nama_pemilik_all.update_xaxes(tickangle= 45)


## -----LAYOUT-----
app.layout = html.Div(children=[
    navbar,
    
    html.Br(),

    ## --Component Main Page--
    html.Div([
        ## --ROW1--
        dbc.Row([
            ### --COLUMN1--
            dbc.Col([
                dcc.Graph(figure=plot_rank_jenis_kapal_all)
            ], width=6),
            ### --COLUMN2--
            dbc.Col([
                dcc.Graph(figure=plot_rank_nama_pemilik_all)
            ], width=6)
        ]),

    html.P('Filter By Nama Pemilik & Jenis Kapal',
            style={'textAlign': 'center', 
                   'fontSize': 20, 
                   'background-color':'#500F0F',
                   'color':'white',
                   'font-family':'Arial'}
            ),

        ## --ROW2--
        dbc.Row([
            ### --COLUMN1--
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Select Nama Pemilik'),
                    dbc.CardBody(
                        dcc.Dropdown(
                            id = 'select_nama_pemilik',
                            options = list_nama_pemilik,
                            value = 'ALL',
                            style={'font-size' : '90%'}
                        )
                    )
                ]),

                html.Br(),

                dbc.Tabs([
                    ## --Jenis Kapal--
                    dbc.Tab(
                        dcc.Graph(
                            id='rank_jenis_kapal',
                        ),
                        label='Jenis Kapal',
                        label_style={"color": "#9A2041"},
                    ),

                    ## --Nama Pemilik--
                    dbc.Tab(
                        dcc.Graph(
                            id='rank_nama_pemilik',
                        ),
                        label='Nama Pemilik',
                        label_style={"color": "#9A2041"},
                    ),                    
                ]),        
            ],width=6),

            ### --COLUMN2--
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Select Jenis Kapal'),
                    dbc.CardBody(
                        dcc.Dropdown(
                            id = 'select_jenis_kapal',
                            options = list_jenis_kapal,
                            value = 'ALL',
                            style={'font-size' : '90%'}
                        )
                    )
                ]),

                html.Br(),

                dbc.Tabs([
                    ## --Panjang--
                    dbc.Tab(
                        dcc.Graph(
                            id='hist_panjang',
                        ),
                        label='Panjang',
                        label_style={"color": "#9A2041"},
                    ),

                    ## --Lebar--
                    dbc.Tab(
                        dcc.Graph(
                            id='hist_lebar',
                        ),
                        label='Lebar',
                        label_style={"color": "#9A2041"},
                    ),

                    ## --Dalam--
                    dbc.Tab(
                        dcc.Graph(
                            id='hist_dalam',
                        ),
                        label='Dalam',
                        label_style={"color": "#9A2041"},
                    ),

                    ## --LOA--
                    dbc.Tab(
                        dcc.Graph(
                            id='hist_loa',
                        ),
                        label='LOA',
                        label_style={"color": "#9A2041"},
                    ),

                    ## --GT--
                    dbc.Tab(
                        dcc.Graph(
                            id='hist_gt',
                        ),
                        label='GT',
                        label_style={"color": "#9A2041"},
                    ),

                    ## --Isi Bersih--
                    dbc.Tab(
                        dcc.Graph(
                            id='hist_isi_bersih',
                        ),
                        label='Isi Bersih',
                        label_style={"color": "#9A2041"},
                    ),

                    ## --Umur Kapal--
                    dbc.Tab(
                        dcc.Graph(
                            id='hist_umur_kapal',
                        ),
                        label='Umur Kapal',
                        label_style={"color": "#9A2041"},
                    ),
                ]),
            ],width=6,
            ),
        ]) 
    ], style={
        'paddingLeft':'30px',
        'paddingRight':'30px',
    }),

    html.Br(),
    html.Footer('ABL',
            style={'textAlign': 'center', 
                   'fontSize': 20, 
                   'background-color':'#500F0F',
                   'color':'white'})
])

##-- Callback Plot Rank Jenis Kapal
@app.callback(
    Output(component_id='rank_jenis_kapal', component_property='figure'),
    Input(component_id='select_jenis_kapal', component_property='value'),
    Input(component_id='select_nama_pemilik', component_property='value')
)

def update_rank_jenis_kapal(jenis_kapal, nama_pemilik):
    # Data aggregation
    if nama_pemilik == 'ALL' and jenis_kapal == 'ALL':
        df_filter = df 
    elif jenis_kapal == 'ALL':
        df_filter = df[df['Nama Pemilik'] == nama_pemilik]
    elif nama_pemilik == 'ALL':
        df_filter = df[df['Jenis Kapal'] == jenis_kapal]
    else :
        df_filter = df[(df['Jenis Kapal'] == jenis_kapal) & (df['Nama Pemilik'] == nama_pemilik)]

    
    df_jenis_kapal = df_filter.groupby('Jenis Kapal')['Jenis Kapal'].count().reset_index(name='Jumlah Kapal').sort_values(by='Jumlah Kapal' ,ascending=False)
    
    # Visualize
    plot_rank_jenis_kapal = px.bar(df_jenis_kapal, 
                                x='Jenis Kapal', 
                                y='Jumlah Kapal', 
                                color_discrete_sequence=['#D94660'], 
                                template = 'ggplot2',
                                title=f'Jumlah Kapal Berdasarkan Jenis Kapal {jenis_kapal} <br> di {nama_pemilik}')
    plot_rank_jenis_kapal.update_xaxes(tickangle= 45)

    # plot_rank_jenis_kapal.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    return plot_rank_jenis_kapal


##-- Callback Plot Rank Nama Pemilik
@app.callback(
    Output(component_id='rank_nama_pemilik', component_property='figure'),
    Input(component_id='select_jenis_kapal', component_property='value'),
    Input(component_id='select_nama_pemilik', component_property='value')
)

def update_rank_nama_pemilik(jenis_kapal, nama_pemilik):
    # Data aggregation
    if nama_pemilik == 'ALL' and jenis_kapal == 'ALL':
        df_filter = df 
    elif jenis_kapal == 'ALL':
        df_filter = df[df['Nama Pemilik'] == nama_pemilik]
    elif nama_pemilik == 'ALL':
        df_filter = df[df['Jenis Kapal'] == jenis_kapal]
    else :
        df_filter = df[(df['Jenis Kapal'] == jenis_kapal) & (df['Nama Pemilik'] == nama_pemilik)]

    df_nama_pemilik = df_filter.groupby('Nama Pemilik')['Nama Pemilik'].count().reset_index(name='Jumlah Kapal').sort_values(by='Jumlah Kapal' ,ascending=False)
    df_nama_pemilik['Nama Pemilik'] = df_nama_pemilik['Nama Pemilik'].replace(['PT BATULICIN NUSANTARA MARITIM',
                                                                            'PT BINTANG SAMUDERA MANDIRI LINES',
                                                                            'PT HABCO TRANS MARITIMA',
                                                                            'PT KARTIKA SAMUDERA ADIJAYA', 
                                                                            'PT MITRABAHTERA SEGARA SEJATI', 
                                                                            'PT PELAYARAN NASIONAL EKALYA PURNAMASARI',
                                                                            'PT PELAYARAN NELLY DWI PUTRI', 
                                                                            'PT PELITA SAMUDERA SHIPPING',
                                                                            'PT PULAU SEROJA JAYA', 
                                                                            'PT TRANS POWER MARINE', 
                                                                            'PT TRANSCOAL PACIFIC',], 
                                                                            ['IDX:BESS', 
                                                                            'IDX:BSML', 
                                                                            'IDX:HATM', 
                                                                            'KSA', 
                                                                            'IDX:MBSS', 
                                                                            'IDX:ELPI', 
                                                                            'IDX:NELY', 
                                                                            'IDX:PSSI', 
                                                                            'PSS', 
                                                                            'IDX:TPMA', 
                                                                            'IDX:TCPI'])

    # Visualize
    plot_rank_nama_pemilik = px.bar(df_nama_pemilik, 
                                x='Nama Pemilik', 
                                y='Jumlah Kapal', 
                                color_discrete_sequence=['#D94660'], 
                                template = 'ggplot2',
                                title=f'Jumlah Kapal {jenis_kapal} <br> di {nama_pemilik}')
    plot_rank_nama_pemilik.update_xaxes(tickangle= 45)
    # plot_rank_jenis_kapal.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    return plot_rank_nama_pemilik


##-- Callback Plot Histogram Panjang
@app.callback(
    Output(component_id='hist_panjang', component_property='figure'),
    Input(component_id='select_jenis_kapal', component_property='value'),
    Input(component_id='select_nama_pemilik', component_property='value')
)

def update_histogram_panjang(jenis_kapal, nama_pemilik):
    # Data aggregation
    if nama_pemilik == 'ALL' and jenis_kapal == 'ALL':
        df_filter = df 
    elif jenis_kapal == 'ALL':
        df_filter = df[df['Nama Pemilik'] == nama_pemilik]
    elif nama_pemilik == 'ALL':
        df_filter = df[df['Jenis Kapal'] == jenis_kapal]
    else :
        df_filter = df[(df['Jenis Kapal'] == jenis_kapal) & (df['Nama Pemilik'] == nama_pemilik)]

    # Visualize
    plot_hist_panjang=px.histogram(df_filter,
                                    x="Panjang",
                                    # nbins=30,
                                    title=f'Sebaran Panjang Kapal {jenis_kapal} <br> di {nama_pemilik}',
                                    color_discrete_sequence=['#D94660'], 
                                    template='ggplot2',
                                    )
    plot_hist_panjang.for_each_trace(lambda t: t.update(hovertemplate=t.hovertemplate.replace("count", "Jumlah Kapal")))
    plot_hist_panjang.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("count", "Jumlah Kapal")))
    return plot_hist_panjang

##-- Callback Plot Histogram Lebar
@app.callback(
    Output(component_id='hist_lebar', component_property='figure'),
    Input(component_id='select_jenis_kapal', component_property='value'),
    Input(component_id='select_nama_pemilik', component_property='value')
)

def update_histogram_lebar(jenis_kapal, nama_pemilik):
    # Data aggregation
    if nama_pemilik == 'ALL' and jenis_kapal == 'ALL':
        df_filter = df 
    elif jenis_kapal == 'ALL':
        df_filter = df[df['Nama Pemilik'] == nama_pemilik]
    elif nama_pemilik == 'ALL':
        df_filter = df[df['Jenis Kapal'] == jenis_kapal]
    else :
        df_filter = df[(df['Jenis Kapal'] == jenis_kapal) & (df['Nama Pemilik'] == nama_pemilik)]

    # Visualize
    plot_hist_lebar=px.histogram(df_filter,
                                    x="Lebar",
                                    # nbins=30,
                                    title=f'Sebaran Lebar Kapal {jenis_kapal} <br> di {nama_pemilik}',
                                    color_discrete_sequence=['#D94660'], 
                                    template='ggplot2',
                                    )
    plot_hist_lebar.for_each_trace(lambda t: t.update(hovertemplate=t.hovertemplate.replace("count", "Jumlah Kapal")))
    plot_hist_lebar.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("count", "Jumlah Kapal")))
    return plot_hist_lebar

##-- Callback Plot Histogram Dalam
@app.callback(
    Output(component_id='hist_dalam', component_property='figure'),
    Input(component_id='select_jenis_kapal', component_property='value'),
    Input(component_id='select_nama_pemilik', component_property='value')
)

def update_histogram_dalam(jenis_kapal, nama_pemilik):
    # Data aggregation
    if nama_pemilik == 'ALL' and jenis_kapal == 'ALL':
        df_filter = df 
    elif jenis_kapal == 'ALL':
        df_filter = df[df['Nama Pemilik'] == nama_pemilik]
    elif nama_pemilik == 'ALL':
        df_filter = df[df['Jenis Kapal'] == jenis_kapal]
    else :
        df_filter = df[(df['Jenis Kapal'] == jenis_kapal) & (df['Nama Pemilik'] == nama_pemilik)]

    # Visualize
    plot_hist_dalam=px.histogram(df_filter,
                                    x="Dalam",
                                    # nbins=30,
                                    title=f'Sebaran Dalam Kapal {jenis_kapal} <br> di {nama_pemilik}',
                                    color_discrete_sequence=['#D94660'], 
                                    template='ggplot2',
                                    )
    plot_hist_dalam.for_each_trace(lambda t: t.update(hovertemplate=t.hovertemplate.replace("count", "Jumlah Kapal")))
    plot_hist_dalam.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("count", "Jumlah Kapal")))
    return plot_hist_dalam

##-- Callback Plot Histogram LOA
@app.callback(
    Output(component_id='hist_loa', component_property='figure'),
    Input(component_id='select_jenis_kapal', component_property='value'),
    Input(component_id='select_nama_pemilik', component_property='value')
)

def update_histogram_loa(jenis_kapal, nama_pemilik):
    # Data aggregation
    if nama_pemilik == 'ALL' and jenis_kapal == 'ALL':
        df_filter = df 
    elif jenis_kapal == 'ALL':
        df_filter = df[df['Nama Pemilik'] == nama_pemilik]
    elif nama_pemilik == 'ALL':
        df_filter = df[df['Jenis Kapal'] == jenis_kapal]
    else :
        df_filter = df[(df['Jenis Kapal'] == jenis_kapal) & (df['Nama Pemilik'] == nama_pemilik)]

    # Visualize
    plot_hist_loa=px.histogram(df_filter,
                                    x="LOA",
                                    # nbins=30,
                                    title=f'Sebaran LOA Kapal {jenis_kapal} <br> di {nama_pemilik}',
                                    color_discrete_sequence=['#D94660'], 
                                    template='ggplot2',
                                    )
    plot_hist_loa.for_each_trace(lambda t: t.update(hovertemplate=t.hovertemplate.replace("count", "Jumlah Kapal")))
    plot_hist_loa.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("count", "Jumlah Kapal")))
    return plot_hist_loa

##-- Callback Plot Histogram GT
@app.callback(
    Output(component_id='hist_gt', component_property='figure'),
    Input(component_id='select_jenis_kapal', component_property='value'),
    Input(component_id='select_nama_pemilik', component_property='value')
)

def update_histogram_gt(jenis_kapal, nama_pemilik):
    # Data aggregation
    if nama_pemilik == 'ALL' and jenis_kapal == 'ALL':
        df_filter = df 
    elif jenis_kapal == 'ALL':
        df_filter = df[df['Nama Pemilik'] == nama_pemilik]
    elif nama_pemilik == 'ALL':
        df_filter = df[df['Jenis Kapal'] == jenis_kapal]
    else :
        df_filter = df[(df['Jenis Kapal'] == jenis_kapal) & (df['Nama Pemilik'] == nama_pemilik)]

    # Visualize
    plot_hist_gt=px.histogram(df_filter,
                            x="GT",
                            # nbins=30,
                            title=f'Sebaran GT Kapal {jenis_kapal} <br> di {nama_pemilik}',
                            color_discrete_sequence=['#D94660'], 
                            template='ggplot2',
                            )
    plot_hist_gt.for_each_trace(lambda t: t.update(hovertemplate=t.hovertemplate.replace("count", "Jumlah Kapal")))
    plot_hist_gt.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("count", "Jumlah Kapal")))
    return plot_hist_gt

##-- Callback Plot Histogram Isi Bersih
@app.callback(
    Output(component_id='hist_isi_bersih', component_property='figure'),
    Input(component_id='select_jenis_kapal', component_property='value'),
    Input(component_id='select_nama_pemilik', component_property='value')
)

def update_histogram_isi_bersih(jenis_kapal, nama_pemilik):
    # Data aggregation
    if nama_pemilik == 'ALL' and jenis_kapal == 'ALL':
        df_filter = df 
    elif jenis_kapal == 'ALL':
        df_filter = df[df['Nama Pemilik'] == nama_pemilik]
    elif nama_pemilik == 'ALL':
        df_filter = df[df['Jenis Kapal'] == jenis_kapal]
    else :
        df_filter = df[(df['Jenis Kapal'] == jenis_kapal) & (df['Nama Pemilik'] == nama_pemilik)]

    # Visualize
    plot_hist_isi_bersih=px.histogram(df_filter,
                                    x="Isi Bersih",
                                    # nbins=30,
                                    title=f'Sebaran Isi Bersih Kapal {jenis_kapal} <br> di {nama_pemilik}',
                                    color_discrete_sequence=['#D94660'], 
                                    template='ggplot2',
                                    )
    plot_hist_isi_bersih.for_each_trace(lambda t: t.update(hovertemplate=t.hovertemplate.replace("count", "Jumlah Kapal")))
    plot_hist_isi_bersih.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("count", "Jumlah Kapal")))
    return plot_hist_isi_bersih

##-- Callback Plot Histogram Umur Kapal
@app.callback(
    Output(component_id='hist_umur_kapal', component_property='figure'),
    Input(component_id='select_jenis_kapal', component_property='value'),
    Input(component_id='select_nama_pemilik', component_property='value')
)

def update_histogram_umur_kapal(jenis_kapal, nama_pemilik):
    # Data aggregation
    if nama_pemilik == 'ALL' and jenis_kapal == 'ALL':
        df_filter = df 
    elif jenis_kapal == 'ALL':
        df_filter = df[df['Nama Pemilik'] == nama_pemilik]
    elif nama_pemilik == 'ALL':
        df_filter = df[df['Jenis Kapal'] == jenis_kapal]
    else :
        df_filter = df[(df['Jenis Kapal'] == jenis_kapal) & (df['Nama Pemilik'] == nama_pemilik)]

    # Visualize
    plot_hist_umur_kapal=px.histogram(df_filter,
                                    x="Umur Kapal",
                                    # nbins=30,
                                    title=f'Sebaran Umur Kapal {jenis_kapal} <br> di {nama_pemilik}',
                                    color_discrete_sequence=['#D94660'], 
                                    template='ggplot2',
                                    )
    plot_hist_umur_kapal.for_each_trace(lambda t: t.update(hovertemplate=t.hovertemplate.replace("count", "Jumlah Kapal")))
    plot_hist_umur_kapal.for_each_yaxis(lambda a: a.update(title_text=a.title.text.replace("count", "Jumlah Kapal")))
    return plot_hist_umur_kapal


######-----Start the Dash server-----#####
if __name__ == "__main__":
    app.run_server()