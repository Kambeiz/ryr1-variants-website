import dash
import dash_bootstrap_components as dbc
import dash_molstar
import os
import pandas as pd

from dash_molstar.utils import molstar_helper
from dash import Dash, dcc, html, dash_table, callback, Input, Output, State
from dash.exceptions import PreventUpdate

# Define the directory and get the list of PDB files
variants_dir = 'variants'
pdb_files = [f for f in os.listdir(variants_dir) if f.endswith('.pdb')]


# taking the variant file
var = pd.read_csv("February24_all_exisiting_variants_features_labeled_both_forms_for_website.csv", index_col=0)

# Initial columns to display in the table
initial_columns = ['Position', 'Mutation', 'Origin']

# Define grouped and ungrouped features based on the column names
feature_groups = {
    'Distances': ['Distance ATP (Primed)', 'Distance ATP (Open)', 'Distance Channel Axis (Primed)', 'Distance Axis Channel (Open)', 
    'Distance Caffein (Primed)', 'Distance Caffein (Open)', 'Distance Zn (Primed)', 'Distance Zn (Open)', 'Distance Ca2+ (Primed)', 'Distance Ca2+ (Open)'],
    'Stability': ['Stability (Primed)', 'Stability (Open)', 'Stability Variation (Primed)', 'Stability Variation (Open)'],
    'SASA': ['Environment SASA Variation (Primed)', 'Environment SASA Variation (Open)', 'SASA residue muted (Primed)', 'SASA residue muted (Open)',
    'Variation SASA residue (Primed)', 'Variation SASA residue (Open)', 'SASA reference residue (Primed)', 'SASA reference residue (Open)'],
    'RMSD': ['RSMD Variant vs Reference (Primed)', 'RMSD Variant vs Reference (Open)',
    'RMSD Primed vs Open', 'RMSD Variant Primed vs Open',
    'Torsional RMSD (Primed vs Open)'],
    'Variation Energy Interaction': ['Variation Energy Interaction (Primed)', 'Variation of Energy Interaction (Open)'],
    'Energy of Interaction': [
        'Energy of Interaction residue muted (Primed)',
        'Energy of Interaction residue muted (Open)'
        'Energy of Interaction reference residue (Primed)',
        'Energy of Interaction reference residue (Open)'
    ],    
    # Ungrouped features
    'Ungrouped Features': [
        'Blosum', 'Conservation', 'Delta Rotatable Bonds', 'Number'
    ]
}

# Flatten the feature groups for dropdown options
dropdown_options = [{'label': key, 'value': ','.join(value)} for key, value in feature_groups.items()]

# Add ungrouped features to the dropdown options individually
for feature in feature_groups['Ungrouped Features']:
    dropdown_options.append({'label': feature, 'value': feature})


layout = html.Div([
    html.Div([
        html.H2('Human RyR1 variants created from our two models'),
        html.P('Start typing to search for a Variant file:'),
        dcc.Dropdown(
            id='search-dropdown',
            options=[{'label': f.split(".")[-2], 'value': f} for f in pdb_files[:5]],
            placeholder='Type to search...',
            className='dropdown'
        ),
        html.Div([
            # Molstar Viewer
            html.Div([
                dash_molstar.MolstarViewer(id='variant-viewer')
            ], className='molstar-container'),
            
            # DataTable
            html.Div([
                dcc.Dropdown(
                    id='feature-dropdown',
                    options=dropdown_options,
                    multi=True,
                    placeholder='Select additional features to display',
                    className='dropdown'
                ),
                dash_table.DataTable(
                    id='variant-data-table',
                    columns=[{'name': col, 'id': col} for col in initial_columns],
                    data=var[initial_columns].to_dict('records'),
                    page_size=19,
                    style_table={'width': '100%'},
                    style_header={'className': 'dash-header'},
                    style_cell={'className': 'dash-cell'}
                )
            ], className='datatable-container')
        ], className='content-container')
    ], className='variants-page-container')  
])



def register_callbacks(app):
    @app.callback(
        Output('search-dropdown', 'options'),
        [Input('search-dropdown', 'search_value')]
    )
    def update_dropdown_options(search_value): # for variants molestar
        if search_value:
            # Filter pdb_files based on search_value
            matching_files = [f for f in pdb_files if search_value.lower() in f.lower()]
            if not matching_files:
                return []
            return [{'label': f.split(".")[-2], 'value': f} for f in matching_files[:19]]  # Limit to 19 results
        else:
            # Show default subset of files if no search term
            return [{'label': f.split(".")[-2], 'value': f} for f in pdb_files[:5]]

    def create_molstar_component():
        """Create a Molstar component with a ball-and-stick representation."""
        return molstar_helper.create_component(
            label="Variant Representation",
            targets=molstar_helper.get_targets(chain=None, residue=[]),  # Adjust targets if needed
            representation='ball-and-stick'
        )


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

    @app.callback(
        [Output('variant-data-table', 'data'),
         Output('variant-data-table', 'columns')],
        [Input('search-dropdown', 'value'),
         Input('feature-dropdown', 'value')],
        [State('variant-data-table', 'columns')]
    )
    def update_table(selected_variant, selected_features, current_columns):
        if not selected_variant:
            raise dash.exceptions.PreventUpdate

        # Extract the number from the variant name
        #variant_number = selected_variant.split("_")[-2]#expression to adjust according our pdb type file, usually i did name my files with underscores
        variant_number = ''.join(filter(str.isdigit, selected_variant))

        # Filter the dataframe based on the variant number
        filtered_df = var[var['Position'].str.contains(variant_number)]

        columns_to_show = [col['name'] for col in current_columns]

        if selected_features:
            for feature in selected_features:
                if ',' in feature:  # This is a grouped feature
                    group_features = feature.split(',')
                    columns_to_show.extend([f.strip() for f in group_features if f.strip() in filtered_df.columns])
                elif feature in filtered_df.columns:
                    columns_to_show.append(feature)

        columns_to_show = list(dict.fromkeys(columns_to_show))  # Remove duplicates while preserving order
        columns = [{'name': col, 'id': col} for col in columns_to_show]
        data = filtered_df[columns_to_show].to_dict('records')

        return data, columns

        
# Example usage of fetching from a URL
# fetched_data = fetch_and_parse_pdb("https://example.com/path/to/pdb/file.pdb")