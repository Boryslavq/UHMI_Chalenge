from flask import jsonify
from flask_restful import Resource
from sqlalchemy import inspect

from resources.helpers import moving_average, convert_time
from utils.database import ConnectDB, Cities, Statistic

db = ConnectDB()


class City(Resource):
    def get(self):
        cities = db.session.query(Cities).all()
        db.session.close()
        if cities:
            cities = [i.city for i in cities]
            return jsonify({'cities': cities})
        return {"message": "Cities not found "}, 404


class Means(Resource):
    def get(self, value_type, city):
        table = inspect(Statistic)
        columns = [c.name for c in table.columns]
        if value_type in columns:
            try:
                city_id = db.session.query(Cities).filter_by(city=city).first().id
                chosen_filters = db.session.query(Statistic).filter_by(city_id=city_id).all()
                result = round(sum([getattr(i, value_type) for i in chosen_filters]) / len(chosen_filters), 2)
                return jsonify({city: {f'Average {value_type}': result}})
            except AttributeError:
                return {'message': 'City was not found'}, 404
            finally:
                db.session.close()
        db.session.close()
        return {'message': 'Value type not found'}, 404


class Records(Resource):
    def get(self, city, start_dt, end_dt):
        try:
            json = []
            city_id = db.session.query(Cities).filter_by(city=city).first().id

            chosen_filters = db.session.query(Statistic).filter_by(city_id=city_id).filter(
                (Statistic.date.between(start_dt, end_dt))).all()

            for atr in chosen_filters:
                json.append({'city': city, 'date': convert_time(atr.date),
                             'weather': {'temp': atr.temp, 'pcp': atr.pcp, 'clouds': atr.clouds,
                                         'pressure': atr.pressure, 'humidity': atr.humidity,
                                         'wind_speed': atr.wind_speed}})
            if len(json) > 0:
                return jsonify(json)
            else:
                return {"message": "Date was not found"}, 404
        except AttributeError:
            return {"message": "Not found"}, 404
        finally:
            db.session.close()


class Moving(Resource):
    def get(self, value_type, city):
        table = inspect(Statistic)
        columns = [c.name for c in table.columns]
        if value_type in columns:
            try:
                city_id = db.session.query(Cities).filter_by(city=city).first().id
                chosen_filters = db.session.query(Statistic).filter_by(city_id=city_id).all()
                result = [getattr(i, value_type) for i in chosen_filters]
                mov_avr = moving_average(result)
                return jsonify({'city': city, 'type_of_calc': 'moving avarage', 'result': f'{value_type}: {mov_avr}'})
            except AttributeError:
                return {"message": "City not found"}, 404
            finally:
                db.session.close()
        db.session.close()
        return {'message': ' Value type not found'}, 404
