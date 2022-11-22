#Login/Sign_up pages

from flask import Blueprint,render_template,request

class GuestApplication:
    name = ""
    credit_card = ""
    address = ""
    email = ""
    password = ""
    phone_num = ""
    
    def __init__(self,name,credit_card,address,phone,email,password) -> None:
        self.name = name
        self.credit_card = credit_card
        self.address = address
        self.email = email
        self.phone_num = phone
        self.password = password

verify_page = Blueprint('verify_page',__name__)

@verify_page.route('/login',methods=['POST','GET'])
def login():
    return render_template("login.html")

@verify_page.route('/sign-up',methods=['POST','GET'])
def sign_up():
    if request.method=="POST":
        username = request.form['name']
        email = request.form['email']
        VerifiedEmail = request.form['email_ver']
        Password = request.form['password']
        VerifiedPassword = request.form['password_ver']
        phoneNum = request.form['phone']
        address = request.form['address']
        creditCard = request.form['Credit_card']
        if email != VerifiedEmail:
            print("Wrong email!")
        if Password != VerifiedPassword:
            print("Password wrong!")
        
        newGuestApp = GuestApplication(username,creditCard,address,phoneNum,VerifiedEmail,VerifiedPassword)
        return "<p>Application sent, "+ username +"</p>"
    return render_template("sign-up.html")