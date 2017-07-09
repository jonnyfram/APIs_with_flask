import json

from flask import request, Response, url_for
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from posts import app
from .database import session

@app.route("/api/posts", methods=["GET"])
@decorators.accept("application/json")
def posts_get():
    """ Get a list of posts """
    title_like = request.args.get("title_like")
    body_like = request.args.get("body_like")
    # Get the posts from the database
    posts = session.query(models.Post)
    
    if title_like:
        posts = posts.filter(models.Post.title.contains(title_like))
    posts = posts.order_by(models.Post.id)
    
    if body_like:
        posts = posts.filter(models.Post.body.contains(body_like))
    posts = posts.order_by(models.Post.id)
    
    # Convert the posts to JSON and return a response
    data = json.dumps([post.as_dictionary() for post in posts])
    return Response(data, 200, mimetype="application/json")
    
@app.route("/api/posts/<int:id>", methods=["GET"])
def post_get(id=0):
    """Get a single post"""
    #get post from DB
    post = session.query(models.Post).get(id)
    
    #Check if post exists:
    #if not return 404 + message
    if not post:
        message= "Could not find post with id{}".format(id)
        data = json.dumps({"message":message})
        return Response(data, 404, mimetype="application/json")
        
    #return post as JSON
    data = json.dumps(post.as_dictionary())
    return Response(data, 200, mimetype="applications/json")

@app.route("/api/posts/<int:id>", methods=["GET"])
def post_delete():
    """Delete a single post"""
    #get post from DB
    post = session.query(models.Post).get(id)
    
    #Check if post exists:
    #if not return 404 + message
    if not post:
        message= "Could not find post with id{}".format(id)
        data = json.dumps({"message":message})
        return Response(data, 404, mimetype="application/json")
        
    session.delete(post)
    session.commit()
    
    message= "Deleted post id{}".format(id)
    data = json.dumps({"message":message})
    return Response(data, 200, mimetype="application/json")