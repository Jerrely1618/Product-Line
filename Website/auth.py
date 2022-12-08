#Login/Sign_up pages

from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import UserApplication,ItemsListed,Users
from . import db
import base64
verify_page = Blueprint('verify_page',__name__)

@verify_page.route('/browser/<username>',methods=['POST','GET'])
def browser(username):
    userSent = Users.query.filter_by(email=username)
    for i in userSent:
        user = i
    if request.method=="POST":
        # image = request.files['img']
        # for i in range(10):
        #     title = "NewObj"+str(i)
        #     desc = "red beautiful"
        #     priceRange = "56-98"
        #     newItem = ItemsListed(title=title,keywords=desc,priceRange=priceRange,img=image.read())
        #     db.session.add(newItem)
        #     db.session.commit()
        searchItem = request.form["searchItem"]
        itemsList = ItemsListed.query.filter_by(title=searchItem).order_by(ItemsListed.time)
        if itemsList.count() == 0:
            itemsListWord = ItemsListed.query.order_by(ItemsListed.time)
            for item in itemsListWord:
                if searchItem in item.keywords:
                    return render_template("browser.html",items=itemsListWord,user=user)
        return render_template("browser.html",items=itemsList,user=user,inputSearch=searchItem)
    itemsList = ItemsListed.query.order_by(ItemsListed.time)
    return render_template("browser.html",items=itemsList,user=user)

@verify_page.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']
        users = Users.query.filter_by(email=username)
        for user in users:  
            if user.password != password:
                flash("User or password do not matched with any of our records")   
            else:
                return redirect('/browser/'+username)
        flash("User or password do not matched with any of our records")
    # username = "random89@gmail.com"
    # password = "random89"
    # name = "randy"
    # phone = "213809128645463"
    # creditcard="3213124121"
    # address = "Brooklyna"
    # tryUser = Users(name=name,email=username,phone=phone,credit_card=creditcard,address=address,password=password)
    # db.session.add(tryUser)
    # db.session.commit()
    
    return render_template("login.html")
@verify_page.route('/item/<titleName>',methods=['POST','GET'])
def item(titleName):
    item = ItemsListed.query.filter_by(title=titleName)
    for it in item:
        image = base64.b64encode(it.img).decode('ascii')
        print(image)
    return render_template("item.html",items=item,img = image)
@verify_page.route('/item/<titleName>/<username>',methods=['POST','GET'])
def itemUser(titleName,username):
    userSent = Users.query.filter_by(email=username)
    for i in userSent:
        user = i
    item = ItemsListed.query.filter_by(title=titleName)
    for it in item:
        image = base64.b64encode(it.img).decode('ascii')
    return render_template("itemUser.html",items=item,img=image,user=user)

@verify_page.route('/admin',methods=['POST','GET'])
def admin():
     def ProcessApplications():
      for application in guestApplication:
           if (application.requirements == True):
               Users.append(application.user)
             

     def ProcessItems():
        for application in ItemApplication:
            if (application.requirements == True):
               ItemsListed.append(application.item)
    

     def WarnUser(user):	
       if(Users.complaints>=1):
          print('User warned')
    

     def Statistics():
        reportsComplaints = len(reportsComplaints)
        usersTotal = len(Users)
        itemsApplications = len(itemsApplications)
        itemsTotal = len(items)
        userApplications = len(userApplications)
        print("Total Users: " + usersTotal + "Total items: " + itemsTotal + "Total user applications: "
         + userApplications + "Total item applications: " + itemsApplications)

    return render_template("admin.html")
 
@verify_page.route('/account',methods=['POST','GET'])
def account():
    def changeBalance(user):
        quantity = 1

    def submitItem():
        picture = ' '
        title = ' '
        keyWords = ' '
        time
        price

         

    def submitBid(item, user):
        bid = input("Enter Bid: ")
    

    def complaint(user):
        complaintInfo = input("Enter your complaint: ")

    def rate(user):
        rating = input("Enter rating between 1 & 5: ")

    def transactionHistory():
        transactionDict = {item1: price1, item2: price2}
        print(transactionDict[i])

    def accountInfo(user):
        userPassword = input("Enter Password: ")
        userName = input("Enter Name: ")
        userAddress = input("Enter Address: ")
        userPhone = input(" Enter Phone Number: ")
        userCreditCardNumber = input("Enter Credit Card Number: ")
        
        print("Password: " + userPassword + "Name: " + userName + "Address: "
        + userAddress + "Phone: " + userPhone + "Credit Card Number: "
        + userCreditCardNumber)

    def changeInfo():
        newPassword = input("Enter New Password: ")
        newPassword = userPassword

        newName = input("Enter New Name: ")
        newName = userName

        newAddress = input("Enter New Address: ")
        newAddress = userAddress

        newPhone = input("Enter New Phone Number: ")
        newPhone = userPhone

        newCreditCardNumber = input("Enter New Credit Card Number: ")
        newCreditCardNumber = userCreditCardNumber



    
    return render_template("account.html")

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
        if len(username) < 3:
            flash("Name should be at least 3 characters",category="error")
        elif email != VerifiedEmail or len(email)<3:
            flash("Emails do not match.",category="error")
        elif Password != VerifiedPassword:
            flash("Passwords do not match.",category="error")
        elif len(Password) < 7:
            flash("Passsword is too short.",category="error")
        else:             
            newGuestApp = UserApplication(name=username,email=email,password=Password,address=address,phone=phoneNum,credit_card=creditCard)
            db.session.add(newGuestApp)
            db.session.commit()
            flash("Application sent",category="Sucess")
            return redirect(url_for("pages.home"))
    return render_template("sign-up.html")