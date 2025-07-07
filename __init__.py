from flask_restx import Namespace, Resource, Api
from flask import Blueprint

from CTFd.utils import config
from CTFd.utils.user import get_current_user, authed

plugin_namespace = Namespace('feedback', description="Endpoint for challenge feedback")

@plugin_namespace.route('')
class Feedback(Resource):
    def get(self):
        if not authed():
            return {"message": "Unauthorized"}, 401
        user = get_current_user()
        if not user:
            return {"message": "User not found"}, 404
        return {
            "message": f"Hello {user.name}"
        }

    def post(self):
        if config.is_teams_mode():
            # handle feedback for team
            pass
        else:
            # handle feedback for individual user
            pass

def load(app):
    api = Blueprint("feedback_api", __name__, url_prefix="/api/v1")
    ctfd_flask_api = Api(api, version="v1", doc=app.config.get("SWAGGER_UI"))
    ctfd_flask_api.add_namespace(plugin_namespace, "/feedback")
    app.register_blueprint(api)

