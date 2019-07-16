#------------------------Generate PDF for every transaction --------------------------------------
def gen_pdf(inf,to):
    pdf             = StringIO()
    pisa.createPDF(StringIO(inf),pdf)
    return pdf

#-------------------- Transaction Details Template ---------------------------------------------
template            = """ 
Account Key\t	Description\n\n
Account Name\t	{uname}\n\n
Account Number\t{acn}\n\n
Account Holder\t{name}\n\n
Country	\t{contry}\n\n
Current Balance\t{bala}\n\n
Create Date	\t{tim}\n\n
Phone Number\t	{num}\n\n
"""


#----------------------------------Home Page-----------------------------------------------------
@app.route("/")
def home():
  return render_template("home.html")

#--------------------------------- Open Account --------------------------------------------------
@app.route("/create-account", methods=["GET","POST"])
def create_account():
  if request.method == "GET":
    return render_template("create.html")
  fnam            = request.form['fname']
  lnam            = request.form['lname']
  pn              = request.form['pnumber']
  em              = request.form['email']
  cont            = request.form['country']
  currency        = request.form['cur']
  pin             = request.form['pin']
   
  #-------------------------------- Phone number must be decimals ----------------------------------
  if not pn.isdecimal():
       return jsonify(error = "The phone number must be digits")
    
  #------------------------------- Check if the email is not already registered-----------------------
  try:
       user        = load_user(em)
       if user: return jsonify(error="User %s Already exists, please try again with different details..."%user.email)
  #--------------------------- I fit gives error, then the emaail is new, just do proceed ------------
  except Exception as e:
        pass

 # if pn[0] != '+' or p[0] != '0':
 #     return render_template('success.html',pn_er=True)

 try:

        user    = User(fname=fnam,lname=lnam,pnumber=int(pn),country=cont,cur=currency,email=em,pin=pin)
        db.session.add(user)
        db.session.commit()

        user        = load_user(em)
        #----------------- Login the user, so that we can get his details anywhere ---------------------
        login_user(user)
        return redirect(url_for('generate_account'))
 except Exception as e:
        error        = "An Error Occured while Registering, please try again..."
        return jsonify(error = error)
    
#--------------------------------- Generate Account Details ---------------------------------------------
@app.route("/geneate_account")
def generate_account():
    if current_user.is_authenticated:
        #------------------------create a bank account----------------------------------------------------
            user_id         = current_user.id
            accn            = current_user.fname+" "+current_user.lname
            #---------------------  Account number for specific user -------------------------------------
            accnum          = 1000000000+user_id
            odate           = datetime.now()
            #--------------  Every Account opened is given a start bonus of 50.00 of h/er currency -------
            bl              = 50.00
            acc             = Account(accNumber=accnum,accName=accn,balance=bl,openDate=odate,accHolder=current_user)
            db.session.add(acc)

            try:
                db.session.commit()
            except Exception as e:
                return jsonify(err="Account creating failed, please try again...%s"%e)
            
            opentransaction       = template.format(uname=accn,acn=accnum,contry =current_user.country,bala= bl,tim=datetime.now(),num=pn)
            #------------------------------Generate Transaction ---------------------------------------
            gen_pdf(opentransaction,user_id)
            
            #----------------------------- Show the account details to the user -----------------------
            account         = Account.query.filter_by(accNumber=accnum).first()
            return render_template('success.html',account=account)
  

#---------------------------------- Deposit some money ------------------------------------------------------
@app.route("/deposit", methods = ["GET","POST"])
def deposit():
    if request.method=='GET':
        return render_template('deposits.html')
    dName           = request.form['dName']
    dpNum           = request.form['dNum']
    dEmail          = request.form['dEmail']
    dAddr           = request.form['dAddr']
    acName          = request.form['accName']
    acNum           = int(request.form['accNum'])
    signature       = request.form['dsignature']
    amo             = float(request.form['amount'])
    dat             = datetime.now()
    #-------------- Necessary 'Variables grabbed'--------------------------------------------------------------
    try:
        deposit          = Deposit(dname=dName,dpnumber=dpNum,demail=dEmail,daddr=dAddr,accName=acName,accNum=acNum,ammount=amo,ddate=dat,dsignature=signature)
    except Exception as e:
        return 'Operation failed, please try again...'
    db.session.add(deposit)
    db.session.commit()
    #-----------------------------------Now do the actual deposit------------------------------------------------
    try:
        #return 'Testing account...'
        ac               = Account.query.filter_by(accNumber=acNum).first()
        try:
            ac.balance += amo
            db.session.commit()
        except Exception as e:
            return render_template('success.html',d_error=True)

            #return 'deposited successfully...'
        deposit =Deposit.query.filter_by(dpnumber=dpNum).first()
        return render_template('success.html',deposit=deposit)
    except Exception as e:
        return jsonify(error = "Deposit failed... %s"%e)

#---------------------------------- Withdraw, go for some fun------------------------------------------
