from flask import Flask
from flask import jsonify
import connexion
from joblib import load



app = connexion.App(__name__, specification_dir="./")

app.add_api("master.yaml")

@app.route("/")
def home():
	msg = {"Server working": "/list for functionality"}
	return jsonify(msg)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, debug=True)
