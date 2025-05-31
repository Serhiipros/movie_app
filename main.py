from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager, UserMixin, login_required
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__,static_url_path="/static")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SECRET_KEY"] = "flash srever for movies "

DEBUG=os.getenv('DEBUG')

class Base(DeclarativeBase):
  pass



db = SQLAlchemy(model_class=Base)
db.init_app(app)




login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "sign"


from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True,  nullable=False)
    comments = db.relationship("Comment", back_populates="user", lazy=True)
    favourite_movies = db.relationship("FavouriteMovies", back_populates="user", lazy=True)



class Comment(db.Model):
    __tablename__ = "coments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(350), unique=False,  nullable=False)
    movie_id=db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship("User", back_populates="comments")



class FavouriteMovies(db.Model):
    __tablename__ = "favourite_movies"
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="favourite_movies")
    created_at = db.Column(db.DateTime, default=datetime.now)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


with app.app_context():
    db.create_all()

users=[]






@app.route("/")

def index():
    from data_file import get_popular_movies ,get_toprated_movies, get_upcoming_movies
    from flask_login import current_user

    toprated_movies = get_toprated_movies()
    popular_movies = get_popular_movies()
    upcoming_movies = get_upcoming_movies()

    fav_movies = []
    if current_user.is_authenticated:
        fav_movies = [movie.movie_id for movie in current_user.favourite_movies]
        print("User favourite movies: ", fav_movies)

    return render_template("index_2.html",
                            toprated_movies=toprated_movies,
                            popular_movies=popular_movies,
                            upcoming_movies=upcoming_movies,
                            fav_movies=fav_movies)


@app.route("/movies/<movies_type>")
def movies_list(movies_type:str):
    from data_file import get_popular_movies, get_toprated_movies, get_upcoming_movies
    from flask import request
    from flask_login import current_user
    page=request.args.get("page", 1)
    
    
    
    if movies_type=="popular":
        movies=get_popular_movies(page)
    elif movies_type=="toprated":
        movies=get_toprated_movies()
    elif movies_type=="upcoming":
        movies=get_upcoming_movies()
    else:
        movies=get_popular_movies()


    fav_movies = []
    if current_user.is_authenticated:
        fav_movies = [movie.movie_id for movie in current_user.favourite_movies]
        print("User favourite movies: ", fav_movies)

    return render_template("movies_list.html", movies=movies, fav_movies=fav_movies)


@app.route("/movies/<movie_id>/details",methods=["GET", "POST"])
def movie_details(movie_id):
    from data_file import get_movies_details, get_images_detail, get_movie_videos, get_recomendations_films
    from flask import request
    from flask_login import current_user
    data=get_movies_details(movie_id)
    images=get_images_detail(movie_id)
    videos=get_movie_videos(movie_id)
    recomend=get_recomendations_films(movie_id)
    filtered_videos = [
        video
        for video in videos
        if video.get("type", "") == "Trailer" and video.get("official", False)
    ]
    video_key = filtered_videos[0].get("key")


    if request.method=="POST":
        content = request.form.get("content")
        print("Comment content: ", content)

        comment=Comment(content=content, movie_id=movie_id,user=current_user)
        db.session.add(comment)
        db.session.commit()

    comments=Comment.query.filter_by(movie_id=movie_id).all()
    fav_movies = []
    if current_user.is_authenticated:
        fav_movies = [movie.movie_id for movie in current_user.favourite_movies]
        print("User favourite movies: ", fav_movies)

    return render_template("details.html", 
                            movie=data,
                            images=images,
                            video_key=video_key,
                            recomend=recomend,
                            comments=comments,fav_movies=fav_movies)
    # return images

@app.route("/movies/search")
def search_movies():
    from flask import request
    from data_file import search_movies_db
    query = request.args.get("query", "")
    print("Search query:", query)
    movies = search_movies_db(query)
    return render_template("movies_list.html", movies=movies)


@app.route("/comments/<comment_id>/delete")
@login_required
def delete_comment(comment_id):
    from flask import redirect, request

    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        return "Comment not found. Try again!", 400

    db.session.delete(comment)
    db.session.commit()

    return redirect(request.referrer or "/")



@app.route("/movies/like/<movie_id>")
@login_required
def toggle_favourite_movie(movie_id):
    from flask_login import current_user
    from flask import redirect, request

    fav_movie = FavouriteMovies.query.filter_by(
        movie_id=movie_id, user=current_user
    ).first()
    if fav_movie:
        db.session.delete(fav_movie)
    else:
        fav_movie = FavouriteMovies(movie_id=movie_id, user=current_user)
        db.session.add(fav_movie)

    db.session.commit()
    return redirect(request.referrer or "/")



@app.route("/registration", methods=["GET", "POST"])
def registration():
    from flask import request, redirect

    if request.method == "POST":
        username=request.form.get("username")
        password=request.form.get("password")
        email=request.form.get("email")


        if len(username.strip()) < 3:
            return render_template(
                "registration.html",error="Username must be at least 3 characters long"
            )


        if len(password.strip()) < 8:
            return render_template(
                "registration.html",error="Password must be at least 8 characters long"
            )

        if User.query.filter_by(username=username).first():
            return render_template(
                "registration.html", error="Username already exists"
            )
        
        if User.query.filter_by(email=email).first():
            return render_template(
                "registration.html", error="Email already exists"
            )




        user=User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()

        return redirect("/sign")


    return render_template("registration.html")

@app.route("/sign", methods=["GET", "POST"])
def sign():
    from flask import request, redirect
    from flask_login import login_user
    if request.method == "POST":
        username=request.form.get("username")
        password=request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if not user:
            return render_template("sign.html", error="User not found")
        


    
        if user.password != password:
            return render_template("sign.html",error="Incorect password")
    
        login_user(user)


        return redirect("/")


    return render_template("sign.html")

@app.route("/profile")
@login_required     
def profile():
    from flask_login import current_user
    from data_file import get_movies_details
    favourite_movies=[
        get_movies_details(m.movie_id) for m in current_user.favourite_movies
    ]
    return render_template("profile.html", favourite_movie=favourite_movies)




@app.route("/logout")
def logout():
    from flask import  redirect
    from flask_login import logout_user
    logout_user()
    return redirect('/sign')


#app.run(debug=DEBUG)
