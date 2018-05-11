from flask_lambda import FlaskLambda


app = FlaskLambda(__name__)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)
