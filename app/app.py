from flask import Flask

# basic flask app for the project
app = Flask(__name__)

# main page just to check server
@app.route("/")
def index():
    return "Invasive Species Monitoring System backend."

# simple test route so we can see different URL working
@app.route("/test")
def test():
    return "Test route is working."

# run the app directly (use debug during development)
if __name__ == "__main__":
    app.run(debug=True)