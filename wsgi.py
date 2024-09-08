import app  # Replace with the actual import statement for your app

application = app.app  # Replace with the variable name of your Dash app

if __name__ == "__main__":
    application.run_server(debug=True)  # Adjust debug as needed