from crypt import methods
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, query):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in query]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    # cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS,PATCH"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def all_category():
        query = Category.query.order_by(Category.id).all()

        if len(query) == 0:
            abort(405)
        else:
            categories = {category.id: category.type for category in query}
            return jsonify({
                'success': True,
                'categories': categories,
                'total_categories': len(query)
            })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        categories_query = Category.query.order_by(Category.id).all()

        question_query = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, question_query)

        if len(current_questions) == 0:
            abort(404)

        categories = {
            category.id: category.type for category in categories_query}
        return jsonify({
            'success': True,
            'questions': current_questions,
            'categories': categories,
            'total_questions': len(Question.query.all())
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            del_query = Question.query.filter(
                Question.id == question_id).one_or_none()

            if del_query is None:
                abort(404)

            del_query.delete()

            query = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, query)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })

        except:
            abort(422)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        try:
            question = Question(question=new_question, answer=new_answer,
                                category=new_category, difficulty=new_difficulty)
            question.insert()

            query = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, query)

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        '''
        POST to look up questions based a 'search' term
        '''
        body = request.get_json()

        search_term = body.get('search_term', None)
        if search_term:
            # search term formatted()
            query = Question.query.order_by(Question.id).filter(
                Question.question.ilike(f'%{search_term}%'))
            current_questions = paginate_questions(request, query)

            return jsonify(
                {
                    'success': True,
                    'questions': current_questions,
                    'message': 'search completed',
                    'total_questions': len(query.all())
                }
            )
        # if query is None:
        #     abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions')
    def categorised_questions(category_id):
        query = Question.query.filter(
            Question.category == category_id).order_by(Question.id).all()
        print(len(query))

        current_questions = paginate_questions(request, query)

        return jsonify({
            'success': True,
            'category_question': current_questions,
            'total_questions': len(query)
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def quiz_game():
        ''' 
        Play quiz game: randomize questions 
        '''
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)

            if quiz_category:
                # query quiz list of questions based on user's quiz_category(Question.category == quiz_category['id])
                if quiz_category['id'] != 0:
                    quiz_list = Question.query.filter(
                        Question.category == quiz_category['id']).all()
                else:
                    # all randomized questions quiz list for clicking 'ALL' category
                    quiz_list = Question.query.order_by(Question.id).all()

            # list of available IDs in quiz_list, then generate randmo_num out of IDs using list method random.choice
            available_ids = [question.id for question in quiz_list]
            random_num = random.choice(
                [num for num in available_ids if num not in previous_questions])

            # random question using random_num(as id) that match Question.id field
            question = Question.query.filter(
                Question.id == random_num).one_or_none()
            previous_questions.append(question.id)
            print('count previous_quetions', len(previous_questions))

            return jsonify(
                {
                    'success': True,
                    'question': question.format()
                }
            )

        except:
            abort(404)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405,
                    "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify({'success': False,
                     'error': 500,
                     'message': 'Internal Server error'}),
            500
        )

    return app
