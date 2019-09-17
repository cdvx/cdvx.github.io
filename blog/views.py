from flask import Blueprint, jsonify, request, render_template, g, session, redirect, url_for
from .models import Article, ArticleSchema
from users.models import User
import random
from datetime import datetime
import string

article = Blueprint('article', __name__)

@article.route("/api/v1/articles/<int:article_id>")
def get_article(article_id):
    article = Article.get_article(id=article_id).first()
    if article:
        article_schema = ArticleSchema()
        return jsonify(
            {'article': article_schema.dump(article).data}), 200
    return jsonify({'error': 'Invalid article Id'}), 400


@article.route("/api/v1/articles", methods=['POST', 'GET'])
def articles():
    if request.method == 'GET':
        articles = Article.query.all()
        get_author = lambda id : User.get(id)
        articles_schema = ArticleSchema(many=True)
        articles = articles_schema.dump(articles).data
        get_date = lambda date_time_obj: date_time_obj.timetuple()[:3]
        
        turn_to_in = lambda t: (int(i) for i in t)

        article = [article.update({
                   'author': get_author(article['author']).first(),
                   'date':  (datetime.now() - datetime(*turn_to_in(get_date(datetime.strptime(article['created_at'][:10], '%Y-%m-%d'))))).days })\
                   for article in articles]
        return render_template('articles.html', articles=articles)
    elif request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 400
        if not session['username'] or not g.user:
            return redirect(url_for('user_app.login')), 403

        get_author = lambda username: User.get_user(username=username).first()

        title = request.json.get('title')
        body = request.json.get('body')
        author = get_author(session['username'])
        image = request.json.get('image')

        try:
            # check that article with similar body exists
            check_article_exists(body)

            article = Article(title=title, body=body, author=author, image=image)
            article.save()
            return render_template('article.html', article=article), 201
        except AssertionError as exception_message:
            return jsonify(error=f"{exception_message}."), 400

def check_article_exists(body):
    try:
        if Article.get_article(body=body).first():
            raise AssertionError('Body already exists!')
    except AttributeError:
        pass


@article.route("/api/v1/articles/<int:article_id>", methods=['PUT', 'PATCH'])
def edit_article(article_id):
    if request.method == 'GET':
        return redirect(url_for('articles.html', login='login'))
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400
    if not session['username'] or not g.user:
            return redirect(url_for('user_app.login')), 403
    try:
        # check that article exists
        article = Article.get_article(article_id)

        if not article:
            return jsonify({"errorf": f"Article {article_id} does not exist!"}), 400
    except AssertionError as exception_message:
        return jsonify(error=f"{exception_message}."), 400

    title = request.json.get('title')
    body = request.json.get('body')
    author = request.json.get('author')
    image = request.json.get('image')

    put = title and body and image
    body_title = title and body
    title_image = title and image
    body_image = body and image
    one_  = body or title or image 
    all_ = body and title and image
    patch = title_image or body_image or body_title or one_
    put = all_

    if put:
        article = Article.get_article(id=article_id).first()
        article.update_(**article)
        return render_template('article.html', article=article
        ), 204

    elif patch:
        article = Article.get_article(id=article_id).first()
        article.update_(**article)
        return render_template('article.html', article=article
        ), 204
