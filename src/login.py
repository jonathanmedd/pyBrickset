@app.route("/login", ["GET", "POST"])
def login():
   # No need to authenticate again
   if current_user.is_authenticated:
       return redirect(url_for("index"))

   # User authentication
   form = LoginForm()
   if form.validate_on_submit():
       user = User.query.filter_by(username=form.username.data).first()

       # User entered correct password?
       if user is None or not user.check_password(form.password.data):
           flash("Invalid username or password")
           return redirect(url_for("login"))

       login_user(user)
       return redirect(url_for("user_page"))

   return render_template("login.html", form = form)