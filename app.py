from flask import Flask, abort
from flask_restful import Api, Resource, reqparse, inputs
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import sys

"""Api, app and sqlalchemy init"""
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)


class EventModel(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)


db.create_all()

"""Parsers for routes"""
parser = reqparse.RequestParser()
parser.add_argument(
    "event",
    type=str,
    help="The event name is required!",
    required=True
)
parser.add_argument(
    "date",
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)
parser_range_date = reqparse.RequestParser()
parser_range_date.add_argument(
    "start_time",
    type=inputs.date
)
parser_range_date.add_argument(
    "end_time",
    type=inputs.date
)


class Event(Resource):
    @staticmethod
    def get():
        args = parser_range_date.parse_args()
        res = []
        if not args["start_time"] or not args["end_time"]:
            for elem in EventModel.query.all():
                res.append({"id": elem.id, "event": elem.event, "date": str(elem.date)})
        else:
            for elem in EventModel.query.filter(EventModel.date >=
                                                args["start_time"].date(), EventModel.date <=
                                                args["end_time"].date()).all():
                res.append({"id": elem.id, "event": elem.event, "date": str(elem.date)})
        return res

    @staticmethod
    def post():
        args = parser.parse_args()
        data = EventModel(event=args["event"], date=args["date"])
        db.session.add(data)
        db.session.commit()
        return {"message": "The event has been added!", "id": data.id, "event": data.event, "date": str(data.date)}


class EventToday(Resource):
    @staticmethod
    def get():
        res = []
        for elem in EventModel.query.filter(EventModel.date == date.today()).all():
            res.append({"id": elem.id, "event": elem.event, "date": str(elem.date)})
        return res


class EventById(Resource):
    @staticmethod
    def get(event_id):
        event = EventModel.query.filter(EventModel.id == event_id).first()
        if not event:
            abort(404, "The event doesn't exist!")
        return {"id": event.id, "event": event.event, "date": str(event.date)}

    @staticmethod
    def delete(event_id):
        event = EventModel.query.filter(EventModel.id == event_id)
        if not event.first():
            abort(404, "The event doesn't exist!")
        event.delete()
        db.session.commit()
        return {"message": "The event has been deleted!"}, 200


"""Connecting classes with routes"""
api.add_resource(Event, '/event')
api.add_resource(EventToday, '/event/today')
api.add_resource(EventById, '/event/<int:event_id>')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
