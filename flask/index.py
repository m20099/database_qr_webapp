from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

app = Flask(__name__)
load_dotenv()

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# CORS 設定
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}, r"/view-*": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/api/*": {"origins": "http://192.168.128.115:8080"}, r"/view-*": {"origins": "http://192.168.128.115:8080"}})
CORS(app, resources={r"/api/*": {"origins": "http://172.24.15.14:8080"}, r"/view-*": {"origins": "http://172.24.15.33:8080"}})

# localhost:5000/
@app.route("/",methods=['GET'])
def index():
    return "<h1>Reload test</h1>"

# ユーザ情報登録テーブル
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

# ユーザー設定テーブル
class UserSettings(db.Model):
    __tablename__ = 'user_settings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    budget_limit = db.Column(db.Float, nullable=False, default=10000)

# レシート管理テーブル
class PurchaseRecord(db.Model):
    __tablename__ = 'purchase_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    store_id = db.Column(db.String(50), nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)

# 購入商品テーブル
class PurchaseItem(db.Model):
    __tablename__ = 'purchase_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase_records.id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False) 

# 商品テーブル
class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(100), nullable=False)
    price = price = db.Column(db.Float, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

# 店名テーブル
class Store(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_name = db.Column(db.String(100), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

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

# /signup
# ユーザ登録のエンドポイント
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    errors = {}
    if User.query.filter_by(username=username).first():
        errors['username'] = 'そのユーザー名は既に使用されています'
    if User.query.filter_by(email=email).first():
        errors['email'] = 'そのメールアドレスは既に使用されています'
    if errors:
        return jsonify({'errors': errors}), 409
    
    hashed_password = generate_password_hash(password)

    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'ユーザー登録成功'}), 201

# /login
# ログイン時にデータを渡すエンドポイント
@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username, is_deleted=False).first()

    if user is None:
        return jsonify({'message': 'ユーザーが存在しません'}), 401
    if not check_password_hash(user.password, password):
        return jsonify({'message': 'パスワードが間違っています'}), 401
    
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))

    return jsonify({'message': 'Login successful', 'token': access_token, 'user': user.id}), 200

# ユーザー情報取得エンドポイント
@app.route('/api/user-info', methods=['GET'])
def get_user_info():
    token = request.headers.get('Authorization').split(" ")[1]
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
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_deleted': user.is_deleted,
        }
        for user in users_list
    ]
    
    return jsonify(users_data), 200

# /receipt_simulator
# 商品登録用エンドポイント
@app.route('/api/itemregister', methods=['POST'])
def register_item():
    data = request.get_json()
    
    item_name = data.get('item_name')
    price = data.get('price')

    item = Item(item_name=item_name, price=price)
    db.session.add(item)
    db.session.commit()

    return jsonify({'message': '商品登録成功'}), 201

# 商品削除用エンドポイント
@app.route('/api/delete-item/<int:item_id>', methods=['PUT'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        return jsonify({'message': '商品が見つかりませんでした。'}), 404
    try:
        item.is_deleted = True
        db.session.commit()
        return jsonify({'message': '商品が論理削除されました。'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '削除に失敗しました。', 'error': str(e)}), 500

# 店舗登録用エンドポイント
@app.route('/api/storeregister', methods=['POST'])
def register_store():
    data = request.get_json()
    
    store_name = data.get('store_name')

    new_store = Store(store_name=store_name)
    db.session.add(new_store)
    db.session.commit()
    
    return jsonify({"message": "店舗が登録されました。"}), 201

# 店舗削除用エンドポイント
@app.route('/api/delete-store/<int:store_id>', methods=['PUT'])
def delete_store(store_id):
    store = Store.query.get(store_id)
    if store is None:
        return jsonify({'message': '店名が見つかりませんでした。'}), 404
    try:
        store.is_deleted = True
        db.session.commit()
        return jsonify({'message': '店舗が論理削除されました。'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '削除に失敗しました。', 'error': str(e)}), 500

# 登録商品一覧取得用エンドポイント
@app.route('/api/view-items', methods=['GET'])
def view_items():
    items_list = Item.query.filter_by(is_deleted=False).all()

    items_data = [
        {
            'id': item.id,
            'item_name': item.item_name,
            'price': item.price
        }
        for item in items_list
    ]
    
    return jsonify(items_data), 200

# 店舗一覧取得用エンドポイント
@app.route('/api/view-stores', methods=['GET'])
def view_stores():
    stores = Store.query.filter_by(is_deleted=False).all()
    result = [{"id": store.id, "store_name": store.store_name} for store in stores]
    return jsonify(result), 200

#QRコード読み取り時用エンドポイント
@app.route('/api/purchases', methods=['POST'])
def create_purchase():
    # リクエストデータ受け取り
    data = request.get_json()

    # 各データ取得
    user_id = data['user_id']
    store_id = data['store_id']
    purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d %H:%M')
    items = data['items']

    # 重複チェック
    existing_purchase = PurchaseRecord.query.filter_by(
        user_id=user_id,
        store_id=store_id,
        purchase_date=purchase_date
    ).first()

    if existing_purchase:
        return jsonify({'error': '同じ日時の購入データがすでに存在します！'}), 400

    # 合計金額の計算
    total_amount = sum(item['price'] * item['quantity'] for item in items)

    # データベース登録
    purchase_record = PurchaseRecord(
        user_id=user_id,
        store_id=store_id,
        purchase_date=purchase_date,
        total_amount=total_amount
    )
    db.session.add(purchase_record)
    db.session.commit()

    for item in items:
        purchase_item = PurchaseItem(
            purchase_id=purchase_record.id,
            item_name=item['item_name'],
            price=item['price'],
            quantity=item['quantity']
        )
        db.session.add(purchase_item)

    db.session.commit()

    return jsonify({'message': '購入データが正常に登録されました！'}), 201

#購入データ確認用エンドポイント
@app.route('/api/purchases', methods=['GET'])
def get_all_purchases():
    try:
        # レシート管理テーブルのデータ取得
        purchase_records = PurchaseRecord.query.all()
        purchase_items = PurchaseItem.query.all()

        # レシート管理テーブルの内容をリストに格納
        purchase_results = []
        for record in purchase_records:
            purchase_results.append({
                'purchase_id': record.id,
                'user_id': record.user_id,
                'store_id': record.store_id,
                'purchase_date': record.purchase_date.strftime('%Y-%m-%d %H:%M'),
                'total_amount': record.total_amount
            })

        # 購入商品テーブルの内容をリストに格納
        item_results = []
        for item in purchase_items:
            item_results.append({
                'purchase_id': item.purchase_id,
                'item_name': item.item_name,
                'price': item.price,
                'quantity': item.quantity
            })

        return jsonify({
            'purchase_records': purchase_results,
            'purchase_items': item_results
        }), 200

    except Exception as e:
        return jsonify({'message': f'エラー: {str(e)}'}), 500

@app.route('/api/receipts', methods=['GET'])
def get_receipts():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    try:
        # ユーザーに関連する購入履歴を取得
        purchase_records = PurchaseRecord.query.filter_by(user_id=user_id).all()

        # 結果を整形
        result = []
        for record in purchase_records:
            # 購入商品データを直接使用
            items = PurchaseItem.query.filter_by(purchase_id=record.id).all()
            item_details = []
            for item in items:
                item_details.append({
                    "id": item.id,                     # アイテムID
                    "item_name": item.item_name,       # 商品名
                    "price": item.price,               # 単価
                    "quantity": item.quantity          # 数量
                })

            # 店舗情報の取得
            store = Store.query.filter_by(id=record.store_id, is_deleted=False).first()
            store_name = store.store_name if store else "Unknown"

            # レスポンスデータに整形
            result.append({
                "id": record.id,                         # レシートID
                "store_name": store_name,                # 店舗名
                "purchase_date": record.purchase_date,   # 購入日
                "items": item_details                    # 購入商品リスト
            })

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ユーザIDに対応した購入データを引っ張ってくるエンドポイント
@app.route('/api/purchases/<int:user_id>', methods=['GET'])
def get_purchases(user_id):
    purchases = PurchaseRecord.query.filter_by(user_id=user_id).all()
    if not purchases:
        return jsonify({'message': '購入データがありません'}), 404

    result = []
    for purchase in purchases:
        result.append({
            'purchase_id': purchase.id,
            'user_id': purchase.user_id,
            'store_id': purchase.store_id,
            'purchase_date': purchase.purchase_date.strftime('%Y-%m-%d %H:%M'),
            'total_amount': purchase.total_amount
        })

    return jsonify(result), 200

@app.route('/api/username/<int:user_id>', methods=['GET'])
def get_username(user_id):
    user = User.query.filter_by(id=user_id, is_deleted=False).first()
    
    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        'user_name': user.username
    })

# ユーザ設定反映用エンドポイント
@app.route('/api/setting', methods=['POST'])
def save_user_setting():
    data = request.json
    user_id = data.get('user_id')
    budget_limit = data.get('budget_limit')

    setting = UserSettings.query.filter_by(user_id=user_id).first()
    if setting:
        setting.budget_limit = budget_limit
    else:
        setting = UserSettings(user_id=user_id, budget_limit=budget_limit)
        db.session.add(setting)

    db.session.commit()
    return jsonify({'message': '設定が保存されました！'}), 200

@app.route('/api/setting/<int:user_id>', methods=['GET'])
def get_user_setting(user_id):
    # User と UserSettings を結合してデータを取得
    user = db.session.query(User, UserSettings).join(
        UserSettings, User.id == UserSettings.user_id
    ).filter(User.id == user_id, User.is_deleted == False).first()

    if user:
        user_data = {
            'username': user.User.username,
            'email': user.User.email,
            'created_at': user.User.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'budget_limit': user.UserSettings.budget_limit
        }
        return jsonify(user_data), 200

    return jsonify({'error': 'User not found'}), 404

@app.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.is_deleted = True
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
