from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

latest_data = {
    "average": 0,
    "category": "Waiting"
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/boot-data", methods=["POST"])
def boot_data():
    global latest_data

    data = request.get_json()

    average = int(data.get("average", 0))

    if average < 20:
        category = "Very Low"
    elif average < 40:
        category = "Low"
    elif average < 60:
        category = "Medium"
    elif average < 80:
        category = "High"
    else:
        category = "Very High"

    latest_data = {
        "average": average,
        "category": category
    }

    return jsonify(latest_data)


@app.route("/api/latest", methods=["GET"])
def get_latest():
    return jsonify(latest_data)

if __name__ == "__main__":
    app.run()