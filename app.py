from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# connect database
def get_db():
    conn = sqlite3.connect("placement.db")
    conn.row_factory = sqlite3.Row
    return conn


# HOME PAGE
@app.route('/')
def home():
    db = get_db()
    jobs = db.execute("SELECT * FROM jobs").fetchall()
    return render_template("index.html", jobs=jobs)


# STUDENT REGISTER
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        branch = request.form['branch']
        cgpa = request.form['cgpa']

        db = get_db()
        db.execute(
            "INSERT INTO students(name,email,branch,cgpa) VALUES(?,?,?,?)",
            (name,email,branch,cgpa)
        )
        db.commit()

        return redirect(url_for('home'))

    return render_template("register.html")


# COMPANY POST JOB
@app.route('/postjob', methods=['GET','POST'])
def postjob():

    if request.method == 'POST':
        company = request.form['company']
        role = request.form['role']
        package = request.form['package']

        db = get_db()
        db.execute(
            "INSERT INTO jobs(company,role,package) VALUES(?,?,?)",
            (company,role,package)
        )
        db.commit()

        return redirect(url_for('home'))

    return render_template("postjob.html")


# APPLY FOR JOB
@app.route('/apply/<int:id>', methods=['GET','POST'])
def apply(id):

    if request.method == 'POST':

        name = request.form['name']

        db = get_db()

        db.execute(
            "INSERT INTO applications(student_name,job_id) VALUES(?,?)",
            (name,id)
        )

        db.commit()

        return "<h2>Application Submitted Successfully</h2><a href='/'>Go Back</a>"

    return '''
    <h2>Apply for Job</h2>
    <form method="post">
    Enter your name:<br><br>
    <input name="name" required>
    <br><br>
    <button type="submit">Apply</button>
    </form>
    '''
# ADMIN DASHBOARD
@app.route('/admin')
def admin():

    db = get_db()

    students = db.execute("SELECT * FROM students").fetchall()
    jobs = db.execute("SELECT * FROM jobs").fetchall()
    applications = db.execute("SELECT * FROM applications").fetchall()

    return render_template(
        "admin.html",
        students=students,
        jobs=jobs,
        applications=applications
    )


if __name__ == '__main__':
    app.run(debug=True)