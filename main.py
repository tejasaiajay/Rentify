from flask import Flask,render_template,url_for,redirect,session,request
import mysql.connector
from datetime import datetime


app=Flask(__name__)
app.secret_key = '@A*Laxman!@$#12!^&77HG'

config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'presidio'
}

connection = mysql.connector.connect(**config)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register_user')
def register_user():
    return render_template("register.html")


@app.route("/user_login",methods=['GET', 'POST'])
def user_login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['pwd']
        type = request.form['type']
        if type=="None":
            return render_template("index.html",msg="Enter Correct Details")
        else:
            try:
                cursor = connection.cursor()
                if type=="1":
                    cursor.execute("SELECT * FROM users WHERE email = %s and password = %s and type = %s", (email, password, type))
                elif type=="0":
                    cursor.execute("SELECT * FROM users WHERE email = %s and password = %s and type = %s", (email, password, type))
                user = cursor.fetchone()

                if user:
                    session['email'] = email
                    if type=="1":
                        return redirect('/after_seller_login')
                    else:
                        return redirect('/after_buyer_login')
                else:
                    return render_template('index.html',msg="Your credentials are Wrong")

            except Exception as e:
                return render_template('register.html',msg=f"Something went wrong. Please try again {e}")

            finally:
                cursor.close()

@app.route("/user_register", methods=['GET', 'POST'])
def user_register():
    if request.method == "POST":
        first_name = request.form['first_name']
        second_name=request.form['second_name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        Type = request.form['type']
        if Type == "-1":
            return render_template('register.html',msg="Enter Correct Inputs")
        else:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM users WHERE email = %s and type = %s", (email,Type))
                user = cursor.fetchone()

                if user:
                    return render_template('register.html',msg="User already exists")

                else:
                    cursor.execute("INSERT INTO users (first_name,last_name,email, password, type,phone) VALUES (%s, %s, %s, %s, %s, %s)", 
                                (first_name,second_name,email, password,Type,phone))
                    connection.commit()
                    return render_template('index.html',msg="Account created successfully")

            except Exception as e:
                return render_template('register.html',msg="Something went wrong. Please try again")

            finally:
                cursor.close()

@app.route('/get_search_data',methods=["POST"])
def get_search_data():
    if 'email' in session:
        query=request.form['search_query'].lower()
        try:
            cursor=connection.cursor()
            cursor.execute("SELECT * FROM post WHERE place LIKE %s", ('%' + query + '%',))
            posts=cursor.fetchall()
            return render_template('after_buyer_login.html',posts=posts)
        except Exception as e:
            return redirect('/after_buyer_login')
    else:
        return redirect('/')


@app.route('/after_seller_login')
def after_seller_login():
    if 'email' in session:
        email=session['email']
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * from post where email=%s",(email,))
            posts=cursor.fetchall()
            return render_template('after_seller_login.html',posts=posts)
        except Exception as e:
            return render_template('index.html',msg=f'Some Thing Went Wrong! Please Login Again {e}')
    else:
        return redirect('/')

@app.route('/after_buyer_login')
def after_buyer_login():
    if 'email' in session:
        try:
            cursor=connection.cursor()
            cursor.execute("SELECT * FROM post")
            details=cursor.fetchall()
            return render_template('after_buyer_login.html',posts=details)
        except Exception as e:
            return redirect('/')
    else:
        return redirect('/')

@app.route('/get_post_details',methods=["POST"])
def get_post_details():
    if 'email' in session:
        email=request.form['id']
        try:
            cursor=connection.cursor()
            cursor.execute("SELECT * FROM users where email=%s",(email,))
            data=cursor.fetchone()
            return render_template('show_seller.html',data=data)
        except Exception as e:
            return redirect('/')
    else:
        return redirect('/')


@app.route('/insert_post')
def insert_post():
    if 'email' in session:
        return render_template('insert_post.html')
    else:
        return redirect('/')

@app.route('/add_post',methods=['POST'])
def add_post():
    if 'email' in session:
        if request.method=='POST':
            email=session['email']
            place=request.form['place'].lower()
            area=request.form['area'].lower()
            rooms=request.form['rooms']
            baths=request.form['baths']
            hospitals=request.form['hospitals']
            colleges=request.form['colleges']
            schools=request.form['schools']
            try:
                cursor=connection.cursor()
                cursor.execute("insert into post(email,place,area,num_of_bed_rooms,bath_rooms,hospitals,colleges,schools) values(%s,%s,%s,%s,%s,%s,%s,%s)",(email,place,area,rooms,baths,hospitals,colleges,schools))
                connection.commit()
                return redirect('after_seller_login')
            except Exception as e:
                return redirect('after_seller_login')
        else:
            return render_template('after_seller_login.html')
    else:
        return redirect('/')

@app.route('/delete_post',methods=['POST'])
def delete_post():
    if request.method=='POST':
        if 'email' in session:
            id=request.form['id']
            try:
                cursor=connection.cursor()
                cursor.execute('DELETE FROM post WHERE id= %s',(id,))
                connection.commit()
                return redirect('/after_seller_login')
            except Exception as e:
                return redirect('/')
        else:
            return redirect('/')

@app.route('/update_post',methods=['POST'])
def update_post():
    if 'email' in session:
        id=request.form['id']
        place=request.form['place']
        area=request.form['area']
        rooms=request.form['num_of_bed_rooms']
        baths=request.form['bath_rooms']
        hospitals=request.form['hospitals']
        colleges=request.form['colleges']
        schools=request.form['schools']
        return render_template('edit.html',details=[id,place,area,rooms,baths,hospitals,colleges,schools])
    else:
        return redirect('/')

@app.route('/update_details',methods=["POST"])
def update_details():
    if request.method=='POST':
        if 'email' in session:
            id=request.form['id']
            place=request.form['place'].lower()
            area=request.form['area'].lower()
            rooms=request.form['rooms']
            baths=request.form['baths']
            hospitals=request.form['hospitals']
            colleges=request.form['colleges']
            schools=request.form['schools']
            try:
                cursor=connection.cursor()
                cursor.execute("UPDATE post set place= %s,area=%s,num_of_bed_rooms=%s,bath_rooms=%s,hospitals=%s,colleges=%s,schools=%s where id=%s",(place,area,rooms,baths,hospitals,colleges,schools,id))
                connection.commit()
                return redirect('/after_seller_login')
            except Exception as e:
                return redirect('/after_seller_login')
        else:
            return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    

if __name__=='__main__':
    app.run(debug=True)