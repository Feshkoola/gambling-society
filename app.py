from flask import Flask, render_template, url_for, request, session, redirect
import requests
import hashlib, os, base64
from datetime import datetime
from datetime import date, timedelta


app = Flask(__name__)

app.secret_key = "B22T_i33s C444o32299o#:@l"

# normal functions

# password checker
def verify_password(stored, entered_password):
    stored_bytes = base64.b64decode(stored)
    salt = stored_bytes[:16]
    stored_hash = stored_bytes[16:]

    new_hash = hashlib.pbkdf2_hmac(
        'sha256',
        entered_password.encode(),
        salt,
        100_000
    )

    return new_hash == stored_hash

# password hasher
def hash_password(password):
    salt = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac(
        'sha256',              
        password.encode(),     
        salt,                  
        100_000                
    )
    return base64.b64encode(salt + hash_bytes).decode()

# last week date return
def last_week():
    today = date.today()
    last_week = today - timedelta(days=6)

    return last_week.isoformat()


# database stuff
SUPABASE_URL = "https://neehcnxytejzkfdlpxsg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5lZWhjbnh5dGVqemtmZGxweHNnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc4ODMwNzAsImV4cCI6MjA5MzQ1OTA3MH0._x7QCrKWaqWALBfwE1uAUahOQ1BItw4XCTDlw6OJl8U"


def insert_user(username, password):
    hashed = hash_password(password)

    data = {
        "username": username,
        "password": hashed,
        "created_at": date.today().isoformat()   
    }

    # Send to Supabase REST API
    url = f"{SUPABASE_URL}/rest/v1/users"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        return redirect("/signin")
    else:
        return f"Error: {response.text}"


def check_user(username, password):

    url = f'{SUPABASE_URL}/rest/v1/users?username=eq.{username}'
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    response = requests.get(url, headers=headers)
    print("RESPONSE:", response.text)

    users = response.json()

    if len(users) == 0:
        return "Invalid login", 401
    
    user = users[0]
    
    stored_hash = user["password"]

    if verify_password(stored_hash, password):
        session["user"] = username
        return redirect("/dashboard")
    return "Invalid Password", 401



def weekly_profit_calculate(username):

    last_week_day = last_week()


    url = f'{SUPABASE_URL}/rest/v1/games?username=eq.{username}&date=gte.{last_week_day}'

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    response=requests.get(url, headers=headers)

    print("RAW RESPONSE:", response.text)

    
    data = response.json()

    total = 0

    for i in data:
        total = total + i["turts"]

    return total





def weekly_wins_calculation(username):

    last_week_day = last_week()


    url = f'{SUPABASE_URL}/rest/v1/games?username=eq.{username}&date=gte.{last_week_day}'

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    response=requests.get(url, headers=headers)

    print("RAW RESPONSE:", response.text)

    
    data = response.json()

    total = 0

    for i in data:
        if i["turts"] > 0:
            total = total+1

    return total

def weekly_losses_calculation(username):

    last_week_day = last_week()


    url = f'{SUPABASE_URL}/rest/v1/games?username=eq.{username}&date=gte.{last_week_day}'

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    response=requests.get(url, headers=headers)

    print("RAW RESPONSE:", response.text)

    
    data = response.json()

    total = 0

    for i in data:
        if i["turts"] < 0:
            total = total+1

    return total



def streak_update(username):
    last_week_day = last_week()


    url = f'{SUPABASE_URL}/rest/v1/users?username=eq.{username}'

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    user = data[0]
    last = user["last_log"]

    today = date.today()

    if last == today.isoformat():
        return user["streak"]
    elif last == (today - timedelta(days=1)).isoformat():
        url = f'{SUPABASE_URL}/rest/v1/users?username=eq.{username}'
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }

        data_change = {
            "streak": user["streak"] + 1,
            "last_log": today.isoformat()
        }

        response = requests.patch(url, json=data_change, headers=headers)
        print("PATCH STATUS:", response.status_code)
        print("PATCH TEXT:", response.text)


        return user["streak"] + 1
    else:
        url = f'{SUPABASE_URL}/rest/v1/users?username=eq.{username}'
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }

        data_change = {
            "streak": 1,
            "last_log": today.isoformat()
        }

        response = requests.patch(url, json=data_change, headers=headers)

        return 1
    
   
def get_achievements(username):
    url = f'{SUPABASE_URL}/rest/v1/achievements?username=eq.{username}&order=date.desc&limit=3'

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    print("ACHIEVEMENT DATA:", data)


    values =[]

    for i in range(len(data)):
        if i == 0:
            values.append(f'{data[i]["date"]} - {data[i]["achievement"]}')
            values.append(data[i]["content"])
        else:
            values.append(f'{data[i]["date"]} - {data[i]["achievement"]}')
    
    return values


def weekly_profit_graph_calculation(username):
    today = date.today()
    week_start = today - timedelta(days=6)

    # Fetch all games from the past week
    url = f"{SUPABASE_URL}/rest/v1/games?username=eq.{username}&date=gte.{week_start.isoformat()}&order=date.asc"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    # Sum turts per date
    totals = {}
    for row in data:
        day = row["date"]
        totals[day] = totals.get(day, 0) + row["turts"]

    # Build full 7‑day list (fill missing days with 0)
    days = []
    turts = []
    for i in range(7):
        d = (week_start + timedelta(days=i)).isoformat()
        days.append(d)
        turts.append(totals.get(d, 0))

    return days, turts





def total_turts_calculation(username): #the actual calculation btw
    url = f"{SUPABASE_URL}/rest/v1/games?username=eq.{username}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    total = 0
    for i in data:
        total = total + i["turts"]
    
    return total

    
def best_game_check(username):
    url = f"{SUPABASE_URL}/rest/v1/games?username=eq.{username}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    totals = {
        "Poker": 0,
        "Blackjack": 0,
        "Big 2": 0,
        "Big Turtle": 0
    }

    for i in data:
        if i["game"] == "poker":
            totals["Poker"] += i["turts"]
        elif i["game"] == "blackjack":
            totals["Blackjack"] += i["turts"]
        elif i["game"] == "big2":
            totals["Big 2"] += i["turts"]
        elif i["game"] == "bigturtle":
            totals["Big Turtle"] += i["turts"]

    biggest_name = max(totals, key=totals.get)
    biggest_value = totals[biggest_name]

    return biggest_name












# routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/blog")
def blog():
    return render_template("blog.html")













# Dashboard

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/signin")
    username = session.get("user")
    
    weekly_profit = weekly_profit_calculate(username)

    weekly_wins = weekly_wins_calculation(username)
    weekly_losses = weekly_losses_calculation(username)

    streak = streak_update(username)

    achievements = get_achievements(username)

    total_turts = total_turts_calculation(username)

    days, turts = weekly_profit_graph_calculation(username)

    best_game = best_game_check(username)


    return render_template("dashboard.html", username=username, weekly_profit=weekly_profit, weekly_wins=weekly_wins, weekly_losses=weekly_losses, streak=streak, achievements=achievements, days=days, turts=turts, total_turts=total_turts, best_game=best_game)
 

















@app.route("/games")
def games():
    return render_template("games.html")



@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")

    username = request.form.get("username")
    password = request.form.get("password")

    return check_user(username, password)



@app.route("/signout")
def signout():
    session.pop("user", None)
    return redirect("/")



@app.route("/create-account", methods=["GET", "POST"])
def createAccount():
    if request.method == "GET":
        return render_template("create-account.html")
    
    username = request.form.get("username")
    password = request.form.get("password")

    return insert_user(username, password)
    


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)