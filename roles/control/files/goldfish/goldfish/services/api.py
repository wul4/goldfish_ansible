import connexion
import logging

# app = Connextion application instance
app = connexion.App(__name__, specification_dir='../api_specs/')

# fapp = Flask application instance
fapp = app.app

# logger = Flask application instance logger, other modules can load logger from
# here to log!
fapp.logger.setLevel(logging.INFO)
logger = fapp.logger

# Start the actual APIs by registering them into the Connexion API instance
# Register APIs
import goldfish.api.register
