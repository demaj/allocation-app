from datetime import datetime

from flask import Flask, request
from flask.json import jsonify

from allocation import bootstrap, views
from allocation.domain import commands
from allocation.service_layer.handlers import InvalidSku

app = Flask(__name__)
bus = bootstrap.bootstrap()


@app.route("/add_batch", methods=["POST"])
def add_batch():
    eta = request.json["eta"]
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    cmd = commands.CreateBatch(
        request.json["ref"], request.json["sku"], request.json["qty"], eta
    )
    bus.handle(cmd)
    return "OK", 201


@app.route("/allocaate", methods=["POST"])
def allocate_endpoint():
    try:
        cmd = commands.Allocate(
            request.json["order_id"], request.json["sku"], request.json["qty"]
        )
        bus.handle(cmd)
    except InvalidSku as e:
        return {"message": str(e)}, 400

    return "OK", 202


@app.route("/allocations/<order_id>", methods=["GET"])
def allocations_view_endpoint(order_id):
    result = views.allocations(order_id, bus.uow)
    if not result:
        return "not found", 404
    return jsonify(result), 200
