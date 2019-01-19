from flask import jsonify

def createJsonResponse(jsonBody):
    return jsonify(jsonBody)