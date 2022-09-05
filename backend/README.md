# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/categories'`
`curl -X GET http://127.0.0.1:5000/categories`

- General

* Fetches a dictionary which either contains
* on success :

  - the category dictionary which contain id and type in key and value pair.
  - the success which is True
  - and the status code of 200

  # Success Example

  ```json
  {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
  ```

  - on failure :

    - the success set to False.
    - the error code of 404.
    - message which is resource not found

    # Failure Example

    ```json
      {
        "success": False,
        "error code": 404,
        "message": " resource not found"
      }
    ```

- Request Arguments: None

`GET /questions`
`curl -X GET http://127.0.0.1:5000/questions?page=1`

- General:

* Fetches a paginated set (maximum of 10) of questions, a total number of questions, all categories and current category string.
* Request Arguments: `page` - integer

- Response:
- Status: 200

* Returns:

  - On success
    An object with 10 questions a page, total questions-int, object including all categories, and current category for each question-string.

    # Success Example

    ```json
    {
      "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
      },
      "questions": [
        {
          "answer": "Apollo 13",
          "category": 5,
          "difficulty": 4,
          "id": 2,
          "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
          "answer": "Tom Cruise",
          "category": 5,
          "difficulty": 4,
          "id": 4,
          "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
          "answer": "Maya Angelou",
          "category": 4,
          "difficulty": 2,
          "id": 5,
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
          "answer": "Edward Scissorhands",
          "category": 5,
          "difficulty": 3,
          "id": 6,
          "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
          "answer": "Muhammad Ali",
          "category": 4,
          "difficulty": 1,
          "id": 9,
          "question": "What boxer's original name is Cassius Clay?"
        },
        {
          "answer": "Brazil",
          "category": 6,
          "difficulty": 3,
          "id": 10,
          "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
          "answer": "Uruguay",
          "category": 6,
          "difficulty": 4,
          "id": 11,
          "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
          "answer": "George Washington Carver",
          "category": 4,
          "difficulty": 2,
          "id": 12,
          "question": "Who invented Peanut Butter?"
        },
        {
          "answer": "Lake Victoria",
          "category": 3,
          "difficulty": 2,
          "id": 13,
          "question": "What is the largest lake in Africa?"
        },
        {
          "answer": "The Palace of Versailles",
          "category": 3,
          "difficulty": 3,
          "id": 14,
          "question": "In which royal palace would you find the Hall of Mirrors?"
        }
      ],
      "success": true,
      "total_questions": 20
    }
    ```

  - On failure:

    - the success set to False.
    - the error code of 404.
    - message which is resource not found

    # Failure Example

    ```json
      {
        "success": False,
        "error code": 404,
        "message": " resource not found"
      }
    ```

  `POST /questions`
  `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question":"When was REACT first released", "answer":"look up in Google", "difficulty":"1", "category":"1"}'`

  - General
    - This create a question in the database with the JSON body attached to the endpoint

  * Request arguements: `question`, `answer` - string, `difficulty`, `category` - integer

  - Response:

    - On success:
      An object is returned, example below

      # Success Example

      ```json
      {
        "success": True,
        "created": question.id,
        "questions": current_questions,
        "total_questions": len(Question.query.all())
      }
      ```

    - On failure:
      An object is returned, example below
      # Failure Example
      ```json
      {
        "success": False,
        "error": 422,
        "message": "unprocessable"
      }
      ```

  `GET /categories/${id}/questions`
  `curl -X GET http://127.0.0.1:5000/categories/1/questions`

  - General:
    - Fetches questions for a cateogry specified by id request argument

  * Request Arguments: category `id` - integer

  * Response:

    - On success:
      An object is returned, example below

      # Success Example

      ```json
      {
        "current_category": "Science",
        "questions": [
          {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
          },
          {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
          },
          {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
          },
          {
            "answer": "look up in Google",
            "category": 1,
            "difficulty": 1,
            "id": 24,
            "question": "When was REACT first released"
          }
        ],
        "success": true,
        "total_questions": 4
      }
      ```

    - On failure:
      An object is returned, example below

      # Failure Example

      ```json
      {
        "success": False,
        "error": 422,
        "message": "unprocessable"
      }
      ```

  `DELETE '/questions/${id}'`
  `curl -X DELETE http://127.0.0.1:5000/questions/27`

  - General:

    - Deletes a specified question using the id of the question

  - Request Arguments: `id` - integer
  - Response:

    - On success:
      An object is returned, example below

      # Success Example

      ```json
      {
        "success": True,
        "deleted": question_id,
        "questions": current_questions,
        "total_questions": len(Question.query.all())
      }
      ```

    - On failure:
      An object is returned, example below

      # Failure Example

      ```json
      {
        "success": True,
        "deleted": question_id,
        "questions": current_questions,
        "total_questions": len(Question.query.all())
      }
      ```

  `POST '/quizzes'`
  `curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"quiz_category": {"id":"1"}, "previous_questions": []}'`

  - General:

    - Sends a post request in order to get the next question
    - Request Body: args - quiz_category-`id` integer, or string, `previous_questions`- list. Below is a example of the request body.

    ```json
    {
      "quiz_category": { "id": "1" },
      "previous_questions": []
    }
    ```

  - Response:

    - On success:
      An object is returned, example below

      # Success Example

      ```json
      {
        "question": {
          "answer": "Blood",
          "category": 1,
          "difficulty": 4,
          "id": 22,
          "question": "Hematology is a branch of medicine involving the study of what?"
        },
        "success": true
      }
      ```

    - On failure:

      - the success set to False.
      - the error code of 404.
      - message which is resource not found

      # Failure Example

      ```json
        {
          "success": False,
          "error code": 404,
          "message": " resource not found"
        }
      ```

  `POST '/questions/search'`
  `curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d '{"searchTerm": "title"}'`

  - General:
    - Sends a post request in order to search for a specific question by search term: `searchTerm` - string

  * Request Body:

  ```json
  {
    "searchTerm": "title"
  }
  ```

  - Response:

    - On success:
      An object is returned, example below

      # Success Example

      ```json
      {
        "questions": [
          {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
          },
          {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
          }
        ],
        "success": true,
        "total_questions": 2
      }
      ```

      # Failure Example

      ```json
        {
          "success": False,
          "error code": 404,
          "message": " resource not found"
        }
      ```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
