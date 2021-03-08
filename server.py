from flask import Flask, render_template, request
from flask import jsonify
import os
import connexion

app = connexion.App(__name__, specification_dir="./")

app.add_api("master.yaml")

@app.route("/")
def home():
	msg = {"msg": "It's really working!"}
	return jsonify(msg)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, debug=True)
