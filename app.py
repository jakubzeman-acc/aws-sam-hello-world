from flask_lambda import FlaskLambda, logging


app = FlaskLambda(__name__)


@app.route("/")
def hello():
    logging.info("Root endpoint called.")
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)
