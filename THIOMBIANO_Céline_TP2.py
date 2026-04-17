# %% [markdown]
# # THIOMBIANO_Céline_TP2

# %% [markdown]
# ## Importation des bibliothèques

# %%
import pandas as pd
import plotly as plt
import calendar
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

# %% [markdown]
# ## Etape 2 : Chargement et préparation des données
# 
# ### Chargement des données

# %%
data = pd.read_csv("data/supermarket_sales.csv")  

# %%
data.info()

# %% [markdown]
# ### Colonnes utiles

# %%
df = data[["Invoice ID", "Date", "Quantity", "Gender", "City", "Total", "Rating", "Product line", "Customer type"]]

# %%
df.describe()


# %% [markdown]
# ### Conversion en date

# %%
df["Date"] = pd.to_datetime(df["Date"])

# %%
df.dtypes

# %% [markdown]
# ## Etapes 3: Fonctions metiers
# 
# ### Fonctions à completer

# %% [markdown]
# #### 1. Montant total des achats : 
# Somme du montant total des achats (Total)

# %%
def calculer_montant_total_achats(df):
    montant = df["Total"].sum()
    return f"{round(montant / 1000):.0f}k USD"
montant_total_achats = calculer_montant_total_achats(df)
print(f"Le montant total des achats est de : {montant_total_achats}")   

# %% [markdown]
# #### 2. Nombre total d'achats : 
# Nombre total d'achats (Invoice ID)

# %%
def calculer_nombre_total_achats(df):
    nb = df["Invoice ID"].nunique()
    return f"{round(nb / 1000):.0f}k" if nb >= 1000 else str(nb)
nombre_total_achats = calculer_nombre_total_achats(df)


print(f"Le nombre total d'achats est de : {nombre_total_achats}")

# %% [markdown]
# ####  3. Évaluation moyenne : 
# Moyenne des évaluations (Rating)

# %%
def calculer_evaluation_moyenne(df):
    avg = df["Rating"].mean()
    return f"{avg:.2f}"
evaluation_moyenne = calculer_evaluation_moyenne(df)
print(f"L'évaluation moyenne est de : {evaluation_moyenne}")

# %% [markdown]
# ## Etapes 4 : Graphiques

# %% [markdown]
# ### 1. Histogramme donnant la répartition des montants totaux des achat

# %%
# Fonction Histogramme donnant la répartition des montants totaux des achats par sexe et par ville.
def histogramme_repartition_montants(df):
    fig = px.histogram(df, x="Total", color="Gender", facet_col="City", nbins=20, title="Répartition des montants totaux des achats par sexe et par ville")
    fig.show()      
 

histogramme_repartition_montants(df)


# %% [markdown]
# ### 2. Diagramme en barres du nombre total d'achats par sexe et par ville.
# %%
# Fonction diagramme en barres du nombre total d'achats par sexe et par ville.
def barplot_nombre_achats_par_sexe(df):
    fig = px.bar(df.groupby(["City", "Gender"])["Invoice ID"].nunique().reset_index(), x="City", y="Invoice ID", color="Gender", title="Nombre total d'achats par ville et par genre ")
    fig.show()
barplot_nombre_achats_par_sexe(df)

# %% [markdown]
# ### Diagramme en barres du nombre total d'achats par catégorie et par type de client

# %%
def plot_bar_nombre_achats(df):

    dfg = df.groupby(["Product line", "Customer type"])["Invoice ID"].nunique().reset_index()

    #  TRI EN ORDRE CROISSANT 
    dfg = dfg.sort_values("Invoice ID", ascending=True)

    fig = px.bar(
        dfg,
        y="Product line",
        x="Invoice ID",
        color="Customer type",
        barmode="group",
        title="Nombre total d'achats",
        labels={
            'Invoice ID': "Nombre d'achats",
            'Product line': 'Catégorie du produit',
            'Customer type': 'Type de client'
        }
    )

    fig.update_layout(
        autosize=True,                     # utilise toute la largeur disponible
        margin=dict(l=5, r=5, t=50, b=10), # marges MINIMALES pour élargir le graphe
        yaxis=dict(tickfont=dict(size=8)), # labels plus petits → barres plus longues
        bargap=0.10,
        bargroupgap=0.02,

        # 🔥 LÉGENDE RÉDUITE AU MAXIMUM
        legend=dict(
            font=dict(size=8),             
            orientation="v",               # verticale 
            x=1.02,                        # collée à droite
            y=1,
            bgcolor="rgba(0,0,0,0)"        # fond transparent
        ),

        #  THÈME
        paper_bgcolor="#2C3E50",
        plot_bgcolor="#ffffff",
        font=dict(color="#f7f7f7"),
        title_font=dict(size=18, color="#f7f7f7"),
    )

    fig.update_traces(marker=dict(line=dict(width=1, color="#2C3E50")))

    return fig
plot_bar_nombre_achats(df).show()


# %% [markdown]
# ### 3. Diagramme circulaire montrant la répartition de la catégorie de produit (Product line)
#  

# %%
def plot_pie_product_line(df):

    # Palette premium adaptée au fond foncé
    color_map = {
        "Fashion accessories": "#4FC3F7",
        "Food and beverages": "#FFB74D",
        "Electronic accessories": "#81C784",
        "Sports and travel": "#E57373",
        "Home and lifestyle": "#BA68C8",
        "Health and beauty": "#FFD54F"
    }

    fig = px.pie(
        df,
        names="Product line",
        title="Répartition des catégories de produits",
        color="Product line",
        color_discrete_map=color_map
    )

    fig.update_layout(
        paper_bgcolor="#2C3E50",
        plot_bgcolor="#ffffff",
        title_font=dict(size=20, color="#f7f7f7"),
        font=dict(color="#f7f7f7"),
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig
plot_pie_product_line(df).show()

# %% [markdown]
# ### 4. Évolution du montant total des achats

# %%
def graph_evolution_hebdo(df):

    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    # Palette premium pour les villes
    color_map = {
        "Yangon": "#2D92C1",
        "Mandalay": "#E13D37",
        "Naypyitaw": "#1D6C21"
    }

    # Début de semaine (lundi)
    df["WeekStart"] = df["Date"] - pd.to_timedelta(df["Date"].dt.weekday, unit="D")

    # Agrégation hebdomadaire
    dfg = df.groupby(["WeekStart", "City"])["Total"].sum().reset_index()

    fig = px.line(
        dfg,
        x="WeekStart",
        y="Total",
        color="City",
        title="Évolution hebdomadaire du montant total des achats par ville",
        labels={
            "WeekStart": "Semaine",
            "Total": "Montant total des achats",
            "City": "Ville"
        },
        color_discrete_map=color_map
    )

    # Ticks mensuels, données hebdomadaires
    fig.update_xaxes(
        dtick="M1",          # 1 tick par mois
        tickformat="%b %Y"   # ex : Mar 2019
    )

    fig.update_layout(
        paper_bgcolor="#2C3E50",
        plot_bgcolor="#e6e6e6",
        title_font=dict(size=20, color="#f7f7f7"),
        font=dict(color="#f7f7f7"),
        xaxis_title="semaine",
        yaxis_title="Montant total des achats",
        margin=dict(l=20, r=20, t=60, b=20)
    )

    fig.update_traces(line=dict(width=3))

    return fig
graph_evolution_hebdo(df).show()


# %% [markdown]
# Les branches ici reprensentent aussi les villes

# %% [markdown]
# # Création du dashbord

# %% [markdown]
# ## Etape 5 : Création du dashboard avec Dash

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State


# Palette de couleurs
PRIMARY = "#1f77b4"
LIGHT = "#4fa3d1"
BG = "#2C3E50"
TEXT = "#f7f7f7"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server


app.layout = dbc.Container(
    style={
        "backgroundColor": BG,
        "min-height": "100vh",
        "padding": "20px"
    },
    children=[

        dbc.Row([

            # ================== COLONNE 1 ==================
            dbc.Col(
                [

                    html.Button(
                        "?",
                        id="help_icon",
                        style={
                            "background": "none",
                            "border": "none",
                            "color": "white",
                            "font-size": "28px",
                            "cursor": "pointer",
                            "padding": "0",
                            "margin-bottom": "10px",
                            "margin-left": "5px"
                        }
                    ),

                    dbc.Tooltip(
                        "Tableau de bord réalisé par Céline THIOMBIANO, dans le cadre du cours Python Avancé "
                        "enseigné par le Dr Abdoul Razac SANE, Master Économétrie Appliquée - "
                        "IAE Nantes (2025-2026).",
                        target="help_icon",
                        placement="right",
                        style={"font-size": "14px"}
                    ),

                    html.Div(
                        [
                            html.Img(
                                src="assets/logosup.png",
                                style={
                                    "display": "block",
                                    "margin": "auto",
                                    "height": "300px",
                                    "margin-top": "10px"
                                }
                            )
                        ],
                        style={
                            "padding": "20px",
                            "backgroundColor": "#2C3E50",
                            "border-radius": "8px",
                            "box-shadow": "0 2px 6px rgba(0,0,0,0.2)"
                        }
                    ),

                    html.Div(
                        [
                            html.Label("Sélectionner le genre", style={"font-weight": "bold", "color": "white"}),
                            dcc.Dropdown(
                                id="gender_filter",
                                options=[{"label": "Tout", "value": "ALL"}] +
                                        [{"label": g, "value": g} for g in df["Gender"].unique()],
                                value="ALL",
                                clearable=False,
                                style={"margin-top": "5px"}
                            )
                        ],
                        style={
                            "padding": "15px",
                            "margin-top": "15px",
                            "backgroundColor": "#34495E",
                            "border-radius": "8px",
                            "box-shadow": "0 2px 6px rgba(0,0,0,0.2)"
                        }
                    ),

                    html.Div(
                        [
                            html.Label("Sélectionner la ville", style={"font-weight": "bold", "color": "white"}),
                            dcc.Dropdown(
                                id="city_filter",
                                options=[{"label": "Tout", "value": "ALL"}] +
                                        [{"label": c, "value": c} for c in df["City"].unique()],
                                value="ALL",
                                clearable=False,
                                style={"margin-top": "5px"}
                            )
                        ],
                        style={
                            "padding": "15px",
                            "margin-top": "15px",
                            "backgroundColor": "#34495E",
                            "border-radius": "8px",
                            "box-shadow": "0 2px 6px rgba(0,0,0,0.2)"
                        }
                    ),

                ],
                width=3,
                style={
                    "padding": "0",
                    "backgroundColor": "#2C3E50"
                }
            ),

            # ================== COLONNE 2 ==================
            dbc.Col(
                [

                    dbc.Row(
                        [

                            dbc.Col(
                                html.Div(
                                    [
                                        html.H5("Montant total des achats", style={"font-weight": "bold", "color": PRIMARY}),
                                        html.Div(id="kpi_total", style={"font-size": "26px", "margin-top": "10px", "color": "#000"})
                                    ],
                                    style={
                                        "padding": "15px",
                                        "backgroundColor": "#e6e6e6",
                                        "border-radius": "8px",
                                        "box-shadow": "0 2px 6px rgba(0,0,0,0.1)",
                                        "text-align": "center"
                                    }
                                ),
                                width=4,
                                style={"padding": "10px"}
                            ),

                            dbc.Col(
                                html.Div(
                                    [
                                        html.H5("Nombre total d'achats", style={"font-weight": "bold", "color": PRIMARY}),
                                        html.Div(id="kpi_nb", style={"font-size": "26px", "margin-top": "10px", "color": "#000"})
                                    ],
                                    style={
                                        "padding": "15px",
                                        "backgroundColor": "#e6e6e6",
                                        "border-radius": "8px",
                                        "box-shadow": "0 2px 6px rgba(0,0,0,0.1)",
                                        "text-align": "center"
                                    }
                                ),
                                width=4,
                                style={"padding": "10px"}
                            ),

                            dbc.Col(
                                html.Div(
                                    [
                                        html.H5("Evaluation moyenne ", style={"font-weight": "bold", "color": PRIMARY}),
                                        html.Div(id="kpi_avg", style={"font-size": "26px", "margin-top": "10px", "color": "#000"})
                                    ],
                                    style={
                                        "padding": "15px",
                                        "backgroundColor": "#e6e6e6",
                                        "border-radius": "8px",
                                        "box-shadow": "0 2px 6px rgba(0,0,0,0.1)",
                                        "text-align": "center"
                                    }
                                ),
                                width=4,
                                style={"padding": "10px"}
                            ),

                        ],
                        style={"margin": "0"}
                    ),

                    dbc.Row(
                        [

                            dbc.Col(
                                [

                                    html.Div(
                                        [
                                            dcc.Graph(id="evolution_chart", style={"height": "100%"})
                                        ],
                                        style={
                                            "padding": "10px",
                                            "height": "50%",
                                            "backgroundColor": "white",
                                            "border-radius": "8px",
                                            "box-shadow": "0 2px 6px rgba(0,0,0,0.1)"
                                        }
                                    ),

                                    html.Div(
                                        [
                                            dcc.Graph(id="pie_chart", style={"height": "100%"})
                                        ],
                                        style={
                                            "padding": "10px",
                                            "height": "50%",
                                            "margin-top": "15px",
                                            "backgroundColor": "white",
                                            "border-radius": "8px",
                                            "box-shadow": "0 2px 6px rgba(0,0,0,0.1)"
                                        }
                                    ),

                                ],
                                width=7,
                                style={"padding": "10px", "height": "700px"}
                            ),

                            dbc.Col(
                                html.Div(
                                    [
                                        dcc.Graph(id="bar_chart", style={"height": "100%"})
                                    ],
                                    style={
                                        "padding": "10px",
                                        "height": "700px",
                                        "backgroundColor": "white",
                                        "border-radius": "8px",
                                        "box-shadow": "0 2px 6px rgba(0,0,0,0.1)"
                                    }
                                ),
                                width=5,
                                style={"padding": "10px"}
                            ),

                        ],
                        style={"margin": "0"}
                    ),

                ],
                width=9,
                style={
                    "padding": "0",
                    "backgroundColor": "#2C3E50"
                }
            ),

        ], style={"margin": "0"})

    ],
    fluid=True
)


@app.callback(
    [
        Output("kpi_total", "children"),
        Output("kpi_nb", "children"),
        Output("kpi_avg", "children"),
        Output("pie_chart", "figure"),
        Output("evolution_chart", "figure"),
        Output("bar_chart", "figure"),
    ],
    [
        Input("gender_filter", "value"),
        Input("city_filter", "value")
    ]
)
def update_dashboard(gender, city):

    dff = df.copy()

    if gender != "ALL":
        dff = dff[dff["Gender"] == gender]

    if city != "ALL":
        dff = dff[dff["City"] == city]

    return (
        calculer_montant_total_achats(dff),
        calculer_nombre_total_achats(dff),
        calculer_evaluation_moyenne(dff),
        plot_pie_product_line(dff),
        graph_evolution_hebdo(dff),
        plot_bar_nombre_achats(dff)
    )


if __name__ == "__main__":
    app.run(debug=True)




