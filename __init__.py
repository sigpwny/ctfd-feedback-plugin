from flask_restx import Namespace, Resource, Api
from flask import Blueprint

from CTFd.utils import config
from CTFd.models import Challenges, Solves, Users, db
from CTFd.utils.user import get_current_user, authed
from CTFd.utils.user import get_current_team
from CTFd.utils.challenges import get_solve_ids_for_user_id, get_solves_for_challenge_id


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
            
            # handle feedback for teams
            pass
        else:
            # handle feedback for individual user
            # need to find a way to check if the user has solved a given challenge then post a difficulty and feedback score for that challenge
            user = get_current_user()
            solveIDs = get_solves_for_challenge_id(chalID)
            feedback_dif = None
            feedback_qual = None
            if(user in solveIDs):
                #ensure user inputs a score only within the valid range for both inputs.
                while(True):
                    try:
                        feedback_dif = int(input(f"How difficult was this challenge on a scale of 1-10? (whole numbers only)"))
                    except ValueError: 
                        print(f"Error: Not an Integer")
                    else:
                        if (feedback_dif > 10 or feedback_dif < 0):
                            print(f"Value not in accepted range")
                        else:
                            break
                while(True):          
                     try:
                        feedback_qual = int(input(f"How much did you like this challenge on a scale of 1-10? (whole numbers only)"))
                     except ValueError: 
                        print(f"Error: Not an Integer")
                     else:
                        if (feedback_qual > 10 or feedback_qual < 0):
                            print(f"Value not in accepted range")
                        else:
                            break
            pass
    
#table for feedback
class FeedbackTable(db.Model):
    feedback_id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id", onedelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id", ondelete="CASCADE"))
    feedback_quality = db.Column(db.Integer)
    feedback_difficulty = db.Column(db.Integer)
    

    def __init__(self, feedback_id, challenge_id, user_id, team_id, feedback_quality, feedback_difficulty):
        self.feedback_id = feedback_id
        self.challenge_id = challenge_id
        self.user_id = user_id
        self.team_id = team_id
        self.feedback_difficulty = feedback_difficulty
        self.feedback_quality = feedback_quality

    #contains new routes for table
def load(app):
    app.db.create_all()
    api = Blueprint("feedback_api", __name__, url_prefix="/api/v1")
    ctfd_flask_api = Api(api, version="v1", doc=app.config.get("SWAGGER_UI"))
    ctfd_flask_api.add_namespace(plugin_namespace, "/feedback")
    app.register_blueprint(api)
    @app.route('/api/v1/feedback', methods=['GET'])
    def view_feedback_qual(challenge_id):
        pass
    def view_feedback_diff(challenge_id):
        pass
    @app.route('/api/v1/feedback', methods=['POST'])
    def post_feedback_diff(challenge_id, feedback_score):
        pass
    def post_feedback_qual(challenge_id, feedback_score):
        pass
        

    
    
        

