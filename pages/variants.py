from dash import html, dcc, callback, Input, Output, State, ALL
import dash_bootstrap_components as dbc
import dash_molstar
from dash_molstar.utils import molstar_helper
import os
import dash
from dash.exceptions import PreventUpdate

layout = html.Div([
    html.H2('Human RyR1 variants created from our two models'),
    html.P('Enter the name or number of the PDB file you want to view:'),
    dbc.Input(id='search-input', type='text', placeholder='Enter search term...', debounce=False),
    html.Div(id='search-results'),
    dash_molstar.MolstarViewer(
        id='variant-viewer',
        style={'width': '85vh', 'height': '60vh'},
        layout={
            'showSequence': True,
            'layoutShowControls': True,
            'layoutShowSequence': True,
        }
    )
])

def register_callbacks(app):
    @app.callback(
        Output('search-results', 'children'),
        Input('search-input', 'value')
    )
    def search_variants(search_term):
        if not search_term:
            raise PreventUpdate

        variants_dir = 'variants'
        matching_files = [f for f in os.listdir(variants_dir) if search_term.lower() in f.lower() and f.endswith('.pdb')]

        if not matching_files:
            return html.P('No matching files found.')

        return [html.Div(
            dbc.Button(f, id={'type': 'variant-button', 'index': i}, n_clicks=0, color="link")
        ) for i, f in enumerate(matching_files)]

    @app.callback(
        Output('variant-viewer', 'data'),
        Input('search-input', 'value'),
        Input({'type': 'variant-button', 'index': ALL}, 'n_clicks'),
        State({'type': 'variant-button', 'index': ALL}, 'children')
    )
    def load_variant(search_term, n_clicks, button_labels):
        ctx = dash.callback_context
        variants_dir = 'variants'

        if not ctx.triggered:
            raise PreventUpdate

        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigger_id == 'search-input':
            if search_term:
                matching_files = [f for f in os.listdir(variants_dir) if search_term.lower() in f.lower() and f.endswith('.pdb')]
                if matching_files:
                    variant_file = matching_files[0]
                else:
                    raise PreventUpdate
            else:
                raise PreventUpdate
        else:
            button_index = eval(trigger_id)['index']
            variant_file = button_labels[button_index]

        variant_path = os.path.join(variants_dir, variant_file)
        return molstar_helper.parse_molecule(variant_path)