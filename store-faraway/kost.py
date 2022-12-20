from flask import Flask, request, render_template, flash, url_for, redirect
from db_util import Database
from UserLogin import UserLogin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "1932"

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Брат, зайди, чтобы тут лазить"
login_manager.login_message_category = "success"

db = Database()
user = False


# декоратор, который будет создавать экземпляр класса UserLogin, при каждом запросе
@login_manager.user_loader
def load_user(user_id):
    print('load user')
    return UserLogin().fromDB(user_id, db)


#
# @app.teardown_appcontext
# def close_db(error):
#     db.commit()
#     db.close()


@app.route('/')
def homepage():
    products = db.get_products()
    return render_template('home.html', products=products)


@app.route('/about')
@login_required
def about():
    return render_template('about.html')


@app.route('/wishlist')
def wishlist():
    if db.person_whishlist(user[0])[0]:
        products_fav = db.person_whishlist(user[0])[0]
        products=[]
        for products_id in products_fav:
            products.append(db.get_product(products_id))
        return render_template('wishlist.html', products=products)
    else:
        render_template('wishlist.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        global user
        user = db.get_user(request.form['login'])
        if user and check_password_hash(user[2], request.form['password']):  # 2 потому что там пароль
            user_login = UserLogin().create(user)
            login_user(user_login)
            return redirect(url_for('wishlist'))
        flash("Неправильно ты пароль ввел, ну или логин", category='error')
    return render_template('login.html')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        login = request.form['login']
        if not db.is_exist_login(login):
            if request.form['password'] == request.form['password2']:
                hash = generate_password_hash(request.form['password'])
                res = db.add_user(request.form['login'], hash, request.form['name'], request.form['surname'])
                if res:
                    flash("Вы успешно зарегистрированы", category="success")
                    return redirect(url_for('login'))
                else:
                    flash("Ошибка добавления в БД", category="error")
            else:
                flash("Ну нормально зарегайся, что как лох", category='error')
        else:
            flash("Такой пользователь уже существует", category="error")

    return render_template('registration.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", category="success")
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    if user:
        login = user[1]
        name = user[3]
        surname = user[4]
        return render_template('profile.html', login=login, name=name, surname=surname)
    else:
        return render_template('profile.html')


@app.route("/product/<int:product_id>")
def get_product(product_id):
    product = db.get_product(product_id)

    if product:
        return render_template("product.html", title=product[2], product=product)

    return render_template("error.html", error="Такого товара не существует в системе")


@app.route('/add_product', methods=['POST', 'GET'])
@login_required
def add_product():
    if request.method == 'POST' and db.add_product(request.form['price'], request.form['name'], request.form['info'],
                                                   request.form['rating'], request.form['img']):
        flash("Все с кайфом", category="success")
    flash("Ошибка добавления в БД", category="error")
    return render_template('add_product.html')


@app.route("/products")
def products_list():
    products = db.get_products()
    # возвращаем сгенерированный шаблон с нужным нам контекстом
    return render_template("products.html", products=products)


@app.route('/add_wishlist', methods=['POST', 'GET'])
def add_wishlist():
    if request.method == 'POST':
        product = request.form['product']
        db.add_wishlist(user, product)
    return render_template("wishlist.html")

# if __name__ == "__main__":
#     app.run(debug=True)
