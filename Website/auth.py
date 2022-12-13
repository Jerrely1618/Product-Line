#Login/Sign_up pages

from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import UserApplication,Items as ItemsListed,Users,Reports,Complaints,Transaction_buyer,Transaction_seller,ItemsApplication
from . import db
import base64 #src = https://stackoverflow.com/questions/2323128/convert-string-in-base64-to-image-and-save-on-filesystem
import secrets

verify_page = Blueprint('verify_page',__name__)
def generateToken() -> str:
    return secrets.token_urlsafe(16)

@verify_page.route('/browser/<username>',methods=['POST','GET'])
def browser(username):
    user = Users.query.filter_by(token=username).first()
    if request.method=="POST":
        if "searchItem" in request.form.keys():
            searchItem = request.form["searchItem"]
            itemsList = ItemsListed.query.filter_by(title=searchItem).order_by(ItemsListed.time)
            if itemsList.count()==0:
                itemsList = ItemsListed.query.filter_by(price=searchItem).order_by(ItemsListed.time)
            return render_template("browser.html",items=itemsList,user=user,inputSearch=searchItem)
        elif "submit" in request.form.keys() and request.form["submit"] == "Add Item":
            return redirect("/newItem/"+user.token)
        else:
            itemsList = ItemsListed.query.filter_by(user=user.token).order_by(ItemsListed.time)
            return render_template("browser.html",items=itemsList,user=user)
    itemsList = ItemsListed.query.order_by(ItemsListed.time)
    return render_template("browser.html",items=itemsList,user=user)

@verify_page.route('/history/<username>',methods=['POST','GET'])
def history(username):
    user = Users.query.filter_by(token=username).first()
    choice="sale"
    if request.method=="POST":
        if request.form["submit"] == "Sales":
            choice = "sale"
        else:
            choice = "purchase"
    transactionSell = user.sales
    transactionBuy = user.purchases
    print(transactionSell)
    return render_template("history.html",choice=choice,purchases=transactionBuy,sales=transactionSell,user=user)
@verify_page.route('/transaction/<side>/<item>/<username>',methods=['POST','GET'])
def transaction(side,item,username):
    user = Users.query.filter_by(token=username).first()
    buyerTrans = Transaction_buyer.query.filter_by(title=item).first()
    sellerTrans = Transaction_seller.query.filter_by(title=item).first()
    
    if side == "Buyer":
        if request.method=="POST":
            if(request.form["submit"]=="Rate"):
                rating = request.form["quantity"]
                userRated = Users.query.filter_by(token=sellerTrans.seller).first()
                userRated.totalRatings += 1
                userRated.rating += (int)(rating)
                db.session.commit()
                flash("Rating Submitted",category="success")
            else:
                complaintDesc = request.form["complaint"]
                newComplaint = Complaints(user_complainer=user.token,description=complaintDesc,user=sellerTrans.seller)
                db.session.add(newComplaint)
                db.session.commit()
                flash("Complaint Submitted",category="success")
            return redirect("/browser/"+user.token)
        return render_template("transaction.html",transaction=buyerTrans,user=user)
    else:
        if request.method=="POST":
            if(request.form["submit"]=="Rate"):
                rating = request.form["quantity"]
                userRated = Users.query.filter_by(token=sellerTrans.buyer).first()
                userRated.totalRatings += 1
                userRated.rating += (int)(rating)
                db.session.commit()
                flash("Rating Submitted",category="success")
            else:
                complaintDesc = request.form["complaint"]
                newComplaint = Complaints(user_complainer=user.token,description=complaintDesc,user=sellerTrans.seller)
                db.session.add(newComplaint)
                db.session.commit()
                flash("Complaint Submitted",category="success")
            return redirect("/browser/"+user.token)
        return render_template("transaction.html",transaction=sellerTrans,user=user)

@verify_page.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(email=username).first() 
        if user:
            if user.password != password:
                flash("User or password do not matched with any of our records")   
            else:
                return redirect('/browser/'+user.token)
        flash("User or password do not matched with any of our records")
    return render_template("login.html")

@verify_page.route('/item/<titleName>',methods=['POST','GET'])
def item(titleName):
    item = ItemsListed.query.filter_by(title=titleName).first()
    image = base64.b64encode(item.img).decode('ascii')
    if request.method == "POST":
        newReport = Reports(title=item.title,description = request.form["description"],user_complainer="Guest")
        db.session.add(newReport)
        db.session.commit()
        flash("Reported.",category="success")
    return render_template("item.html",item=item,img = image)

@verify_page.route('/item/<titleName>/<username>',methods=['POST','GET'])
def itemUser(titleName,username):
    user = Users.query.filter_by(token=username).first()
    it = ItemsListed.query.filter_by(title=titleName).first()
    image = base64.b64encode(it.img).decode('ascii')
    if request.method == "POST":
        if request.form["submit"] == "Bid":
            if (float)(it.price) < (float)(request.form["bid"]):
                if((float)(request.form["bid"])<=user.balance):
                    it.price = request.form["bid"]
                    it.user_bidder = user.token
                    db.session.commit()
                    flash("Bid of $"+request.form["bid"]+" submitted",category = "success")
                else:
                    flash("Not enough money",category="error")
            else:
                flash("Too little.",category="error")
        elif request.form["submit"] == "Report Item":
            newReport = Reports(title=it.title,description = request.form["description"],user_complainer=user.token)
            db.session.add(newReport)
            db.session.commit()
            flash("Reported.",category="success")
        elif request.form["submit"]=="Sell":
            buyer = Users.query.filter_by(token=it.user_bidder).first()
            newTransactionBuy = Transaction_buyer(buyer_name = buyer.name,seller_name=user.name,title=it.title,seller = user.token,buyer = it.user_bidder)
            newTransactionSell = Transaction_seller(buyer_name = buyer.name,seller_name=user.name,title=it.title,seller = user.token,buyer = it.user_bidder)
            user.balance+=(int)(it.price)
            buyer.balance-=(int)(it.price)
            db.session.add(newTransactionBuy)
            db.session.add(newTransactionSell)
            db.session.delete(it)
            db.session.commit()
            flash("Item sold.",category = "success")
            return redirect("/browser/"+user.token)
    return render_template("itemUser.html",item=it,img=image,user=user)

@verify_page.route('/newItem/<username>',methods=['POST','GET'])
def itemInput(username):
    user = Users.query.filter_by(token=username).first()
    if request.method=="POST":
        title = request.form.get('title')
        price = request.form.get('price')
        desc = request.form.get('keywords')
        image = request.files['image']
        buyerDummy = "Dummy"
        newItem = ItemsListed(img=image.read(),user_bidder=buyerDummy,title=title,user=user.token,keywords=desc,price=price)
        db.session.add(newItem)
        db.session.commit()
    return render_template('inputItem.html',user=user)

@verify_page.route('/admin/<username>',methods=['POST','GET'])
def admin(username):
    user = Users.query.filter_by(token=username).first()
    def ProcessApplications()->None:
        guestApplication = ' '
        for application in guestApplication:
            if (application.requirements == True):
                Users.append(application.user)
            else:
                print("Item Application Denied")
             

    def ProcessItems()->None:
        itemApplication = ' '
        for application in itemApplication:
            if (application.requirements == True):
                ItemsListed.append(application.item)
            else:
                print("Item Application Denied")
    

    def WarnUser(user)->None:	
        if(Users.complaints>=1):
            print('User warned')
    

    def Statistics()->None:
        reportsComplaints = len(reportsComplaints)
        usersTotal = len(Users)
        itemsApplications = len(itemsApplications)
        items = ' '
        itemsTotal = len(items)
        userApplications = len(userApplications)
        print("Total Users: " + usersTotal + "Total items: " + itemsTotal + "Total user applications: "
         + userApplications + "Total item applications: " + itemsApplications)
    return render_template("admin.html",user=user)
    
@verify_page.route('/procApp/<username>',methods=['POST','GET'])
def procApp(username):
    user = Users.query.filter_by(token=username).first()
    return render_template("admin.html",user=user)
 
@verify_page.route('/procItem/<username>',methods=['POST','GET'])
def procItem(username):
    user = Users.query.filter_by(token=username).first()
    return render_template("admin.html",user=user)
 
@verify_page.route('/warnings/<username>',methods=['POST','GET'])
def warnings(username):
     user = Users.query.filter_by(token=username).first()
     return render_template("admin.html",user=user)
 
@verify_page.route('/stats/<username>',methods=['POST','GET'])
def stats(username):
     user = Users.query.filter_by(token=username).first()
     itemsList = ItemsListed.query.order_by(ItemsListed.time)
     userList = Users.query.order_by(Users.name)
     userApps = UserApplication.query.order_by(UserApplication.name)
     itemsApps = ItemsApplication.query.order_by(ItemsApplication.title)
     return render_template("Stats.html",user=user,users=userList.count(),itemsApp=itemsApps.count(),userApp = userApps.count(),items = itemsList.count())
 
@verify_page.route('/account/<username>',methods=['POST','GET'])
def account(username):
    user = Users.query.filter_by(token=username).first()
    if user.totalRatings > 0:
        rating = user.rating / user.totalRatings
    else:
        rating = 0
    return render_template("account.html",user=user,rating = rating)
   
    def changeBalance(user):
        quantity = ' '
        userBalance = ' '
        if (quantity >= 0):
            userBalance += quantity
        elif (userBalance > quantity):
            userBalance -= quantity
        else:
            print("Not enough funds")
           

    def submitItem():
        picture = ' '
        title = ' '
        keyWords = ' '
        time = ''
        price = ''
        newItem = item(picture, title, keyWords, time, price)
        itemApplication = ' '
        itemsApplications = ' '
        newApplication = itemApplication(item)
        itemsApplications.append(newApplication)


    def submitBid(item, user):
        bid = input("Enter Bid: ")
        userBalance = ' '
        itemBid = ' '
        if (bid <= userBalance and  bid > itemBid):
            itemBid = bid
            itemBidder = user
    
    def complaint(user):
        complaintInfo = input("Enter your complaint: ")
        report = ' '
        userComplaint = ' '
        userComplaint += 1
        newComplaint = report

    def rate(user):
        rating = input("Enter rating between 1 & 5: ")
        userRatings = ' '
        userRatings.append(rating)

    def transactionHistory():
        item1 = ' '
        item2 = ' '
        price1 = ' '
        price2 = ' '
        transactionDict = {item1: price1, item2: price2}
        print(transactionDict)

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
        userPassword = ' '
        newPassword = userPassword

        newName = input("Enter New Name: ")
        userName = ' '
        newName = userName

        newAddress = input("Enter New Address: ")
        userAddress = ' '
        newAddress = userAddress

        newPhone = input("Enter New Phone Number: ")
        userPhone = ' '
        newPhone = userPhone

        newCreditCardNumber = input("Enter New Credit Card Number: ")
        userCreditCardNumber = ' '
        newCreditCardNumber = userCreditCardNumber

        def browse():
            word = ' '
            itemTitle = ' '
            for item in ItemsListed:
                if(itemTitle == word):
                    return item

        def ordinaryApplication(userName, userAddress, userPhone, userPassword, userCreditCardNumber):
            newUser = user(userName, userAddress, userPassword, userPhone, userCreditCardNumber)
            NewApplication = UserApplication(user)
            itemsApplications = ' '
            itemsApplications.append(NewApplication)

        def submitReport(item):
            reportInfo = ' '
            reportsComplaints = ' '
            newReport = reportsComplaints(reportInfo, item.user)
            reportsComplaints.append(newReport)

@verify_page.route('/balance/<username>',methods=['POST','GET'])
def balance(username):
    user = Users.query.filter_by(token=username).first()
    if request.method=="POST":
        add = request.form["balance"]
        if (int)(add) <=0:
            flash("Input a positive number",category="error")
        else:
            flash("Balance Updated",category="success")
            user.balance+=(int)(add)
            db.session.commit()
    return render_template("changebalance.html",user=user)
    
@verify_page.route('/ChangeInfo/<username>',methods=['POST','GET'])
def ChangeInfo(username):
    user = Users.query.filter_by(token=username).first()
    if request.method == "POST":
        
        if request.form["submit"] == "Change Name":
            return render_template("changeinfo.html",user=user, change="Name")
        elif request.form["submit"] == "Change Email":
            return render_template("changeinfo.html",user=user, change="Email")
        elif request.form["submit"] == "Change Password":
            return render_template("changeinfo.html",user=user, change="Password")
        elif request.form["submit"] == "Change Address":
            return render_template("changeinfo.html",user=user, change="Address")
        elif request.form["submit"] == "Change Phone":
            return render_template("changeinfo.html",user=user, change="Phone")
        elif request.form["submit"] == "Change Credit Card Number":
            return render_template("changeinfo.html",user=user, change="Card")
        else:
            if "oldPass" in request.form.keys():
                old = request.form["oldPass"]
                new = request.form["newPass"]
                confirm = request.form["confirmPass"]
                if old != user.password:
                    print(user.password)
                    flash("Wrong Password.",category="error")
                    return render_template("changeinfo.html",user=user, change="Password")
                else:
                    if new != confirm:
                        flash("Passwords do not match.",category="error")
                        return render_template("changeinfo.html",user=user, change="Password")
                    else:
                        user.password = new
            elif "Address" in request.form.keys():
                address = request.form["Address"]
                user.address = address
            elif "Card" in request.form.keys():
                card = request.form["Card"]
                user.credit_card = card
            elif "Number" in request.form.keys():
                num = request.form["Number"]
                user.phone = num
            elif "Email" in request.form.keys():
                email = request.form["Email"]
                confirm = request.form["confirmEmail"]
                if email != confirm:
                    flash("Emails do not match.")
                    return render_template("changeinfo.html",user=user, change="Email")
                else:
                    user.email = email
            elif "Name" in request.form.keys():
                name = request.form["Name"]
                user.name = name
            db.session.commit()
            flash("Changes commited",category="success")
            return render_template("changeinfo.html",user=user, change="None")
    else:
        return render_template("changeinfo.html",user=user, change="None")
    
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