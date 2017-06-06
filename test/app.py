from flask import Flask, flash, render_template, url_for
from flask import request
from flaskext.mysql import MySQL
import pandas as pd
from wtforms import Form, TextField, BooleanField, StringField, PasswordField, validators

#Connect to the mysql database
app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'cartrawler-admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cartrawler'
app.config['MYSQL_DATABASE_DB'] = 'cartrawler'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def index():
    return render_template("main_page.html")

@app.route('/getdetails', methods=['POST'])
def get_details():
    conn = mysql.connect().cursor()
    print(request.form["queryid"])
    queryid = ''
    queryid = request.form["queryid"]
    query = "SELECT `Queryid`,`Carid`,`Price`,`Bags`, `Passengers`,`Segment` FROM `seg_car` WHERE `Queryid` = %s" %(queryid)

    x = conn.execute(query)
    if x == 0:
        return 'Please enter a valid QueryId'
    else:
        data = conn.fetchall()

    df = pd.DataFrame(list(data), columns=['Queryid', 'Carid','Price','Bags', 'Passengers','Segment'])
    seg = df.ix[0, 'Segment']

    if seg == 'Family':
        df.sort_values('Passengers', ascending=False, inplace=True)
        dfy = df.head(10)
    elif lv_seg == 'Business':
        df.sort_values('Passengers', ascending=True, inplace= True)
        dfy = df.head(10)
    else:
        df.sample(frac=1)
        dfy = df.head(10)

    df_tuples = [tuple(x) for x in dfy.to_records(index=False)]

    return render_template("next_page.html",
                           title="Segments",
                           info=df_tuples,
                           juhi=seg)

if __name__ == '__main__':
    app.secret_key = 'supere secret'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)