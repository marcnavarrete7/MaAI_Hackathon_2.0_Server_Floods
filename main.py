from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def home():
    return "test response"

if __name__ == "__main__":
    app.run(debug=True)
