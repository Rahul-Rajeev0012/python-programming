from flask import Flask,render_template,request, session, redirect, url_for, g
import mysql.connector


connection=mysql.connector.connect(
    host='localhost',
    user='root',
    password='Rahul@123',
    database='OnlineRecipe')

mycursor = connection.cursor(dictionary=True)

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def home():
    search_query = request.args.get('search')
    category = request.args.get('category')
    recipe = []
    query=f'select * from recipies WHERE 1=1'
    option=[]
    if search_query:
        query+=' AND r_name LIKE %s'
        option.append ("%" + search_query + "%")
    else:
        search_query = ''
    if category:
        query += ' AND category = %s'
        option.append(category)
    mycursor.execute(query, option)
    recipe = mycursor.fetchall()

    # Fetch comments for each recipe
    for r in recipe:
        recipie_id = r['r_id']
        comment_query = 'SELECT comments.comment, comments.date_posted, users.username FROM comments JOIN users ON comments.user_id = users.id WHERE recipie_id = %s'
        mycursor.execute(comment_query, (recipie_id,))
        comments = mycursor.fetchall()
        r['comments'] = comments

    return render_template('home.html', search_query=search_query, recipe=recipe, category=category)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loggedin', methods=['POST'])
def loggedin():
    user = request.form.get("user")
    pwd = request.form.get("pass")

    if not user:
        return render_template('login.html', msg="INVALID USERNAME")

    # Check if the user exists
    query = 'SELECT id, password FROM users WHERE username = %s LIMIT 1'
    mycursor.execute(query, (user,))
    user_record = mycursor.fetchone()

    if user_record:
        stored_password = user_record['password']

        if pwd and pwd == stored_password:
            session['user'] = user
            session['user_record'] = user_record
            return render_template('loggedin.html')
        else:
            return render_template('login.html', msg="INVALID PASSWORD")
    else:
        return render_template('login.html', msg="INVALID USERNAME")
    
@app.route('/loggedinsearch') 
def loggedinsearch():
    search_query = request.args.get('search')
    category = request.args.get('category')
    recipe = []
    query=f'select * from recipies WHERE 1=1'
    option=[]
    if search_query:
        query+=' AND r_name LIKE %s'
        option.append ("%" + search_query + "%")
    else:
        search_query = ''
    if category:
        query += ' AND category = %s'
        option.append(category)
    mycursor.execute(query, option)
    recipe = mycursor.fetchall()

    # Fetch comments for each recipe
    for r in recipe:
        recipie_id = r['r_id']
        comment_query = 'SELECT comments.comment, comments.date_posted, users.username FROM comments JOIN users ON comments.user_id = users.id WHERE recipie_id = %s'
        mycursor.execute(comment_query, (recipie_id,))
        comments = mycursor.fetchall()
        r['comments'] = comments


    return render_template('loggedin.html', search_query=search_query, recipe=recipe, category=category)
    

@app.route('/register',methods=['GET','POST'])
def add_emp():
    if request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        query = "insert into users(username,email,password) values (%s,%s,%s)"
        data = (username,email,password)
        mycursor.execute(query,data)
        connection.commit()
        return render_template('login.html')
    return render_template('register.html')

@app.route('/addrecipe',methods=['GET','POST'])
def addrecipe():
    if request.method=='POST':
        user = session['user']
        query = f'SELECT id FROM users WHERE username LIKE "{user}"'
        mycursor.execute(query)
        userrecord = mycursor.fetchone()
        if userrecord:
            userid = userrecord['id']
        rname = request.form['rname']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        cooktime = request.form['cooktime']
        ssize = request.form['ssize']
        category = request.form['category']
        query1 = "INSERT INTO recipies (r_name, ingredients, instructions, cook_time, serve_size, user_id, category) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        data = (rname, ingredients, instructions, cooktime, userid, ssize, category)
        mycursor.execute(query1, data)
        msg='recipe added succesfully'
        connection.commit()
        return render_template('loggedin.html', msg=msg)
    return render_template('addrecipe.html')

@app.route('/view')
def view():
    user_record = session.get('user_record')
    user_id = user_record['id']
    query="select *  from recipies;"
    mycursor.execute(query)
    data = mycursor.fetchall()
    return render_template('viewrecipe.html',sqldata=data)

@app.route('/delete',methods=['GET','POST'])
def delete():
    user_record = session.get('user_record')
    user_id = user_record['id']
    if request.method == 'POST':
       id = request.form['id']
       query = "delete from recipies where r_id=%s"
       data=(id,)
       mycursor.execute(query,data)
       connection.commit()
       message = f"Recipie with id {id} deleted successfully"
       query="select * from recipies where user_id =%s"
       mycursor.execute(query,(user_id,))
       data = mycursor.fetchall()
       return render_template('delete.html',sqldata=data,msg=message)
    else:
        query="select * from recipies"
        mycursor.execute(query)
        data = mycursor.fetchall()
        return render_template('delete.html',sqldata=data)
    
@app.route('/update',methods=['GET','POST'])
def update():
    user_record = session.get('user_record')
    user_id = user_record['id']
    if request.method == 'POST':
      id = request.form['id']
      name = request.form['r_name']
      ingredients = request.form['ingredients']
      instructions = request.form['instructions']
      cooktime = request.form['cook_time']
      serve_size = request.form['serve_size']
      category = request.form['category']

      query = """
        UPDATE recipies
        SET r_name = %s, ingredients = %s, instructions = %s,
            cook_time = %s, serve_size = %s, category = %s
        WHERE r_id = %s
      """
      data = (name, ingredients, instructions, cooktime, serve_size, category, id)
      mycursor.execute(query, data)
      connection.commit()
      message = "Recipe Updated Successfully"
      query="select * from recipies"
      mycursor.execute(query)
      data = mycursor.fetchall()

      return render_template('update.html', msg=message, sqldata=data)  # Avoid exposing updated data
    else: 
        query="select * from recipies"
        mycursor.execute(query)
        data = mycursor.fetchall()
        return render_template('update.html', sqldata=data)  
  
@app.route('/viewprofile',methods=['GET','POST'])
def viewprofile():
    user_record = session.get('user_record')
    user_id = user_record['id']

    if request.method == 'POST':
        id = request.form['id']
        name = request.form['username']
        email = request.form['email']

        query = """
        UPDATE users
        SET username = %s, email = %s
        WHERE id = %s
      """
        data = (name, email, id)
        mycursor.execute(query, data)
        connection.commit()
        message = " Updated Successfully"
        query = "SELECT id,username,email FROM users where id = %s"
        mycursor.execute(query,(user_id,))
        data = mycursor.fetchall()

        return render_template('profile.html', msg=message, sqldata=data)  # Avoid exposing updated data
    else: 
        query = "SELECT id,username,email FROM users where id = %s"
        mycursor.execute(query,(user_id,))
        data = mycursor.fetchall()
        return render_template('profile.html', sqldata=data)

@app.route('/deleteprofile',methods=['GET','POST'])
def deleteprofile():
    user_record = session.get('user_record')

    if not user_record:
        return redirect(url_for('login'))  # Redirect to login if user is not logged in

    user_id = user_record['id']

    query = "DELETE FROM users WHERE id = %s"
    mycursor.execute(query, (user_id,))
    connection.commit()
    session.pop('user_record', None)  # Remove user data from session
    message = "Profile deleted successfully"

    return redirect(url_for('login', msg=message))

@app.route('/comment',methods=['GET', 'POST'])
def comment():
    user_record = session.get('user_record')
    user_id = user_record['id']
    query="select * from comments"
    mycursor.execute(query)
    data = mycursor.fetchall()
    return render_template('comments.html',sqldata=data)

@app.route('/addcomments',methods=['GET', 'POST'])
def addcomments():
    user_record = session.get('user_record')
    user_id = user_record['id']
    if request.method=='POST':
        recipie_id = request.form['recipie_id']
        comment = request.form['comment']
        query = "insert into comments(recipie_id,user_id,comment) values (%s,%s,%s)"
        data = (recipie_id,user_id,comment)
        mycursor.execute(query,data)
        connection.commit()
        return render_template('comments.html',sqldata=data)
    return 0
   
@app.route('/logout',methods=['GET', 'POST'])
def logout():
    # Clear the user session
    session.pop('user', None)
    return redirect(url_for('home'))

#run flask application
if __name__ == '__main__':
    app.run(debug = True)

