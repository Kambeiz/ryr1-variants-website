import dash
from dash import html, dcc
from dash.dependencies import Input, Output

layout = html.Div([
    html.Header([
        html.H1("RyR1"),
        html.P("Ryanodine Receptor 1"),
    ]),
    html.Div([
        html.H2("Bienvenue sur le site dédié à l'étude de RyR1"),
        html.P("Ce site a été créé dans le cadre d'une thèse sur la protéine RyR1 (Récepteur de la ryanodine de type 1). Vous trouverez ici des informations détaillées sur la structure, sa fonction et mon travail relatif sur la prédiction de phénotype de ces variants missense, modélisés pour l'occasion."),
        html.P("Explorez les différentes sections pour en apprendre davantage sur :"),
        html.Ul([
            html.Li("La Présentation générale de RyR1"),
            html.Li("Modèles Humains de RyR1"),
            html.Li("Variants de RyR1"),
        ]),
        html.P("N'hésitez pas à me contacter pour plus d'informations ou pour discuter de cette recherche."),
    ]),
])
