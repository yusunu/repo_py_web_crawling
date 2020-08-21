from tripadv.main_tripadv import trigger_Restaurant_tripa
from flask import Flask

app = Flask(__name__)


@app.route('/api/refresh_location')
def refresh():
    trigger_Restaurant_tripa()


if __name__ == "__main__":
    app.run()
