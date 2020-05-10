# Load the actual Connexion and Flask application instances from API service
# root
from goldfish.services.api import app, fapp

# Define simple function to register API spec into Connexion API instance
def register_api(name, spec):
    fapp.logger.info("Registering %s from API spec %s." % (name, spec))
    app.add_api(spec)

## Register APIs (from api_specs/)
# Log with the logger class from Flask application instance
fapp.logger.info("Registering APIs..")

# Note: Since our Connexion application is started with API dir api_specs, we
# only need to use filename here, not the full path!
register_api("Example Hello World API", "hello_world_api.yml")
register_api("Pebble API", "pebble_api.yml")