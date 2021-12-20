from flask import Flask
from flask_restful import Api
from resources.rest import City, Means, Records, Moving

app = Flask(__name__)
app.config['DEBUG'] = True
api = Api(app)


@app.errorhandler(404)
def page_not_found(e):
    """Note that we set the 404 status explicitly"""
    return {'message': 'Route was not found'}, 404


api.add_resource(City, '/cities')
api.add_resource(Means, '/means/<string:value_type>/<string:city>')
api.add_resource(Records, '/records/<string:city>/<string:start_dt>/<string:end_dt>')
api.add_resource(Moving, '/moving_mean/<string:value_type>/<string:city>')

if __name__ == '__main__':
    app.run()
