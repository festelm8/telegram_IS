from flask_restful import Resource

from src.lib.access import user_only


class PingAPI(Resource):
    @user_only()
    def get(self):
        return "pong"
