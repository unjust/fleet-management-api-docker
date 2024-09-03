from typing import Optional
import json
from datetime import datetime
import yaml
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException, BadRequest # NotFound, InternalServerError
from .models import taxis
from .models import trajectories
from .config import Config
from .spec import spec

DEFAULT_PAGE = 1
ROWS_PER_PAGE = 10

def create_app(cfg: Optional[Config] = None) -> Flask:
    if cfg is None:
        cfg = Config()

    app = Flask(__name__)
    app.config.from_object(cfg)

    @app.route("/taxis", methods=["GET"])
    def get_taxis():
        """Endpoint to get list of taxis
        ---
        get:
          description: Get taxi list
          parameters:
            - in: query
              name: page
              schema:
                type: integer
              required: false
              description: Page number of results
            - in: query
              name: per_page
              schema:
                type: integer
              required: false
              description: Number of results per page
          responses:
            200:
              description: Returns the list of taxis
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      taxis:
                        type: array
                        items:
                          $ref: '#/components/schemas/TaxiModel'
                      count:
                        type: integer
        """
        page = request.args.get("page", DEFAULT_PAGE, type=int)
        per_page = request.args.get("limit", ROWS_PER_PAGE, type=int)
        taxis_response = taxis.get(page, per_page)
        response = {"taxis": taxis_response, "count": len(taxis_response)}
        return jsonify(response)

    @app.route("/trajectories", methods=["GET"])
    def get_trajectories_by_taxi_id():
        """Endpoint to get list of trajectories for a specific taxi
        ---
        get:
          description: Get trajectories list
          parameters:
            - in: query
              name: taxiId
              schema:
                type: integer
              required: true
              description: taxi id
            - in: query
              name: date
              schema:
                type: string
              required: true
              description: Date format DD-MM-YYYY
            - in: query
              name: page
              schema:
                type: integer
              required: false
              description: Page number of results
            - in: query
              name: per_page
              schema:
                type: integer
              required: false
              description: Number of results per page
          responses:
            200:
              description: Return trajectories list for a specific taxi
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      trajectories:
                        type: array
                        items:
                          $ref: '#/components/schemas/trajectoriesModel'
        """
        # pdb.set_trace()
        date = request.args.get("date", None, type=str) # date format yyyy-MM-dd
        if date is None:
            return handle_exception(BadRequest("Missing date parameter"))
        try:
            date = datetime.strptime(date, '%d-%m-%Y').date()
        except ValueError:
            return handle_exception(BadRequest("Invalid date format, use DD-MM-YYYY"))

        taxi_id = request.args.get("taxiId", type=int)
        page = request.args.get("page", DEFAULT_PAGE, type=int)
        per_page = request.args.get("limit", ROWS_PER_PAGE, type=int)
        results = trajectories.get_trajectories_by_taxi_id(taxi_id, page, per_page, date)
        return jsonify(results)

    @app.route("/trajectories/latest", methods=["GET"])
    def get_latest_trajectories():
        """Endpoint to get last location (trajectory) of all taxis
        ---
        get:
          description: Get last location (trajectory) of all taxis
          parameters:
            - in: query
              name: page
              schema:
                type: integer
              required: false
              description: Page number of results
            - in: query
              name: per_page
              schema:
                type: integer
              required: false
              description: Number of results per page
          responses:
            200:
              description: Returns the list of last location of all taxis
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      taxis:
                        type: array
                        items:
                          $ref: '#/components/schemas/trajectoriesModel'
        """
        page = request.args.get("page", DEFAULT_PAGE, type=int)
        # https://werkzeug.palletsprojects.com/en/3.0.x/datastructures/#werkzeug.datastructures.MultiDict.get
        per_page = request.args.get("limit", ROWS_PER_PAGE, type=int)
        results = trajectories.get_latest_trajectories(page, per_page)
        return jsonify(results)

    # https://code-maven.com/python-flask-catch-exception
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify({ 'message': e.description }), e.code
        return jsonify({ 'message': str(e) }), 500

    # Register the path and the entities within it
    # Since path inspects the view and its route,
    # we need to be in a Flask request context
    with app.test_request_context():
        spec.path(view=get_taxis)
        spec.path(view=get_trajectories_by_taxi_id)
        spec.path(view=get_latest_trajectories)
    # Both .yaml & .json files are being generated but we
    # are aware we just need one of them
    with open("swagger.yaml", "w", encoding="utf-8") as file:
        yaml.dump(spec.to_yaml(), file, line_break="\n", indent=4)
    with open("swagger.json", "w", encoding="utf-8") as file:
        json.dump(spec.to_dict(), file)
    return app

if __name__ == "__main__":
    taxi_app = create_app()
    taxi_app.run()
