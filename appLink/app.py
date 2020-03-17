from flask import Flask, render_template
from flask_cors import CORS

from routes.linkRoute import linksBP

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:8000/*",
                "http://localhost:8080/*",
                "http://192.168.100.142:8000/*",
                "http://192.168.100.142:8080/*",
                "http://192.168.0.4:8000/*",
                "http://192.168.0.4:8080/*",
                "http://172.20.10.2:8000/*",
                "http://172.20.10.2:8080/*"                
            ]
        }
    }
)

app.register_blueprint(linksBP)

app.run(host='localhost', port=8000, debug=True)