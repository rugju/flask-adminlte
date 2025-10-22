from flask import Blueprint

blueprint = Blueprint(
    'cryptobot_blueprint',
    __name__,
    url_prefix='/crypto'
)