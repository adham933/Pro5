from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secretkey123"

users = {
    "test": {"first": "Test", "last": "User", "password": "1234"}
}


@app.route("/")
def root():
    return redirect(url_for("login"))


@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("homepage.html", username=session["user"])

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        if username in users:
            return "Username already exists!"

        if password != confirm:
            return "Passwords do not match!"

        users[username] = {
            "first": first_name,
            "last": last_name,
            "password": password
        }

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", username=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
