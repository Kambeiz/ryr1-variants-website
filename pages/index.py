import dash
from dash import html, dcc
from dash.dependencies import Input, Output

layout = html.Div([
    html.Header([
        html.H1("RyR1"),
        html.P("Ryanodine Receptor 1"),
    ]),
    html.Div([
        html.H2("Welcome the website dedicated to RyR1 Missense Variants!"),
        html.P("This website have been created for the purpose to show the work and results of my PhD thesis on the protein RyR1."),
        html.P("Feel free to browse to learn about"),
        html.Ul([
            html.Li("The Protein RyR1"),
            html.Li("Human Models of RyR1"),
            html.Li("RyR1 Variants"),
        ]),
        html.P("Feel free to contact me (see About me) for more informations or questions."),
    ]),
])
