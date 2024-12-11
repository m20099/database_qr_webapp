from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# CORS 設定
CORS(app, resources={
     r"/api/register": {"origins": "http://localhost:8080"},
     r"/view-data": {"origins": "http://localhost:8080"},
     r"/api/login": {"origins": "http://localhost:8080"},
     r"/api/user-info": {"origins": "http://localhost:8080"}
})

# localhost:5000/
@app.route("/",methods=['GET'])
def index():
    return "<h1>Reload test</h1>"

# demo version用db定義
class QRData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(255), nullable=False)
    store_location = db.Column(db.String(255), nullable=False)
    store_description = db.Column(db.String(255), nullable=False)

# ユーザ情報登録テーブル
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 購入履歴管理テーブル
class PurchaseRecord(db.Model):
    __tablename__ = 'purchase_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    store_id = db.Column(db.String(50), nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)

class PurchaseItem(db.Model):
    __tablename__ = 'purchase_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase_records.id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


# 読み取ったデータを渡すエンドポイント
@app.route('/api/qr-data', methods=['POST'])
def receive_qr_data():
    data = request.get_json()

    store_name = data['storeName']
    store_location = data['storeLocation']
    store_description = data['storeDescription']
    
    qr_data = QRData(
        store_name=store_name,
        store_location=store_location,
        store_description=store_description
    )
    
    db.session.add(qr_data)
    db.session.commit()

    return jsonify({'message': 'QR data received successfully'}), 201

# ユーザ登録のエンドポイント
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'そのユーザー名は既に使用されています'}), 409
    
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'そのメールアドレスは既に使用されています'}), 409

    hashed_password = generate_password_hash(password)

    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'ユーザー登録成功'}), 201

# ログイン時にデータを渡すエンドポイント
@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()

    if user is None:
        return jsonify({'message': 'ユーザーが存在しません'}), 401
    if not check_password_hash(user.password, password):
        return jsonify({'message': 'パスワードが間違っています'}), 401

    return jsonify({'message': 'Login successful', 'user_id': user.id}), 200

# ユーザー情報取得エンドポイント
@app.route('/api/user-info', methods=['GET'])
def get_user_info():
    token = request.headers.get('Authorization').split(" ")[1]  # Bearerトークンを取得
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['user_id']
        user = User.query.get(user_id)
        
        if user:
            return jsonify({'username': user.username, 'email': user.email}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

# ユーザ登録情報確認用のエンドポイント
@app.route('/view-users', methods=['GET'])
def view_users():
    # ユーザー情報をすべて取得
    users_list = User.query.all()
    
    users_data = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')  # 日付フォーマット
        }
        for user in users_list
    ]
    
    return jsonify(users_data), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
