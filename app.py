from flask import Flask, jsonify
from movies_bp import movies_bp
from models import db

app = Flask(__name__)
app.register_blueprint(movies_bp)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.sqlite3'
app.secret_key = 'Secret@1234'
db.init_app(app)

@app.errorhandler(404)
def handle_not_found_error(err):
    print(err)
    return jsonify({'Error': str(err)})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)