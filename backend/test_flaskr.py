import os
from traceback import print_tb
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import load_dotenv


# load .env file in backend dir using python-dotenv lib
path = os.path.dirname(os.path.dirname(__file__))
env_file = os.path.join(path, ".env")
load_dotenv(env_file)


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = os.getenv('DB_TEST')
        self.db_host = os.getenv('DB_HOST')
        self.db_password = os.getenv('DB_PASS')
        self.db_user = os.getenv('DB_USER')
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(self.db_user, self.db_password, self.db_host, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # test data for creationg a new question
        self.test_question = {
            'question': "what is the capital of Nigeria",
            'answer': "Abuja",
            'difficulty': 1,
            'category': 1
        }

        # test data for generating a random question
        self.random_question = {'previous_questions': [], 'quiz_category': {'id': 1}}

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    DONE
    Write at least one test for each test for successful operation and for expected errors.
    """

    # test for successful question creation
    def test_200_add_question(self):
        '''
        Test for successful question creation
        '''
        res = self.client().post('/questions', json=self.test_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # test for unsuccessful question creation
    def test_405_add_question(self):
        '''
        Test for unsuccessful question creation
        '''
        res = self.client().post('/questions/2', json=self.test_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # test for successful retrival of categories
    def test_200_retrieve_categories(self):
        '''
        Test for successful retrival of categories
        '''
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    # test for unsuccessful retrival of categories
    def test_404_retrieve_categories(self):
        '''
        Test for unsuccessful retrival of categories
        '''
        res = self.client().get('/categories/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # test for successful paginated questions
    def test_200_retrieve_paginated_questions(self):
        '''
        Test for successful paginated questions
        '''
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    # test for unsuccessful paginated questions
    def test_200_retrieve_paginated_questions(self):
        '''
        Test for unsuccessful paginated questions
        '''
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # test for successful delete question endpoint
    def test_200_delete_question(self):
        '''
        Test for successful delete question endpoint
        '''
        res = self.client().delete('/questions/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 3)

    # test for unsuccessful delete question endpoint
    def test_422_failed_delete_question(self):
        '''
        Test for unsuccessful delete question endpoint
        '''
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    # test on search endpoints
    # successful search with questions endpoint
    def test_200_search_questions_results(self):
        '''
        Test for successful search with questions endpoint
        '''
        res = self.client().post('/questions/search', json={"search_term": "Nigeria"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'search completed')
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 14)

    # successful search without questions endpoint
    def test_200_no_search_results(self):
        '''
        Test for successful search without questions endpoint
        '''
        res = self.client().post('/questions/search', json={"search_term": "GTA"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'search completed')
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)
    
    # unsuccessful search questions endpoint
    def test_404_invalid_search(self):
        '''
        Test for unsuccessful search with questions endpoint
        '''
        res = self.client().post('/questions/search/1', json={"search_term": "GTA"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['error'], 404)


    # test on quizzes endpoint
    # successful one category quiz endpoint
    def test_200_quiz(self):
        '''
        Quiz test for Categorised randomized questions
        '''
        # '/quizzes'
        res = self.client().post('/quizzes', json=self.random_question)
        data = json.loads(res.data)

        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    # successful all category quiz endpoint
    def test_200_quiz_all(self):
        '''
        Test for all not categorised random question
        '''
        res = self.client().post('/quizzes', json={"quiz_category": {'id': 0}, "previous_questions": []})
        # = {'previous_questions': [], 'quiz_category': {'id': 0}}
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    # unsuccessful quiz endpoint
    def test_404_failed_quizz(self):
        '''
        Test for out_of_range_category random question
        '''
        res = self.client().post('/quizzes', json={"quiz_category": {'id': 1000},"previous_questions": []})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
