from flask import render_template, redirect, url_for, request, flash, abort

from flaskMoviesApp.forms import SignupForm, LoginForm, NewMovieForm, AccountUpdateForm
from flaskMoviesApp import app, db, bcrypt

from flaskMoviesApp.models import User, Movie
from flask_login import login_user, current_user, logout_user, login_required
## diko moy add @@@@@@@@@@@@@@@@@@@



from werkzeug.utils import secure_filename

import secrets, os
from PIL import Image

from datetime import datetime as dt

### Συμπληρώστε κάποια από τα imports που έχουν αφαιρεθεί ###
from sqlalchemy import desc

current_year = dt.now().year



### Μέθοδος μετονομασίας και αποθήκευσης εικόνας ###
def image_save(image, where, size):
    random_filename = secrets.token_hex(8)
    file_name, file_extension = os.path.splitext(image.filename)
    image_filename = random_filename + file_extension
    image_path = os.path.join(
        app.root_path, 'static/images/' + where, image_filename)

    image_size = size  # this must be a tupe in the form of: (150, 150)
    img = Image.open(image)
    img.thumbnail(image_size)

    img.save(image_path)

    return image_filename


### ERROR HANDLERS START ### CHECK @@@@@@@@@@@@@@@@@@@

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(415)
def unsupported_media_type(e):
    return render_template('errors/415.html'), 415

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

## Εδώ πρέπει να μπεί ο κώδικας για τους error handlers (πχ για το error 404 κλπ).
## Θα πρέπει να φτιαχτούν οι error handlers για τα errors 404, 415 και 500.

### ERROR HANDLERS END ###






### Αρχική Σελίδα ###
@app.route("/home/")
@app.route("/")
def root():
    page = request.args.get('page', 1, type=int)
    ordering = request.args.get('ordering',1, type=str)

    ## EKANA KAPOIES ALLAGOYLES @@@@@@@@@@@@@@@@@@@

    ## Να προστεθεί σε αυτό το view ότι χρειάζεται για την ταξινόμηση
    ## ανά ημερομηνία εισαγωγής στη βάση, ανά έτος προβολής και ανά rating
    ## με σωστή σελιδοποίηση για την κάθε περίπτωση.
    if ordering == "release_year":
        movies = Movie.query.order_by(desc(Movie.release_year)).paginate(page=page, per_page=5)
        return render_template("index.html", movies=movies, ordering=ordering)
    elif ordering == "rating":
        movies = Movie.query.order_by(desc(Movie.rating)).paginate(page=page, per_page=5)
        return render_template("index.html", movies=movies, ordering=ordering)
        

    movies = Movie.query.order_by(desc(Movie.insert_date)).paginate(page=page, per_page=5)
    
    return render_template("index.html", movies=movies, ordering=ordering)
        
    
    ## Pagination: page value from 'page' parameter from url


    ## Για σωστή ταξινόμηση ίσως πρέπει να περάσετε κάτι επιπλέον μέσα στο context.
    ## Υπενθύμιση: το context είναι το σύνολο των παραμέτρων που περνάμε
    ##             μέσω της render_template μέσα στα templates μας
    ##             στην παρακάτω περίπτωση το context περιέχει μόνο το movies=movies
    ## PROSTHESA KAI STO RENDER TEMPLATE OTI ELEIPE @@@@@@@@@@@@@@@@@@@#######################################################
    ## TA PERASA ME TA ONOMATA TOYS 

   

@app.route("/signup/", methods=['GET','POST'])
def signup():
    ## Έλεγχος για το αν ο χρήστης έχει κάνει login ώστε αν έχει κάνει,
    ## να μεταφέρεται στην αρχική σελίδα

    ## TO TSEKARISMA AN EINAI LOGGED IN 
    if current_user.is_authenticated:
        return redirect(url_for("root"))

    ## Create an instance of the Sign Up form

    form = SignupForm()
    

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password2 = form.password2.data

        encrypted_password = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username=username, email=email, password=encrypted_password)
        db.session.add(user)
        db.session.commit()

        flash(f"Ο λογαριασμός για τον χρήστη <b>{username}</b> δημιουργήθηκε με επιτυχία", "success")

        return redirect(url_for('login'))

    return render_template("signup.html", form=form)





## Σελίδα Λογαριασμού Χρήστη με δυνατότητα αλλαγής των στοιχείων του
## Να δοθεί ο σωστός decorator για υποχρεωτικό login

   
    ## Έλεγχος αν έχει δοθεί νέα εικόνα προφίλ, αλλαγή ανάλυσης της εικόνας
    ## και αποθήκευση στον δίσκο του server και στον χρήστη (δηλαδή στη βάση δεδομένων).
    ## Αποθήκευση των υπόλοιπων στοιχείων του χρήστη.
@app.route("/account/", methods=['GET','POST'])
@login_required
def account():

    form = AccountUpdateForm(username = current_user.username, email=current_user.email) ## Αρχικοποίηση φόρμας με προσυμπληρωμένα τα στοιχεία του χρήστη

    if request.method == 'POST' and form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        if form.profile_image.data:
            try:
                image_file = image_save(form.profile_image.data, 'profiles_images', (150,150))
            except:
                abort(415)
            current_user.profile_image = image_file

        db.session.commit()

        flash(f"Ο λογαριασμός του χρήστη <b>{current_user.username}</b> ενημερώθηκε με επιτυχία", "success")
        return redirect(url_for('root'))

    else: 
        return render_template("account_update.html", form=form)

        
    


### Σελίδα Login ###
@app.route("/login/", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("root"))
    
    form = LoginForm()
    ## Αρχικοποίηση φόρμας με προσυμπληρωμένα τα στοιχεία του χρήστη

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data

        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            flash(f"Η είσοδος του χρήστη με email: {email} στη σελίδα μας έγινε με επιτυχία.", "success")
            login_user(user, remember=form.remember_me.data)

            next_link = request.args.get("next")

            return redirect(next_link) if next_link else redirect(url_for("root"))
        else:
            flash("Η είσοδος του χρήστη ήταν ανεπιτυχής, παρακαλούμε δοκιμάστε ξανά με τα σωστά email/password.", "warning")

    return render_template("login.html", form=form)

### Σελίδα Logout ###

@app.route("/logout/")
def logout():
    logout_user()
    flash("Έγινε αποσύνδεση του χρήστη.", "success")
    
    return redirect(url_for("root"))

    ## Αποσύνδεση Χρήστη
    ## Ανακατεύθυνση στην αρχική σελίδα



### Σελίδα Εισαγωγής Νέας Ταινίας ###

## Να δοθεί ο σωστός decorator για τη σελίδα με route 'new_movie'
## καθώς και ο decorator για υποχρεωτικό login

        ## Υλοποίηση της λειτουργίας για ανάκτηση και έλεγχο (validation) των δεδομένων της φόρμας
        
        ## Τα πεδία που πρέπει να έρχονται είναι τα παρακάτω:
        ## title, plot, image, release_year, rating
        ## Το πεδίο image πρέπει να ελέγχεται αν περιέχει εικόνα και αν ναι
        ## να μετατρέπει την ανάλυσή της σε (640, 640) και να την αποθηκεύει στο δίσκο και τη βάση
        ## αν όχι, να αποθηκεύει τα υπόλοιπα δεδομένα και αντί εικόνας να μπαίνει το default movie image 
@app.route("/new_movie/", methods=["GET", "POST"])
@login_required
def new_movie():
    form = NewMovieForm()
    if form.validate_on_submit():
        # Αποθήκευση των υπόλοιπων στοιχείων της ταινίας στη βάση δεδομένων.
        if form.image.data:
            try:
                image_file = image_save(
                    form.image.data, 'movies_images', (640, 640))
            except:
                abort(415)
        else:
            image_file = "default_movie_image.png"
        movie = Movie(
            title=form.title.data,
            plot=form.plot.data,
            image=image_file,
            rating=form.rating.data,
            release_year=form.release_year.data,
            user_id=current_user.id
        )
        
        db.session.add(movie)
        db.session.commit()
        flash(
            f'Η ταινία: <b>{movie.title}</b> καταχωρήθηκε με επιτυχία.', 'success')

        return redirect(url_for('root'))
   
    return render_template("new_movie.html", form=form, page_title="Εισαγωγή Νέας Ταινίας", current_year=current_year)
    
### Πλήρης σελίδα ταινίας ###

## Να δοθεί ο σωστός decorator για τη σελίδα με route 'movie'
## και επιπλέον να δέχεται το id της ταινίας ('movie_id')
@app.route("/movie/<int:movie_id>")
def movie(movie_id):

    ## Ανάκτηση της ταινίας με βάση το movie_id
    
    movie = Movie.query.get_or_404(movie_id)

    ## ή εμφάνιση σελίδας 404 page not found
    return render_template("movie.html", movie=movie)



## ΝΑ ΞΑΝΑΔΩ ΤΟΝ ΚΩΔΙΚΑ ΓΙΑ ΤΟ ΒΥ ΑΥΘΟΡ 


### Ταινίες ανά χρήστη που τις ανέβασε ###

## Να δοθεί ο σωστός decorator για τη σελίδα με route 'movies_by_author'
## και επιπλέον να δέχεται το id του χρήστη ('author_id')
@app.route("/movies_by_author/<int:author_id>")
def movies_by_author(author_id):
    user = User.query.get_or_404(author_id)
    
    page = request.args.get('page', 1, type=int)
    ordering = request.args.get('ordering',1, type=str)

    ## EKANA KAPOIES ALLAGOYLES 

    ## Να προστεθεί σε αυτό το view ότι χρειάζεται για την ταξινόμηση
    ## ανά ημερομηνία εισαγωγής στη βάση, ανά έτος προβολής και ανά rating
    ## με σωστή σελιδοποίηση για την κάθε περίπτωση.
    if ordering == "release_year":
        movies = Movie.query.filter_by(author=user).order_by(Movie.release_year.desc()).paginate(page=page, per_page=5)
        return render_template("movies_by_author.html", movies=movies, author=user, ordering_by=ordering)
    elif ordering == "rating":
        movies = Movie.query.filter_by(author=user).order_by(Movie.rating.desc()).paginate(page=page, per_page=5)
        return render_template("movies_by_author.html", movies=movies, author=user, ordering_by=ordering)

    movies = Movie.query.filter_by(author=user).order_by(Movie.insert_date.desc()).paginate(page=page, per_page=5)
    return render_template("movies_by_author.html", movies=movies, author=user, ordering_by=ordering)

     # Επιστροφή του πίνακα με τις ταινίες του χρήστη
     
### Σελίδα Αλλαγής Στοιχείων Ταινίας ###

## Να δοθεί ο σωστός decorator για τη σελίδα με route 'edit_movie'
## και επιπλέον να δέχεται το id της ταινίας προς αλλαγή ('movie_id')
## και να προστεθεί και ο decorator για υποχρεωτικό login
@app.route("/edit_movie/<int:movie_id>", methods=['GET', 'POST'])
@login_required
def edit_movie(movie_id):

    movie = Movie.query.filter_by(id=movie_id, author=current_user).first_or_404()

    ## Έλεγχος αν βρέθηκε η ταινία
    if movie:
        form = NewMovieForm(title=movie.title, plot=movie.plot, release_year=movie.release_year, rating=movie.rating)
        if form.validate_on_submit():
            movie.title = form.title.data
            movie.plot = form.plot.data
            movie.release_year = form.release_year.data
            movie.rating = form.rating.data
            if form.image.data:
                try:
                    image_file = image_save(form.image.data,'movies_images', (640,640))                
                except:
                    abort(415)
                    
                delete_movie_img = movie.image
                if delete_movie_img != "default_movie_image.png":
                    paths = os.path.join(app.root_path, 'static/images/movies_images/'+delete_movie_img)
                    os.remove(paths)
                movie.image = image_file
            db.session.commit()
            
            flash('Η επεξεργασία της ταινίας ολοκληρώθηκε με επιτυχία', 'success')
            return redirect(url_for('movie', movie_id=movie.id))
        
        
        return render_template("new_movie.html", form=form, movie=movie, page_title="Αλλαγή Ταινίας")
    else:
        flash('Δε βρέθηκε η ταινία', 'info')
        return redirect(url_for("root"))

### Σελίδα Διαγραφής Ταινίας από τον author της ###

## Να δοθεί ο σωστός decorator για τη σελίδα με route 'delete_movie'
## και επιπλέον να δέχεται το id της ταινίας προς αλλαγή ('movie_id')
## και να προστεθεί και ο decorator για υποχρεωτικό login
@app.route("/delete_movie/<int:movie_id>", methods=['GET','POST'])
@login_required
def delete_movie(movie_id):

    movie = Movie.query.filter_by(id=movie_id, author=current_user).first_or_404()

    ## Εάν βρεθεί η ταινία, κάνουμε διαγραφή και εμφανίζουμε flash message επιτυχούς διαγραφής
    ## με ανακατεύθυνση στην αρχική σελίδα
    ## αλλιώς εμφανίζουμε flash message ανεπιτυχούς διαγραφής
    ## με ανακατεύθυνση στην αρχική σελίδα
    if movie:
        db.session.delete(movie)
        db.session.commit()
        
        delete_movie_img = movie.image
        if delete_movie_img != "default_movie_image.png":
            paths = os.path.join(app.root_path, 'static/images/movies_images/'+delete_movie_img)
            os.remove(paths)
        
        flash('Η ταινία διαγράφηκε με επιτυχία', 'success')
        return redirect(url_for('root'))

    flash('Δεν βρέθηκε ταινία', 'warning')
 
    # Ανεξαρτήτως αποτελέσματος, ανακατεύθυνση στην αρχική σελίδα
    return redirect(url_for("root"))
