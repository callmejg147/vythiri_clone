from flask import Flask, flash, render_template, request
import hashlib
import sqlite3


from twilio.rest import Client
import os




# flask settings
HOSTNAME = "localhost"
PORT = "8080"
dom = "http://"+HOSTNAME+":"+PORT
app=Flask(__name__)
app.debug = True

# secret key
app.secret_key = "vythiri clone"
app.config['SESSION_TYPE'] = 'filesystem'
# setting routes
@app.route("/",)
def home():
    return render_template("index.html", dom = dom)

@app.route("/dwell/celestial-honeymoon")
def celestial():
    return render_template("celestialhoneymoon.html", dom = dom )

@app.route("/dwell/family-pool-villa")
def poolvilla():
    return render_template("poolvilla.html", dom = dom )

@app.route("/dwell/honeymoon-villa")
def honeymoon():
    return render_template("honeymoon.html", dom = dom )

@app.route("/dwell/tree-house")
def treehouse():
    return render_template("treehouse.html", dom = dom )

@app.route("/dwell/premium-haven")
def premiumhaven():
    return render_template("premium.html", dom = dom )

@app.route("/dwell/vythiri-haven")
def vythirihaven():
    return render_template("vythirihaven.html", dom = dom )

@app.route("/vexperiences")
def experiences():
    return render_template("Vexperiences.html", dom = dom )

@app.route("/rainforest")
def rainforest():
    return render_template("rainforest.html", dom = dom)

@app.route("/activities")
def activities():
    return render_template("activities.html", dom = dom)

@app.route("/gallery")
def gallery():
    return render_template("gallery.html", dom = dom)

@app.route("/tariff")
def tariff():
    return render_template("tariff.html", dom = dom)

@app.route("/dwell")
def dwell():
    return render_template("dwell.html", dom = dom)

@app.route("/facilities")
def facilities():
    return render_template("facilities.html", dom = dom)

@app.route("/rejuvenate")
def rejuvenate():
    return render_template("rejuvenate.html", dom = dom)

@app.route("/reservation")
def reservation():
    return render_template("reservation.html", dom = dom)

@app.route("/contactus")
def contactus():
    return render_template("contactus.html", dom = dom)

@app.route("/packages")
def packages():
    return render_template("packages.html", dom = dom)

@app.route("/specialoffers")
def specialoffers():
    return render_template("specialoffers.html", dom = dom)

@app.route("/guestspeaks")
def guestspeaks():
    return render_template("guestspeaks.html", dom = dom)

@app.route("/awards")
def awards():
    return render_template("awards.html", dom = dom)

@app.route("/howtogetthere")
def howtogetthere():
    return render_template("howtogetthere.html", dom = dom)

@app.route("/termsandconditions")
def tandc():
    return render_template("tandc.html", dom = dom)

@app.route("/privacypolicy")
def privacypolicy():
    return render_template("privacypolicy.html", dom = dom)

@app.route("/sitemap")
def sitemap():
    return render_template("sitemap.html", dom = dom)

@app.route("/gallery/photo-gallery")
def photogallery():
    return render_template("photo-gallery.html", dom = dom)

@app.route("/gallery/video-gallery")
def videogallery():
    return render_template("video-gallery.html", dom = dom)

@app.route("/gallery/high-resolution-images")
def hires():
    return render_template("hires.html", dom = dom)

@app.route("/gallery/photo-gallery")
def views():
    return render_template("360views.html", dom = dom)

@app.route("/reservation-request", methods = ["GET","POST"])
def resreq():
    #conn = sqlite3.connect('reservation.db')
    #cur = conn.cursor()
    firstname = request.form.get('fname')
    lastname = request.form.get('lname')
    address = request.form.get('addrs')
    country = request.form.get('country')
    state = request.form.get('state')
    city = request.form.get('city')
    zipcode = request.form.get('zcode')
    phnum = request.form.get('mobile')
    email = request.form.get('email')
    norooms = request.form.get('rnum')
    roomtype = request.form.get('rtype')
    noadult = request.form.get('adults')
    arr = request.form.get('adate')
    dep = request.form.get('ddate')
    nochildren = request.form.get('children')

    if request.method == "POST":

        conn = sqlite3.connect('reservation.db')
        cur = conn.cursor()
        sql = ("INSERT INTO res_request (fname,lname,addrs,country,state,city,zcode,pnum,email,rtype,rnum,arrival,departure,nadults,nchildren) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")

        cur.execute(sql, (firstname,lastname,address,country,state,city,zipcode,phnum,email,roomtype,norooms,arr,dep,noadult,nochildren))

        sql2 = ("SELECT pwd FROM imp_pass WHERE usr LIKE 'sendmail'")
        cur.execute(sql2)
        pwd = cur.fetchone()[0]

        # sending an email to the customer
        os.system(f"python3 send_email.py {email} {pwd}")

        # send sms via sms.py
        os.system(f"python3 sms.py {phnum}")
        conn.commit()
        conn.close()

        return render_template('reservation-req.html')


@app.route('/admin')
def login():
    return render_template('admin-page.html')

@app.route('/admin-view', methods = ["GET", "POST"])
def admin():
    user = request.form.get('user')
    pas = request.form.get('pass')
    pasword = hashlib.md5(pas.encode('utf-8')).hexdigest()

    if request.method == "POST":
        conn = sqlite3.connect('reservation.db')
        cur = conn.cursor()
        sql = ("SELECT pass FROM admins WHERE usr LIKE "+"'"+user+"'")
        cur.execute(sql)
        usrpass = cur.fetchone()[0]

        if pasword == usrpass:
            return render_template('admin-home.html', user=user)
        else:
            return "<h1 style='color:red; text-align:center;'>Unauthorised Login Attempt</h1>"
    else:
        return " wrong request method </h1>"

@app.route('/admin/reservation-requests', methods=["GET","POST"])
def viewres():
    conn =sqlite3.connect('reservation.db')
    cur = conn.cursor()
    sql = ("SELECT * FROM res_request")
    cur.execute(sql)


    data = cur.fetchall()
    pending = len(data)

    conn.close()
    if len(data)<1:
        return render_template('no-reservation.html')
    else:
        if request.method == "POST":
            for row in data:
                action = request.form.get('action')
                if action == 'accept':
                    conn = sqlite3.connect('reservation.db')
                    cur = conn.cursor()
                    q1 = ("INSERT INTO accepted_res (name, pnum, addr, rnum, email, rtype, adults, children, adate, ddate) VALUES (?,?,?,?,?,?,?,?,?,?)")
                    cur.execute(q1,(row[0],row[7],row[2],row[10],row[8],row[9],row[13],row[14],row[11],row[12]))
                    q2 = (f"DELETE FROM res_request WHERE email LIKE '{row[8]}'")
                    cur.execute(q2)
                    conn.commit()
                    sql = ("SELECT * FROM res_request")
                    cur.execute(sql)
                    data = cur.fetchall()
                    conn.close()
                    return render_template('admin-reservation-requests.html', data=data, pending=pending)
                elif action == 'reject':
                    conn = sqlite3.connect('reservation.db')
                    cur = conn.cursor()
                    q1 = ("INSERT INTO rejected_res (name, pnum, email) VALUES (?,?,?)")
                    cur.execute(q1, (row[0],row[7],row[8]))
                    q2 = (f"DELETE FROM res_request WHERE email LIKE '{row[8]}'")
                    cur.execute(q2)
                    conn.commit()
                    sql = ("SELECT * FROM res_request")
                    cur.execute(sql)
                    data = cur.fetchall()
                    conn.close()
                    return render_template('admin-reservation-requests.html', data=data, pending=pending)
        return render_template('admin-reservation-requests.html', data=data, pending=pending)

@app.route('/admin/view-accepted', methods=["GET"])
def viewaccepted():
    conn =sqlite3.connect('reservation.db')
    cur = conn.cursor()
    sql = ("SELECT * FROM accepted_res")
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()
    return render_template('accepted.html', data=data)

@app.route('/admin/view-rejected', methods=["GET"])
def viewrejected():
    conn =sqlite3.connect('reservation.db')
    cur = conn.cursor()
    sql = ("SELECT * FROM rejected_res")
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()
    return render_template('rejected.html', data=data)
if __name__ == "__main__" :
    app.run(HOSTNAME, PORT)

