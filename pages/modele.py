from dash import html, dcc
from dash.dependencies import Input, Output
import dash_molstar
from dash_molstar.utils import molstar_helper

layout = html.Div([
    html.H2("Modèle de RyR1 chez l'Homme"),
    html.P("In the context of my PhD, I produced two models of RyR1 in the Human, based on two structure templates from the rabbit 7M6A and 7M6L."),
    html.H3("Primed form or Open form:"),
    html.P("You can view the two Human models and the Structural domains of RyR1 with the help of dash Molstar based on molstar.js (the structure might take a couple of seconds to load) below:"),
    dcc.Dropdown(
        id='model-selector',
        options=[
            {'label': 'Primed State', 'value': 'modeles_ryr1_human/Human_7M6A_fullv2_minimise.pdb'},
            {'label': 'Open State', 'value': 'modeles_ryr1_human/Human_7M6L_fullv2_minimise.pdb'}
        ],
        value='modeles_ryr1_human/Human_7M6A_fullv2_minimise.pdb',
        style={'width': '60%'}
    ),
    dash_molstar.MolstarViewer(
        id='model-viewer',
        style={'width': '80%', 'height': '75vh'},
        layout={
            'showSequence': True,
            'layoutShowControls': True,
            'layoutShowSequence': True,
        }
    )
])

def register_callbacks(app):
    @app.callback(
        Output('model-viewer', 'data'),
        [Input('model-selector', 'value')]
    )
    def update_model(selected_model):
        chains = ['A', 'B', 'C', 'D']
        domains = {
            "NTD": list(range(1, 628)),
            "SPRY1": list(range(628, 850)),
            "RY1-2": list(range(850, 1055)),
            "SPRY2-3": list(range(1055, 1657)),
            "JSOL": list(range(1657, 2145)),
            "RY3-4": list(range(2735, 2939)),
            "BSOL": list(range(2145, 3614)),
            "CSOL": list(range(3614, 4175)),
            "EF": list(range(4060, 4135)),
            "TaF": list(range(4175, 4254)),
            "pVSD": list(range(4541, 4820)),
            "Pore": list(range(4820, 4957)),
            "S6c": list(range(4938, 4957)),
            "CTD": list(range(4957, 5039))
        }
        
        components = []
        for domain in domains.keys():
            component = molstar_helper.create_component(
                label=f"Domain {domain}",
                targets=molstar_helper.get_targets(chain=None, residue=domains[domain]),
                representation='cartoon',
            )
            components.append(component)
        
        data = molstar_helper.parse_molecule(selected_model, component=components)
        return data
