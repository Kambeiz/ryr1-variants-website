from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash_molstar
from dash_molstar.utils import molstar_helper
import os
import dash
from dash.exceptions import PreventUpdate

# Define the directory and get the list of PDB files
variants_dir = 'variants'
pdb_files = [f for f in os.listdir(variants_dir) if f.endswith('.pdb')]

# Define the layout of the app
layout = html.Div([
    html.H2('Human RyR1 variants created from our two models'),
    html.P('Start typing to search for a Variant file file:'),
    dcc.Dropdown(
        id='search-dropdown',
        options=[{'label': f.split(".")[-2], 'value': f} for f in pdb_files[:5]],  # Default to first 5 files
        placeholder='Type to search...',
        style={'width': '85%'}
    ),
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
        Output('search-dropdown', 'options'),
        [Input('search-dropdown', 'search_value')]
    )
    def update_dropdown_options(search_value):
        if search_value:
            # Filter pdb_files based on search_value
            matching_files = [f for f in pdb_files if search_value.lower() in f.lower()]
            if not matching_files:
                return []
            return [{'label': f.split(".")[-2], 'value': f} for f in matching_files[:19]]  # Limit to 19 results
        else:
            # Show default subset of files if no search term
            return [{'label': f.split(".")[-2], 'value': f} for f in pdb_files[:5]]

    @app.callback(
        Output('variant-viewer', 'data'),
        Input('search-dropdown', 'value')
    )
    def load_variant(selected_variant):
        if not selected_variant:
            raise PreventUpdate

        variant_path = os.path.join(variants_dir, selected_variant)
        
        # Ensure the selected variant exists in the full list of files
        if selected_variant not in pdb_files or not os.path.exists(variant_path):
            raise PreventUpdate
        
        # Parse the molecule and add the custom stick representation
        return molstar_helper.parse_molecule(
            variant_path,
            component=create_molstar_component()  # Use the custom component
        )

    def create_molstar_component():
        """Create a Molstar component with a stick representation."""
        return molstar_helper.create_component(
            label="Variant Representation",
            targets=molstar_helper.get_targets(chain=None, residue=[]),  # Adjust targets accordingly
            representation='ball-and-stick'  # Change representation type here to 'Ball & Stick'
        )


    def fetch_and_parse_pdb(url):
        """Fetch and parse PDB file from an external website."""
        response = requests.get(url)
        if response.status_code == 200:
            pdb_content = response.text
            # Save the file temporarily if needed or directly parse from content
            return molstar_helper.parse_molecule_from_string(pdb_content, format='pdb')
        else:
            print("Failed to fetch the file.")
            return None



# Example usage of fetching from a URL
# fetched_data = fetch_and_parse_pdb("https://example.com/path/to/pdb/file.pdb")