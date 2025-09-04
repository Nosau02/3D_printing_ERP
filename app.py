"""
FR, EN below:
Page d'acceuil et gestion des routes entre les modules:
Ce fichier utilise le framework Dash pour créer une application web avec une barre de navigation latérale.
Il importe les modules Calculator, Matière et Tracking, chacun représentant une section différente de l'application.
Il gère également la page d'acceuil de l'application.

%============

EN:
Home page and management of routes between modules:
This file uses the Dash framework to create a web application with a side navigation bar.
It imports the Calculator, Material and Tracking modules, each representing a different section of the application.
It also manages the application's home page.
"""
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input


# Importer les 3 modules
from Modules import Calculator, Materials, Tracking

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Sidebar (menu vertical)
sidebar = dbc.Nav(
    [
        dbc.NavLink("🏠 Home", href="/", active="exact"),
        dbc.NavLink("📊 Calculation", href="/calculator", active="exact"),
        dbc.NavLink("📁 Material database", href="/matiere", active="exact"),
        dbc.NavLink("📋 Quote Management", href="/tracking", active="exact"),
    ],
    vertical=True,
    pills=True,
    className="bg-light",
)

# Layout principal avec sidebar + contenu
app.layout = dbc.Container(
    [
        dcc.Location(id="url"),
        dbc.Row(
            [
                dbc.Col(sidebar, width=2),
                dbc.Col(html.Div(id="page-content"), width=10)
            ]
        )
    ],
    fluid=True,
)

# Callback pour afficher la page selon l'URL
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)

# Appel des fonctions de layout de chaque module 
def display_page(pathname): 
    if pathname == "/calculator": 
        return Calculator.layout() 
    elif pathname == "/matiere": 
        return Materials.layout() 
    elif pathname == "/tracking": 
        return Tracking.layout() 
    else: 
        return html.Div([ html.H2("Welcome into your 3D Printing Management System, beginning point of your 3D printing buisness !"), 
                         html.P("Choose a section from the sidebar to get started.") ]) 
    
# Enregistrer les callbacks de chaque fichier 
Calculator.register_callbacks(app) 
Materials.register_callbacks(app) 
Tracking.register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=True)
