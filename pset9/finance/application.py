import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":
        
        #slect all stocks the user owns
        stocks = db.execute("SELECT symbol, quantity FROM portfolio WHERE user_id = ?", session["user_id"])
        
        #initialize variables for users cash and value of all their assets    
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = user_cash[0]["cash"]
        assets_value = cash
        
        #make sure user has stocks
        if not stocks:
            return render_template("indexed.html", cash=cash, assets_value=assets_value)
        
        #iterate through each stock the user owns, and insert the current price, value of the stocks 
        for stock in stocks:
            price = lookup(stock["symbol"])["price"]
            value = stock["quantity"] * price
            stock.update({"price": price, "value": value})
            assets_value += value
            if stock["quantity"] == 0:
                db.execute("DELETE FROM portfolio WHERE quantity = 0 AND user_id = ?", session["user_id"])
        
        #if user doesn't own that stock anymore, delete it from portfolio    
        #f stock["quantity"] == 0:
            #db.execute("DELETE FROM portfolio WHERE quantity = 0 AND user_id = ?", session["user_id"])
            
        return render_template("index.html", value=value, cash=cash, assets_value=assets_value, price=price, stocks=stocks)
    
    else:
        amount = request.form.get("add_cash")
        
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", amount, session["user_id"])
        
        return redirect("/")



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    
    #If method is POST:
    else:
        
        #Ensure user gives valid input
        if request.form.get("symbol") == "" or lookup(request.form.get("symbol")) == None:
            return apology("Must enter a valid stock symbol")
            
        if not str.isdigit(request.form.get("shares")):
            return apology("Enter a valid integer")
            
        if int(request.form.get("shares")) <= 0 or request.form.get("shares") == "":
            return apology("Must enter a valid quantity")
        
        else:
            #Initialize variables. stock_info = price, symbol, name of stock
            stock_info = lookup(request.form.get("symbol"))
            quantity = int(request.form.get("shares"))
            
            #initialize variables: how much the transactions costs & amount of cash user has
            cost = stock_info["price"] * quantity
            user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            
            # ensure user has enough cash for the transaction
            if  user_cash[0]["cash"] < cost:
                return apology("You do not have enough cash for this transaction")
                
            #insert transaction into transactions
            db.execute("INSERT INTO transactions (symbol, price, quantity, user_id, type) values(?, ?, ?, ?, ?)", stock_info["symbol"], stock_info["price"], quantity, session["user_id"], "buy")
            
            #if user has enough cash, initialize variable for their new cash total
            new_cash = int(user_cash[0]["cash"] - cost)
            
            #update users cash to new_cash value
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])
            
            #select all stocks the user owns
            stock = db.execute("SELECT symbol FROM portfolio WHERE user_id = ?", session["user_id"])
    
            #if stock is not in portfolio add it to portfolio
            if stock_info["symbol"] not in stock:
                db.execute("INSERT INTO portfolio (symbol, price, quantity, user_id) values(?, ?, ?, ?)", stock_info["symbol"], stock_info["price"], quantity, session["user_id"])
            
            #if stock is in portfolio, update the quantity of that stock
            else:
                db.execute("UPDATE portfolio SET quantity = quantity + ? WHERE symbol = ? AND user_id = ?", quantity, stock_info["symbol"], session["user_id"])
            
            return redirect("/")
            


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    #Select all transactions of the user_id
    portfolio = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])
    
    #see if user has made any transactions
    if not portfolio:
        return apology("you have not made any transactions")
        
    return render_template("history.html", stocks=portfolio)    
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    
    else:
        #look up price of stock
        quote = lookup(request.form.get("symbol"))
        
        #make sure user has entered a valid quote
        if quote == "" or quote == None:
            return apology("Must enter a valid stock symbol")
        
        #return user to quoted page to see the price of stock    
        else:    
            return render_template("quoted.html", quote=quote, price=quote["price"])
        


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    session.clear()
        
    if request.method == "GET":
        return render_template("register.html")
    # check username and password
    else:
        #initialize variables for user input
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        #make sure all input fields are valid
        if username == "":
            return apology("Please select a username")
            
        elif len(db.execute('SELECT username FROM users WHERE username = ?', username)) > 0:  
            return apology("Username is taken")
        
        elif password == "":
            return apology("Please select a password")
            
        elif password != confirmation:
            return apology("Password does not match")
            
        #insert username and password hash into users table
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))

        #Log the user in after they register and return them to the index page
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
    
        return redirect("/")
        
        
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        #get stocks and quantity that the user owns
        portfolio = db.execute("SELECT symbol FROM portfolio WHERE user_id = ?", session["user_id"])
        
        return render_template("sell.html", stocks=portfolio)
    
    else:
        #initialize variables for symbol & shares
        shares_requested = int(request.form.get("shares"))
        stock_requested =  request.form.get("symbol")
        print(shares_requested)
        
        #initialize variable getting all the user stocks (symbol, price, quantity, user_id)
        stocks = db.execute("SELECT quantity FROM portfolio WHERE symbol = ? AND user_id = ?", stock_requested, session["user_id"])
        stocks_name = db.execute("SELECT symbol FROM portfolio WHERE symbol = ? AND user_id = ?", stock_requested, session["user_id"])
        print(stocks[0]["quantity"])
        
        #make sure user enters valid inputs (stock, quantity)
        if stock_requested == "":
            return apology("Please enter a valid stock symbol")
        
        if shares_requested == "":
            return apology("Please enter a quantity greater than 1")
            
        if stock_requested not in stocks_name[0]["symbol"]:
            return apology("You do not own any of that stock")
        
        if stocks[0]["quantity"] < shares_requested:
            return apology("You do not have enough shares to complete this transaction")
            
        
        #create a query to insert into transactions
        stock_info = lookup(stock_requested)
        db.execute("INSERT INTO transactions (symbol, price, quantity, user_id, type) values(?, ?, ?, ?, ?)", stock_requested, stock_info["price"], shares_requested, session["user_id"], "sell")
        
        #create a query to update portfolio
        new_quantity = stocks[0]["quantity"] - shares_requested
        db.execute("UPDATE portfolio SET quantity = ? WHERE symbol = ? AND user_id = ?", new_quantity, stock_requested, session["user_id"])
        
        #create a query to update user cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", (stock_info["price"] * shares_requested), session["user_id"])
        
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
