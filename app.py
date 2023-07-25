from flask import Flask, render_template,request,redirect, url_for, session
import random,string
import db
from datetime import timedelta


app = Flask(__name__)
app.secret_key=''.join(random.choices(string.ascii_letters, k=256))

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')   # Redirect された時のパラメータ受け取り

    if msg == None:
        # 通常のアクセスの場合
        return render_template('index.html')
    else :
        # register_exe() から redirect された場合
        return render_template('index.html', msg=msg)

@app.route('/', methods=['POST'])
def login():
    # error = 'ログインに失敗しました。'
    # return render_template('index.html', error=error)
    user_name=request.form.get('username')
    password=request.form.get('password')
    # ログイン判定
    if db.login(user_name, password):
        session["user"] = True  # session にキー：'user', バリュー:True を追加
        session.permanent = True  # session の有効期限を有効化
        app.permanent_session_lifetime = timedelta(minutes=10)  # session の有効期限を 5 分に設定
        return redirect(url_for("mypage"))
    else:
        error='ユーザ名またはパスワードが違います。'
        input_data={'user_name':user_name, 'password':password}
        return render_template('index.html', error=error, data=input_data)
    
@app.route('/mypage', methods=['GET'])
def mypage():
    if "user" in session:
        return render_template("mypage.html")  
    else:
          return redirect(url_for("index"))
    


@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/registerbook.html')
def register_book():
    return render_template('registerbook.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    password = request.form.get('password')


    if user_name == '':
        error = 'ユーザ名が未入力です'
        return render_template('register.html', error=error)

    if password == '':
        error = 'パスワードが未入力です'
        return render_template('register.html', error=error)

    count = db.insert_user(user_name, password)

    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index', msg=msg))  
    
    else:
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)


@app.route('/list')
def sample_list():
    book_list = db.select_all_books()
    return render_template('list.html', books=book_list)


@app.route('/register_book', methods=['POST'])
def register_books():
    title=request.form.get('title')
    author=request.form.get('author')
    publisher=request.form.get('publisher')
    pages=request.form.get('pages')
    if title=="":
        error="タイトル等が入力されていません"
        return render_template("registerbook.html",error=error)
    if author=="":
        error="著者等が入力されていません"
        return render_template("registerbook.html",error=error)
    if publisher=="":
        error="出版社等が入力されていません"
        return render_template("registerbook.html",error=error)
    if pages=="":
        error="ページ数が入力されていません"
        return render_template("registerbook.html",error=error)
    
    db.insert_book(title, author, publisher, pages)

    msg="登録が完了しました。"
    return render_template('registerbook.html',msg=msg)

@app.route("/logout")
def logout():
    session.pop("user", None) 
    return redirect(url_for("index"))

@app.route("/list", methods=['POST']) 
def delete():
    id = request.form.get("id")
    if id == "":
        error = "idが入力されていません"
        book_list = db.select_all_books()
        return render_template("list.html", error=error, books=book_list)

    db.deletebook(id)
    book_list = db.select_all_books()
    msg = "削除が完了しました。"
    return render_template("list.html", msg=msg, books=book_list)

@app.route("/search", methods=["POST"])
def search():
    title = request.form.get("title")
    if title == "":
        error = "タイトルが入力されていません"
        book_list = db.select_all_books()
        return render_template("list.html", error=error, books=book_list)

    book_list = db.seach_book(title)
    msg = "対象図書一覧です"
    return render_template("list.html", msg=msg, books=book_list)
    
    
if __name__ == "__main__":
    app.run(debug=True)