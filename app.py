
from flask import Flask , request , jsonify
import cs50

app = Flask(__name__)
db = cs50.SQL("sqlite:///stock.db")

@app.route('/')
def home():
    return "Hello, World!"

@app.route("register" , methods = ["POST"])
def register():
    if request.method == "POST":
        data = request.json
        mail= data["mail"]
        username = data["username"]
        password= data["password"]
        c_password = data["confirm_password"]
        if password == c_password:
            users  = db.execute("select * from users")
            id = 0 
            for user in users:
                id +=1
                if user["mail"] == mail or user["username"] == username:
                    return jsonify({"message" : "username or mail already exists"})
            db.execute("INSERT INTO users (id ,mail , username , password) VALUES (?,?,?,?)", id , mail , username , password)
            return jsonify({"message" : "user created successfully" , "id":id})
        else:
            return jsonify({"message": "Passwords do not match"}), 400
    return jsonify({"message":"mehtod not allowed"})    

@app.route("/login" , methods = ["POST"])
def login():
    if request.method == "POST":
        data = request.json
        mail = data["mail"]
        password = data["password"]
        users = db.execute("SELECT * FROM users WHERE mail = ? AND password = ?", mail ,password)
        id  = users[0]["id"]
        return jsonify({"message" : "logged in successfully" , "id":id})
    else:
        return jsonify({"message":"method not allowed"})
    

@app.route("/save_stock" , methods = ["POST"])
def save_stock():
    if request.method == "POST":
        data = request.json
        id = data["id"]
        stock = data["stock"]
        db.execute("INSERT INTO stock (id , stock) VALUES (?,?)", id , stock)
        return jsonify({"message" : "stock saved successfully" , "id":id})
    else:
        return jsonify({"message":"method not allowed"})
    
@app.route("/show_stocks")
def show_stocks():
    id = request.args.get("id")
    stocks = db.execute("SELECT * FROM stock WHERE id = ?", id)
    return jsonify({"stocks":stocks})


if __name__ == '__main__':
    app.run(debug=True)
