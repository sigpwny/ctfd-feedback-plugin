from flask_restx import Namespace, Resource, Api
from flask import Blueprint

plugin_namespace = Namespace('feedback', description="Endpoint for challenge feedback")

@plugin_namespace.route('')
class CSRFToken(Resource):
    def get(self):
        return {
            "message": "Hello, world!"
        }

def load(app):
    api = Blueprint("feedback_api", __name__, url_prefix="/api/v1")
    ctfd_flask_api = Api(api, version="v1", doc=app.config.get("SWAGGER_UI"))
    ctfd_flask_api.add_namespace(plugin_namespace, "/feedback")
    app.register_blueprint(api)

