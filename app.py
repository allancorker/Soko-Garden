from flask import *
import pymysql
import sms

app=Flask(__name__)

connection= pymysql.connect(host='localhost',user='root',password='', database='kindi1_soko_garden') #creating a connection to our database using function connect
sql='SELECt * FROM products WHERE product_category"Smartphones"'
sql2='SELECt * FROM products WHERE product_category"Clothes"'

cursor=connection.cursor()
cursor1=connection.cursor()
cursor2=connection.cursor()

app.secret_key="sokosecretkey" #we are setting secret key to secure our session or make it unique

@app.route('/')
def home():
    connection= pymysql.connect(host='localhost',user='root',password='', database='kindi1_soko_garden') #creating a connection to our database using function connect
    sql='SELECT * FROM products WHERE product_category="Smartphones"'
    cursor=connection.cursor()
    cursor.execute(sql)
    data=cursor.fetchall() #fetchall() is used to fetch the remainig rows from the results set of a query fetchmany(size=20) is used to fetch a specified number of rows from the result set of a query. fetchone() is used to fetch a single row 

    #fetching category electronics
    sql1='SELECt * FROM products WHERE product_category="Electronics"'
    cursor.execute(sql1)
    data1=cursor.fetchall()

    #fetching category clothes
    sql2='SELECt * FROM products WHERE product_category="Clothes"'
    cursor.execute(sql2)
    data2=cursor.fetchall()

    #fetching category utensils
    sql3='SELECt * FROM products WHERE product_category="Utensils"'
    cursor.execute(sql3)
    data3=cursor.fetchall()

    #fetching category other
    sql4='SELECt * FROM products WHERE product_category="Other"'
    cursor.execute(sql4)
    data4=cursor.fetchall()

    return render_template('index.html', category_smartphones=data,category_Electronics=data1,category_Clothes=data2,category_Utensils=data3,category_Other=data4)

@app.route('/upload', methods=['POST','GET']) #Routing upload.html
def upload():
    #This is where data is uploaded
    if request.method == 'POST':
        # below data receives all variables sent or submitted from form
        product_name=request.form['product_name']
        product_desc=request.form['product_desc']
        product_cost=request.form['product_cost']
        product_category=request.form['product_category']
        product_image_name=request.files['product_image_name']
        product_image_name.save('static/images/'+ product_image_name.filename) # saves the image file in images folder, in static folder
        
        # connecting to the database
        connection= pymysql.connect(host='localhost',user='root',password='', database='kindi1_soko_garden')
        cursor=connection.cursor() #cursor() allows code to execute sql command in a database session

        data3 = (product_name,product_desc,product_cost,product_category,product_image_name.filename)

        sql="INSERT INTO products (`product_name`,`product_desc`,`product_cost`,`product_category`,`product_image_name`)VALUES(%s,%s,%s,%s,%s)" #%s is used as a placeholder for the variables in the data variable
        cursor.execute(sql,data3) #the execute() is used to execute the query in the variable sql
        connection.commit() #commit() is used to write changes to database

        return render_template('upload.html', message='Product Added Successfully')
    else:
        return render_template('/upload.html',message='Give Your details below:')
    
@app.route('/merchant', methods=['POST','GET'])
def merchant():
    if request.method == 'POST':
        firstname=request.form['firstname']
        secondname=request.form['secondname']
        lastname=request.form['lastname']
        national_ID=request.form['national_ID']
        county=request.form['county']

        connection= pymysql.connect(host='localhost',user='root',password='', database='kindi1_soko_garden')
        cursor=connection.cursor()

        data = (firstname,secondname,lastname,national_ID,county)

        sql="INSERT INTO `merchant`(`firstname`, `secondname`, `lastname`, `national_ID`, `county`) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql,data)
        connection.commit()

        return render_template('merchant.html', feedback='Merchant Added')
    else:
        return render_template('/merchant.html', feedback='Create Merchant Account')
    
@app.route('/single_item/<product_id>', methods=['POST','GET'])
def single_item(product_id):
    sql='SELECT * FROM products WHERE product_id=%s'
    cursor.execute(sql,product_id)
    product= cursor.fetchone()

    return render_template('single_item.html',product=product )

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username=request.form['username']
        email=request.form['email']
        phone=request.form['phone']
        password1=request.form['password1']
        password2=request.form['password2']

        # we need to validate our passwords
        if len(password1) < 8:
            return render_template('signup.html',error='PASSWORD MUST BE ATLEAST 8 CHARACTERS')
        elif password1 != password2:
            return render_template('signup.html', error1='PASSWORD DOES NOT MATCH')
        else:
            my_query='''INSERT INTO users (`username`, `password`, `email`, `phone`) VALUES (%s,%s,%s,%s)'''
            cursor.execute(my_query,(username,password1,email,phone))
            connection.commit()

            sms.send_sms(phone, "Thank You for Registering, Registeration successful. Congratulations for registering. You are eligible for scholarhip at AfricaStalking. Kindly feel free to check about our site")
            return render_template('signup.html', success='SIGNED UP SUCCESSFULLY') #check youtube how to send email instead of sms
    else:
        return render_template('signup.html')
    
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username=request.form['username']
        password1=request.form['password1']

        sql="SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(sql,(username,password1)) 
        connection.commit()

        if cursor.rowcount == 0:
            return render_template('login.html', error="INVALID CREDENTIALS. You may have entered the wrong Password or Username")
        else:
            session['key']=username #we need to create a session for all users so as to make their page unique/private. we are linking the session key with username
            return redirect('/')
    else:
        return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.clear() #we are ending the session
    return redirect('/login')

@app.route('/mpesa', methods=['POST','GET'])
def mpesa():
    phone = request.form['phone']
    amount=request.form['amount']

    import mpesa 
    mpesa.stk_push(phone,amount)
    return '<h3>Please Complete Payment in your mobile and we will deliver in a minute</h3>'\
    '<a href='"/"' class="btn btn-dark btn-sm">Back Home</a>'

if __name__=='__main__':
    app.run(debug=True)