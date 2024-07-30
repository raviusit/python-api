"""
A Simple Api written in python using Flask and Postgresql provisioned locally or in Cloud
"""

import os, json
import logging
from flask import Flask, jsonify, redirect, render_template, request, send_from_directory, url_for
import psycopg2
from src.response import TodoResponse
from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError

app = Flask(__name__, static_folder='static')

health_status = True

logging.basicConfig(
    format="%(levelname)s: %(message)s", level=os.environ.get("LOG_LEVEL", "INFO")
)
log = logging.getLogger(__name__)

invalid_request = TodoResponse(False, "Invalid request", None).to_json()

@app.errorhandler(404)
def handle_not_found_error(error):
    return TodoResponse(False, "Request not found", None).to_json()


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return TodoResponse(False, response, None).to_json()


@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return TodoResponse(False, jsonify(error.messages), None).to_json()



# Global constants, methods
def db_connect():
    # for sqlite3 connection
    # con = sqlite3.connect('records.db')

    # For Postgresql Connection
    # con = psycopg2.connect(host='localhost', dbname='records', port=5432)
    con = psycopg2.connect(user=os.environ.get("PGUSER"), password=os.environ.get("PGPASSWORD"), host=os.environ.get("PGHOST"), port=5432, database=os.environ.get("PGDATABASE"))
    return con


@app.route('/toggle')
async def toggle():
    try:
        global health_status
        health_status = not health_status
        return jsonify(health_value=health_status)
    except Exception as ex:
        return invalid_request


@app.route('/health')
async def health():
    try:
        if health_status:
            resp = jsonify(health="healthy")
            resp.status_code = 200
        else:
            resp = jsonify(health="unhealthy")
            resp.status_code = 500
        return resp
    except Exception as ex:
        return invalid_request

# Info Page - base URL
@app.route('/')
async def welcome():
    """
    This method just responds to the browser URL
    :return:        the rendered message
    """
    return '''<h1>Welcome to the LeanIX Hiring Assignment <br /><br /></h1>
               <p> Hey, I'm Ravi and I'm very excited to talk to you soon.
               Just a breif about myself - I am an Indian, born and borught up In Delhi (national capital, northern region). I did my schooling, graduated from college and started
               working in Delhi before decided to persue my Master's from University of Twente in the Netherlands.
               Then I moved back to India and relocated to Bangalore (capital of a State called Karnataka down south in India) from where I moved to Berlin in Apr, 2022.
               I have worked for companies like HPE, Honeywell Labs, Oracle, SAP labs and I am currently working with NewStore as an SRE.
               I'm also very keen about learning as a process because I believe there is a lot for me to learn and improve upon.
               When I’m not working, either I am cooking or playing Badminton. I am also an avid listener and intrested in talking to everyone to hear about their life experirences.
               <br />
               <br />
               Endpoints Information for todos API:
               <dd>
               <b>GET /todos </b> → <i> Returns all ToDo </i>
               <br /><b>GET /todos/{id} </b> → <i> Returns a ToDo </i>
               <br /><b>POST /todos </b> → <i> Expects a ToDo (without an id) and returns a ToDo with an id </i>
               <br />
               </dd >
               <br />
               Cheers!!
               <br />
               Ravi <br />
            </p>'''


# /todos - returns you all todos
@app.route('/todos', methods=['GET'])
async def get_todos():
    """
    This function responds to {Base_URL}/todos
    :return:        all todos with id, todo and description
    """
    try:
        con = db_connect()
        cur = con.cursor()
        query = "SELECT * from records"
        cur.execute(query)
        rows = cur.fetchall()
        con.close()
        return jsonify({'Todos': rows})
    except Exception as ex:
        return invalid_request


# GET /todos/{id} → Returns a ToDo
@app.route('/todos/<id>', methods=['GET'])
async def get_todo(id):
    """
    This function responds to {Base_URL}/todos/{id}
    :return:        a specific todo
    """
    try:
        con = db_connect()
        cur = con.cursor()
        query = f"SELECT todo from records WHERE id = {id}"
        cur.execute(query)
        row = cur.fetchone()
        con.close()
        return jsonify({'Todo': ''.join(row)})
    except Exception as ex:
        return invalid_request


@app.route('/todos/', methods=['POST'])
async def add_todo():
    """
    This function responds to {Base_URL}/todos/
    :return:       Expects a ToDo (description is optional) and returns a ToDo with an id
    """
    try:
        con = db_connect()
        cur = con.cursor()
        request_body = request.get_json()

        # validate inputs here
        if len(request_body) > 0:
            if len(request_body) > 2:
                return jsonify({"Error": "Invalid Input, you can only provide a todo and description"})
            else:
                if 'todo' in [key for key in request_body] and not request_body['todo'].isspace() and len(request_body['todo']) > 0:
                    print(request_body['todo'])
                    todo = request_body['todo']
                    description = request_body.get('description', None)
                    if description == None:
                        description = ''
                    else:
                        description = request_body['description']
                    cur.execute("insert into records(todo, description) values(%s, %s)",[todo,description])
                    con.commit()
                    cur.execute("SELECT MAX(id) FROM records")
                    id = cur.fetchone()
                    con.close()
                    response = {'id': ''.join(x for x in str(id) if x.isdigit()), 'todo': todo}
                    return jsonify(response)
                else:
                    return jsonify({"Error": "Invalid Input, Please make sure to provide a valid Todo"})
        else:
            return jsonify({"Error": "No input provided"})
    except Exception as ex:
        return invalid_request


@app.route('/todos/<id>', methods=['PUT', 'PATCH'])
async def mod_record(id):
    """
    This function responds to {Base_URL}/todos/{id}
    :return:       Expects an id and returns a message that particular Todo/description is updated
    """
    try:
        con = db_connect()
        cur = con.cursor()
        query = f'SELECT * FROM records WHERE id = {id}'
        cur.execute(query)
        todo = cur.fetchone()
        todo = todo[1]
        description = todo[2]
        update_todo = request.get_json()

        # validate todo
        if 'todo' in update_todo and not update_todo['todo'].isspace() and len(update_todo['todo']) > 0:
            todo = update_todo['todo']

            # Validate description
            if 'description' in update_todo and not update_todo['description'].isspace() and len(update_todo['description']) > 0:
                description = update_todo['description']

                # run query
                cur.execute('UPDATE records SET todo = %s, description = %s'' WHERE id = %s', [todo, description, id])
                con.commit()
                con.close()
                return jsonify({"Success": f"Todo #{id} is successfully updated!"})
            else:
                return jsonify({"Error": "Invalid Inputs, Please make sure to provide a valid description for update"})
        else:
            return jsonify({"Error": "Invalid Input, Please make sure to provide a valid Todo to update"})
    except Exception as ex:
        return invalid_request
        

if __name__ == "__main__":
    app.run(debug=True, port=5000)
