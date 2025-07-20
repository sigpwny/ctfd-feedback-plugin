from flask_restx import Namespace, Resource, Api
from flask import Blueprint, request, session

from CTFd.utils import config
from CTFd.models import Challenges, Solves, Users, db, Teams
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
            chalID = request.form('challenge_id')
            team_id = get_current_team
            user = get_current_user()
            solves = Solves.query\
                    .join(Teams, Solves.team_id == Teams.id)\
                    .filter(Solves.teamid == session['id'])\
                    .all()
            solve_IDs = []
            for solve in solves:
                solve_IDs.append(chalID)
            
            if(chalID in solve_IDs):
                 feedback_dif= request.form('feedback_d')
                 feedback_qual = request.form('feedback_q')
                 feedback_difficulty = None
                 feedback_quality = None
                 try:
                     feedback_difficulty = int(feedback_dif)
                     feedback_quality = int(feedback_qual)
                 except:
                     return {"message" : "Bad Request"}, 400
                 if(feedback_dif > 10 or feedback_dif < 1):
                     return {"message" : "Bad Request"}, 400
                 if(feedback_qual > 10 or feedback_qual < 1):
                    return {"message" : "Bad Request"}, 400
                 feed = FeedbackTable(chalID, user, team_id, feedback_quality, feedback_difficulty)
                 db.session.add(feed)
                 db.session.commit()
                 db.session.close()
                 return {"message": "Feedback Posted"}, 201
            else:
                return {"message":"Challenge Not Solved"}, 403

        else:
            # handle feedback for individual user
            # need to find a way to check if the user has solved a given challenge then post a difficulty and feedback score for that challenge
            chalID = request.form('challenge_id')
            team_id = get_current_team
            user = get_current_user()
            solves = get_solve_ids_for_user_id(user)
            if(chalID in solves):
                 feedback_dif= request.form('feedback_d')
                 feedback_qual = request.form('feedback_q')
                 feedback_difficulty = None
                 feedback_quality = None
                 try:
                     feedback_difficulty = int(feedback_dif)
                     feedback_quality = int(feedback_qual)
                 except:
                     return {"message" : "Bad Request"}, 400
                 if(feedback_dif > 10 or feedback_dif < 1):
                     return {"message" : "Bad Request"}, 400
                 if(feedback_qual > 10 or feedback_qual < 1):
                    return {"message" : "Bad Request"}, 400
                 feed = FeedbackTable(chalID, user, team_id, feedback_quality, feedback_difficulty)
                 db.session.add(feed)
                 db.session.commit()
                 db.session.close()
                 return {"message": "Feedback Posted"}, 201

            else:
                return {"message":"Challenge Not Solved"}, 403
                
            
           
               
                
            
    
#table for feedback
class FeedbackTable(db.Model):
    feedback_id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id", onedelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id", ondelete="CASCADE"))
    feedback_quality = db.Column(db.Integer)
    feedback_difficulty = db.Column(db.Integer)
    

    def __init__(self, challenge_id, user_id, team_id, feedback_quality, feedback_difficulty):
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
   

    
    
        

