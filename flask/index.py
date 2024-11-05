from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app, resources={
     r"/api/qr-data": {"origins": "http://localhost:8080"},
     r"/view-data": {"origins": "http://localhost:8080"}
})

@app.route("/",methods=['GET'])
def index():
    return "<h1>Reload test</h1>"


class QRData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_content = db.Column(db.String(255), nullable=False)


# 読み取ったデータを渡すエンドポイント
@app.route('/api/qr-data', methods=['POST'])
def receive_qr_data():
    data = request.get_json()

    qr_data = QRData(code_content=data['code_content'])
    db.session.add(qr_data)
    db.session.commit()

    return jsonify({'message': 'QR data received successfully'}), 201

@app.route('/view-data', methods=['GET'])
def view_data():
    # データベースからすべてのQRコードデータを取得
    qr_data_list = QRData.query.all()
    # データをHTMLテンプレートに渡して表示
    return jsonify([{'id': data.id, 'code_content': data.code_content} for data in qr_data_list])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
