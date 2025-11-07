from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

# instancias
app = Flask(__name__)
app.config.from_object("connection")
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# trunk-ignore(ruff/E402)
# trunk-ignore(ruff/F401)
from src import routes

# trunk-ignore(ruff/E402)
# trunk-ignore(ruff/F401)
from src.models import usuario_model

# trunk-ignore(ruff/E402)
# trunk-ignore(ruff/F401)
from src.services import usuario_service
