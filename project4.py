from flask import Flask, jsonify, request, abort, make_response, url_for

app = Flask(__name__)

tasks = [ 
{
'id':1,
'name': u'Deep',
'occupation': u'scientist, enginner, programmer',
'done': False
},
{
'id': 2,
'name': u'Marina',
'occupation': u'Need to pick a job',
'done': False
},
]  


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task



#@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
#def get_tasks(task_id):
#	task = [task for task in tasks if task['id'] == task_id]
#	if len(task)== 0:
#	abort(404) 
#	return jsonify({'tasks': tasks[0]})


# @app.route('/todo/api/v1.0/tasks', methods=['GET'])
# def get_tasks():
#  return jsonify({'tasks': [make_public_task(task) for task in tasks]})




@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
if not request.json or not 'name' in request.json:
abort(400)
task = {
'id': tasks[-1]['id'] + 1,
'name': request.json['name'],
'occupation': request.json.get('occupation', ""),
'done': False
}
tasks.append(task)
return jsonify({'task': task}), 201 

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != unicode:
        abort(400)
    if 'occupation' in request.json and type(request.json['occupation']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['name'] = request.json.get('name', task[0]['name'])
    task[0]['occupation'] = request.json.get('occupation', task[0]['occupation'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})
 



@app.errorhandler(404)
def not_found(error):
return make_response(jsonify({'error': 'Not found'}),404) 

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': tasks})

if __name__ == '__main__':
        app.run(debug=True)