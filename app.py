import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
# Import of the page modules here
import pages.index as index
import pages.presentation as presentation
import pages.modele as modele
import pages.variants as variants
import pages.contact as contact

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=["style", dbc.themes.BOOTSTRAP])

def nav_bar():
    return dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand("RyR1 Study", href="/", className="text-white"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink('Accueil', href='/', className="nav-link")),
                    dbc.NavItem(dbc.NavLink('RyR1 Overview', href='/presentation', className="nav-link")),
                    dbc.NavItem(dbc.NavLink('Human RyR1 Models', href='/modele', className="nav-link")),
                    dbc.NavItem(dbc.NavLink('Variants', href='/variants', className="nav-link")),
                    dbc.NavItem(dbc.NavLink('About me', href='/contact', className="nav-link")),
                ],
                className="ml-auto d-flex align-items-center",
                navbar=True
            ),
        ]),
        color="primary",
        dark=True,
        className="mb-4",
    )

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav_bar(),
    html.Div(id='page-content', className='container-fluid')  
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index.layout
    elif pathname == '/presentation':
        return presentation.layout
    elif pathname == '/modele':
        return modele.layout
    elif pathname == '/variants':
        return variants.layout
    elif pathname == '/contact':
        return contact.layout
    else:
        return html.H1('404: Page not found')

modele.register_callbacks(app)
variants.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)