from flaskMoviesApp import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    profile_image = db.Column(db.String(30), nullable=False, default='default_profile_image.jpg')
    password = db.Column(db.String(15), nullable=False)
    movies = db.relationship('Movie', backref='author', lazy=True)

    def __repr__(self):
        return f"{self.username}:{self.email}"



class Movie(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(50), nullable=False) ## δήλωση τίτλου (50 χαρακτήρες), υποχρεωτικό πεδίο
    plot =db.Column(db.Text(), nullable=False) ## δήλωση υπόθεσης ταινίας (κείμενο με απεριόριστο αριθμό χαρακτήρων), υποχρεωτικό πεδίο
    image = db.Column(db.String(30), nullable=False, default='default_movie_image.png')## δήλωση ονόματος εικόνας ταινίας (40 χαρακτήρες) με προεπιλεγμένο τίτλο:'default_movie_image.png', ΜΗ υποχρεωτικό πεδίο
    rating = db.Column(db.Integer, nullable=False, default=1)  ## Integer, δήλωση πεδίου βαθμολογίας ταινίας, με προεπιλεγμένη τιμή το μηδέν: default=1, υποχρεωτικό πεδίο
    release_year = db.Column(db.Integer, nullable=False, default=2000) ## Integer, δήλωση πεδίου χρονιάς πρώτης προβολής της ταινίας με προεπιλεγμένη τιμή default=2000, υποχρεωτικό πεδίο
    insert_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) ## δήλωση ημερομηνίας δημιουργίας ταινίας τύπου DateTime με προεπιλεγμένη τιμή: default=datetime.utcnow
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) ## δήλωση ID του χρήστη που αποθήκευσε την ταινία, ForeignKey στο πεδίο id του πίνακα user, υποχρεωτικό πεδίο

    def __repr__(self):
        return f"{self.insert_date}:{self.title}:{self.rating}"
    