from flask import Flask,render_template,redirect,request
from mysqlconnection import connectToMySQL

# from mysqlconnection import connectToMySQL

app = Flask(__name__)


@app.route('/')
def index():
    mysql= connectToMySQL('users_db')
    users = mysql.query_db ('SELECT * FROM users;')
    print(users)
    return render_template("index.html", all_users=users)


@app.route('/create', methods=['POST'])
def add_users_to_db():
    query = "INSERT INTO users ( first_name , last_name , email, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s, %(email)s,NOW(),NOW());"
    data = {
    'first_name': request.form['first_name'],
    'last_name': request.form['last_name'],
    'email': request.form['email']
    }
    bd = connectToMySQL('users_db')
    user_id= bd.query_db(query,data)
    print(user_id)
    return redirect(f'/user/{user_id}')



@app.route('/create_page')
def creat_page():
    return render_template('create.html')

    
@app.route('/user/<user_id>')
def user_page(user_id):
    mysql= connectToMySQL('users_db')
    data={
        'id': user_id
    }
    user = mysql.query_db ('SELECT * FROM users WHERE id= %(id)s;',data)
    return render_template('userinfo.html',one_user=user[0])


@app.route('/edit_page/<user_id>')
def edit_page(user_id):
    query = "SELECT * FROM users WHERE id= %(id)s;"
    data={
        'id': user_id
    }
    users= connectToMySQL('users_db').query_db(query,data)
    return render_template("edit.html",user=users[0])



@app.route('/delete/<user_id>')
def delete(user_id):
    query = "DELETE FROM users WHERE id = %(id)s;"
    data={
        'id': user_id
    }
    users= connectToMySQL('users_db').query_db(query,data)
    print(users)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)