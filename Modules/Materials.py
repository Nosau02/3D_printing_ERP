"""
FR, EN below:
Module de gestion de la base de données matière:

Ce module affiche l'entier de la base de donnée matière, permet d'ajouter une nouvelle référence,
de supprimer une référence, et de visualiser la répartition des matériaux.
Les données sont stockées dans le fichier "materials.csv".

%============

EN:
Material database management module:

This module displays the entire material database, allowing you to add a new reference, delete a reference and view the distribution of materials,
delete a reference, and view the distribution of materials.
The data is stored in the "materials.csv" file.
"""
from dash import html, dash_table, dcc, callback, Output, Input, State, ctx
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from os import path


# === Configuration de base ===
# Fichiers
MAT_FILE = "materials.csv"
FOLDER_PATH = path.split(path.dirname(__file__))[0]  # Dossier parent
DATA_PATH = path.join(FOLDER_PATH, "Data")
MAT_PATH = path.join(DATA_PATH, MAT_FILE)

# Lecture ou création du fichier
if path.exists(MAT_PATH):
    material_df = pd.read_csv(MAT_PATH)
else:
    material_df = pd.DataFrame(columns=["Material", "Type", "Color", "Price", "Brand", "Reference", "Supplyer", "Empty spool weight"])
    material_df.to_csv(MAT_PATH, index=False)

if "Delete" not in material_df.columns:
    material_df["Delete"] = "❌"


# === Layout ===

def layout():
    return dbc.Container([
        dcc.Interval(id="refresh", interval=0, n_intervals=0, max_intervals=1),
        html.H2("Material database", className="text-primary text-center mt-3"),

        dbc.Row([
            dbc.Col([
                html.H5("Material database", className="text-secondary text-center mb-3"),
                dbc.Row([
                    dbc.RadioItems(
                        options=[{"label": x, "value": x} for x in ['Material', 'Color', 'Supplyer']],
                        value='Material',
                        inline=True,
                        id='mat-radio-buttons'
                    )
                ], className="mb-3"),
                dash_table.DataTable(
                    id='mat-material-table',
                    columns=[{"name": i, "id": i} for i in material_df.columns],
                    data=material_df.sort_values(by="Material").to_dict('records'),
                    page_size=10,
                    style_table={'overflowX': 'auto', "maxHeight": "400px", "overflowY": "auto"},
                    style_cell={'textAlign': 'center'},
                    style_data_conditional=[
                        {
                            'if': {'column_id': 'Delete'},
                            'color': 'red',
                            'cursor': 'pointer',
                            'fontWeight': 'bold',
                            'textAlign': 'center'
                        }
                    ]
                ),
                html.Div(className="my-3"),
                dbc.Button("Refresh", id="mat-btn-refresh", color="secondary", className="mb-2 w-100"),
                html.Div(className="my-3"),
                dcc.Graph(id='material-visualisation', style={"height": "400px"})   
                 ], width=6),
                
            dbc.Col([
                html.H5("Add new reference", className="text-secondary text-center mb-3"),
                dbc.Form([
                    dbc.Row([dbc.Label("Material"), dbc.Input(id="mat-input-material", type="text")]),
                    dbc.Row([dbc.Label("Type"), dbc.Input(id="mat-input-type", type="text")]),
                    dbc.Row([dbc.Label("Color"), dbc.Input(id="mat-input-color", type="text")]),
                    dbc.Row([dbc.Label("Cost per kg (CHF)"), dbc.Input(id="mat-input-price", type="number", step="any")]),
                    dbc.Row([dbc.Label("Brand"), dbc.Input(id="mat-input-brand", type="text")]),
                    dbc.Row([dbc.Label("Reference"), dbc.Input(id="mat-input-ref", type="text")]),
                    dbc.Row([dbc.Label("Supplier"), dbc.Input(id="mat-input-supl", type="text")]),
                    dbc.Row([dbc.Label("Empty spool weight (g)"), dbc.Input(id="mat-input-empty-weight", type="number", step="any")]),
                    html.Br(),
                    dbc.Button("Add to database", id="mat-submit-button", color="primary", className="mt-2"),
                    html.Div(id="mat-confirmation-message", className="text-success mt-2")
                ])
            ], width=6)
            ])
    ], fluid=True)


# === Fonctions utilitaires ===
# Mise à jour de la base de données matière
def load_data():
    if path.exists(MAT_PATH):
        return pd.read_csv(MAT_PATH)
    return pd.DataFrame(columns=[
        "Material", "Type", "Color", "Price",
        "Brand", "Reference", "Supplyer",
        "Empty spool weight"
    ])


# === Callbacks ===

def register_callbacks(app):

    @app.callback(
        Output('mat-material-table', 'data'),
        Output('material-visualisation', 'figure'),
        Output('mat-confirmation-message', 'children'),
        Input('mat-submit-button', 'n_clicks'),
        Input('mat-btn-refresh', 'n_clicks'),
        Input('mat-material-table', 'active_cell'),
        Input('mat-radio-buttons', 'value'),
        State('mat-input-material', 'value'),
        State('mat-input-type', 'value'),
        State('mat-input-color', 'value'),
        State('mat-input-price', 'value'),
        State('mat-input-brand', 'value'),
        State('mat-input-ref', 'value'),
        State('mat-input-supl', 'value'),
        State('mat-input-empty-weight', 'value'),
        State('mat-material-table', 'data'),
        prevent_initial_call=False
    )
    def handle_all_events(n1, n2, active_cell, col_chosen, material, type, color, price, brand, ref, supplyer, empty_weight, table_data):
        triggered = ctx.triggered_id
        material_df = pd.read_csv(MAT_PATH)
        
        #Par défaut, aucun message
        message = ""

        # Suppression d'une ligne
        if triggered == "mat-material-table" and active_cell and active_cell["column_id"] == "Delete":
            row_index = active_cell["row"]
            material_df = pd.DataFrame(table_data)
            material_df = material_df.drop(index=row_index).reset_index(drop=True)
            material_df = material_df.drop(columns=["Delete"])
            material_df.to_csv(MAT_PATH, index=False)
            message = "🗑️ Row deleted."

        # Ajout d'une nouvelle référence
        elif triggered == "mat-submit-button":
            new_row = pd.DataFrame([{
                'Material': material,
                'Type': type,
                'Color': color,
                'Price': price,
                'Brand': brand,
                'Reference': ref,
                'Supplyer': supplyer,
                'Empty spool weight': empty_weight
            }])
            material_df = pd.concat([material_df, new_row], ignore_index=True)
            material_df.to_csv(MAT_PATH, index=False)
            message = "✅ Reference added."

        # Rafraîchissement manuel
        elif triggered == 'mat-btn-refresh':
            material_df = load_data()  # relit le CSV du disque
            message = "🔄 Data refreshed."

        # Mise à jour de la colonne "Delete" et tri selon radiobutton
        material_df["Delete"] = "❌"
        material_df = material_df.sort_values(by=col_chosen)

        # Graphique de répartition des matériaux
        fig = px.pie(material_df, names=col_chosen, title=f"Distribution by {col_chosen}")
        return material_df.to_dict('records'), fig, message


# === Exécution en standalone ===

if __name__ == '__main__':
    from dash import Dash
    app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
    app.layout = layout()
    register_callbacks(app)
    app.run(debug=True)