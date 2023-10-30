import os
import datetime
import sys, math

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, password_rules

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance2.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":
        user = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])
        cash = user[0]["cash"]

        holdings = db.execute("SELECT * FROM holdings WHERE user_id=:user_id", user_id=session["user_id"])

        # Total asset value counter
        assets = float(cash)

        # For each holding in holdings
        for holding in holdings:

            # Lookup the data of the first stock by using function lookup on holding["symbol"] which is the first holding
            stock = lookup(holding["symbol"])

            # Store the data
            holding["name"] = stock["name"]
            holding["symbol"] = stock["symbol"]
            holding["price"] = stock["price"]
            holding["total"] = float(holding["price"]) * float(holding["amount"])

            # Add to total asset value
            assets += float(holding["total"])

            # Convert to USD
            holding["price"] = usd(float(holding["price"]))
            holding["total"] = usd(float(holding["total"]))

        return render_template("index.html", cash=cash, total=assets, holdings=holdings)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    else:
        # Number of shares ordered
        shares = request.form.get("shares")
        if not shares:
            return apology("Please enter a valid number of shares.")
        if not shares.isdigit():
            return apology("Fractional trading is currently unavailable.")

        # Symbol that the user searched
        searchSymbol = request.form.get("symbol")

        # Check if user inputted a symbol
        if not searchSymbol:
            return apology("Please provide a stock symbol.")

        # Lookup symbol
        searchSymbol = searchSymbol.upper()
        symbol = lookup(searchSymbol)

        # Check if symbol exists, if not return apology
        if symbol == None:
            return apology("Stock symbol returned no results.")

        # Check if shares ordered is 1 or more
        shares = int(shares)
        if shares <= 0:
            return apology("You may only buy 1 or more shares")

        # Price of one share
        sharePrice = symbol["price"]

        # Total cost of order, number of shares ordered * price of one share
        cost = shares * sharePrice

        # Current balance of the user
        userCash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # Remaining cash of user after the transaction
        userCash = float(userCash[0]['cash'])
        remCash = userCash - cost

        # If user does not have enough funds to complete the transaction
        if remCash < 0:
            return apology("Unfortunately you do not have enough funds to complete this transaction.")
        else:
            # Date and time
            now = datetime.datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")

            # Insert transaction details into the transaction table
            transaction = db.execute("INSERT INTO transactions (user_id, name, symbol, price, amount, cost, transaction_type, date_time) VALUES (:user_id, :name, :symbol, :price, :amount, :cost, :transaction_type, :date_time)", user_id=session["user_id"], name=symbol["name"], symbol=symbol["symbol"], price=sharePrice, amount=shares, cost=cost, transaction_type="Purchase", date_time=date_time)

            # Update the user's balance
            update = db.execute("UPDATE users SET cash=:remCash WHERE id=:user_id", remCash=remCash, user_id=session["user_id"])

            # Update the user's holdings
            holding = db.execute("SELECT symbol FROM holdings WHERE symbol=:symbol AND user_id=:user_id", symbol=symbol["symbol"], user_id=session["user_id"])

            # If user did not own any of the company's shares previously
            if len(holding) < 1:
                addHoldings = db.execute("INSERT INTO holdings (user_id, name, symbol, amount) VALUES (:user_id, :name, :symbol, :amount)", user_id=session["user_id"], name=symbol["name"], symbol=symbol["symbol"], amount=shares)

            # If user owns at least one share of the company's shares
            else:
                # Get the number of current shares owned
                currentHoldings = db.execute("SELECT amount FROM holdings WHERE user_id=:user_id AND symbol=:symbol", user_id=session["user_id"], symbol=symbol["symbol"])

                # Cast to int
                currentAmount = int(currentHoldings[0]["amount"])

                # Calculate final amount of shares
                finalAmount = shares + currentAmount

                # Update the shares to the database
                updateHoldings = db.execute("UPDATE holdings SET amount=:finalAmount WHERE user_id=:user_id AND symbol=:symbol", user_id=session["user_id"], symbol=symbol["symbol"], finalAmount=finalAmount)

            # Return user to index
            return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    if request.method == "GET":
        transactions = db.execute("SELECT * FROM transactions WHERE user_id=:user_id", user_id=session["user_id"])

        for transaction in transactions:
            transaction["price"] = usd(float(transaction["price"]))
            transaction["cost"] = usd(float(transaction["cost"]))

        return render_template("history.html", transactions=transactions)

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
        searchSymbol = request.form.get("symbol")
        symbol = lookup(searchSymbol)
        if symbol == None:
            return apology("Stock symbol returned no results.")

        return render_template("quoted.html", symbol=symbol)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("Please provide a username.")

        elif not request.form.get("password"):
            return apology("Please provide a password.")

        newUsername = request.form.get("username")
        newPassword = request.form.get("password")
        cfmNewPassword = request.form.get("confirmation")

        if newPassword != cfmNewPassword:
            return apology("Please ensure passwords match.")

        if password_rules(newPassword):
            hashPassword = generate_password_hash(newPassword)
        else:
            return apology("Please ensure password is between 8 and 20 characters, contains uppercase and lowercase characters, and at least one digit")

        rows = db.execute("SELECT * FROM users WHERE username = :newUsername", newUsername=newUsername)
        if len(rows) != 0:
            return apology("Sorry, your username has already been taken. Please choose a new username.")

        db.execute("INSERT INTO users (username,hash) VALUES (:newUsername, :hashPassword)", newUsername=newUsername, hashPassword=hashPassword)

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":

        # Dropdown menu options for the list of stocks owned
        holdings = db.execute("SELECT symbol FROM holdings WHERE user_id=:user_id", user_id=session["user_id"])

        return render_template("sell.html", holdings=holdings)

    else:

        # Stock sold
        soldSymbol = request.form.get("symbol")

        # Check if user selected a stock
        if not soldSymbol:
            return apology("Please select a stock.")

        # Lookup symbol
        symbol = lookup(soldSymbol)

        # Check if symbol exists/is owned, if not return apology
        if symbol == None:
            return apology("Stock symbol is invalid.")

        # Get the current number of shares owned
        currentHoldings = db.execute("SELECT amount FROM holdings WHERE user_id=:user_id AND symbol=:symbol", user_id=session["user_id"], symbol=symbol["symbol"])
        currentAmount = int(currentHoldings[0]["amount"])

        # Shares sold
        shares = request.form.get("shares")
        if not shares:
            return apology("Please select a number of stocks to sell.")

        # If user sold too many shares
        shares = int(shares)
        if shares > currentAmount:
            return apology("You have sold too many shares.")

        # Price of one share
        sharePrice = symbol["price"]

        # Total value sold, number of shares sold * price of one share
        value = shares * sharePrice

        # Current balance of user
        userCash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # New balance of user after transaction
        userCash = float(userCash[0]['cash'])
        newCash = userCash + value

        # Log into transactions
        # Date and time
        now = datetime.datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")

        # Insert transaction details into the transaction table
        transaction = db.execute("INSERT INTO transactions (user_id, name, symbol, price, amount, cost, transaction_type, date_time) VALUES (:user_id, :name, :symbol, :price, :amount, :cost, :transaction_type, :date_time)", user_id=session["user_id"], name=symbol["name"], symbol=symbol["symbol"], price=sharePrice, amount=shares, cost=value, transaction_type="Sale", date_time=date_time)

        # Update the user's balance
        update = db.execute("UPDATE users SET cash=:newCash WHERE id=:user_id", newCash=newCash, user_id=session["user_id"])

        # Update the user's holdings
        holding = db.execute("SELECT symbol FROM holdings WHERE symbol=:symbol AND user_id=:user_id", symbol=symbol["symbol"], user_id=session["user_id"])

        # Get the current number of shares owned
        currentHoldings = db.execute("SELECT amount FROM holdings WHERE user_id=:user_id AND symbol=:symbol", user_id=session["user_id"], symbol=symbol["symbol"])
        finalAmount = currentAmount - shares
        updateHoldings = db.execute("UPDATE holdings SET amount=:finalAmount WHERE user_id=:user_id AND symbol=:symbol", user_id=session["user_id"], symbol=symbol["symbol"], finalAmount=finalAmount)

        # Delete row if number of shares left is 0
        if finalAmount == 0:
            deleteHolding = db.execute("DELETE FROM holdings WHERE user_id=:user_id AND symbol=:symbol", user_id=session["user_id"], symbol=symbol["symbol"])
        return redirect("/")
