from flask import Flask,render_template,request,redirect,session,flash
import mysql.connector
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


app=Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="localhost",user="root",password="",database="sandeep")
cursor=conn.cursor()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def about():
    return render_template('register.html')



@app.route('/index')
def home():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return redirect('/')

@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin_home')
def admin_home():
    cursor.execute('SELECT user_id, name, email FROM users')
    data = cursor.fetchall()
    if 'admin_id' in session:
        return render_template('admin_home.html', output_data=data)
    else:
        return redirect('/admin_login')


@app.route('/abt')
def abt():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Read the housing data from CSV file
    df = pd.read_csv('house[1].csv')
    df.set_index('Id', inplace=True)

    # Data preprocessing
    df.dropna(inplace=True)
    df['MasVnrArea'] = pd.to_numeric(df['MasVnrArea'], errors='coerce')
    df['MasVnrArea'] = df['MasVnrArea'].astype('int64')

    # Independent variable declaration
    X_var = df[['LotArea', 'MasVnrArea', 'BsmtUnfSF', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF', 'GrLivArea', 'GarageArea',
                'WoodDeckSF', 'OpenPorchSF']].values
    # Dependent(Target) variable declaration
    y_var = df['SalePrice'].values

    # Splitting the data into train(80) and test(20) sets
    X_train, X_test, y_train, y_test = train_test_split(X_var, y_var, test_size=0.2, random_state=0)

    # Create an instance of the LinearRegression model
    model = LinearRegression()
    # Train the model on training data
    model.fit(X_train, y_train)

    # Extract the input values from the form
    features = [float(x) for x in request.form.values()]

    # Perform prediction using the model
    prediction = model.predict([features])[0]

    # Round the prediction to two decimal places
    prediction = round(prediction, 2)

    # Render the result template and pass the prediction value
    return render_template("result.html", prediction=prediction)



@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')


    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'"""
                   .format(email,password))
    users=cursor.fetchall()

    error = 'Invalid username or password. Please try again!'


    if len(users)>0:
        session['user_id']=users[0][0]


        flash('You were successfully logged in')
        return redirect("/index")
    else:
        return render_template('login.html', error = error)

@app.route('/admin_validation', methods=['POST'])
def admin_validation():
    username=request.form.get('username')
    password=request.form.get('password')


    cursor.execute("""SELECT * FROM `admin` WHERE `username` LIKE '{}' AND `password` LIKE '{}'"""
                   .format(username,password))
    admin=cursor.fetchall()

    error = 'Invalid username or password. Please try again!'


    if len(admin)>0:
        session['admin_id']=admin[0][0]


        flash('You were successfully logged in')
        return redirect("/admin_home")
    else:
        return render_template('admin_login.html', error = error)


@app.route('/add_user', methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')


    cursor.execute("""INSERT INTO `users` (`user_id`,`name`,`email`,`password`) VALUES
    (NULL, '{}','{}','{}')""".format(name,email,password))
    conn.commit()
    msg = "Sucessfully Registered  Please Log In"
    return render_template('register.html', error=msg)


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')





if __name__=="__main__":
    app.run(debug=True)