from flask import Flask, jsonify, abort, make_response, request
app=Flask(__name__)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error':'Not Found'}),404)

tasks = [
	{
		'id':1,
		'title':'Buy Groceries',
		'description':'Milk, Cheese, Pizza, Fruit, Tylenol',
		'done':False
	},
	{
		'id':2,
		'title':'Learn Python',
		'description':'Need to find a good Python tutorial on the web',
		'done':False
	}
]

@app.route('/')
def index():
	return "Hello World!"

@app.route('/api/tasks',methods=['GET'])
def get_tasks():
	return jsonify({'tasks':tasks})

@app.route('/api/tasks/<int:task_id>',methods=['GET'])
def get_task(task_id):
	task=[task for task in tasks if task['id']==task_id]
	if len(task)==0:
		abort(404)
	return jsonify({'tasks':task[0]})

@app.route('/api/tasks',methods=['POST'])
def create_task():
	if not request.json or 'title' not in request.json:
		abort(404)
	task={
		'id':tasks[-1]['id']+1 if len(tasks)>0 else 1,
		'title': request.json['title'],
		'description': request.json.get('description',""),
		'done':False
	}
	tasks.append(task)
	return jsonify({'task': task}), 201

@app.route('/api/tasks/<int:task_id>',methods=['DELETE'])
def delete_task(task_id):
	task=[task for task in tasks if task['id']==task_id]
	if len(task)==0:
		abort(404)
	tasks.remove(task[0])
	return jsonify({'result':True})

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
	task=[task for task in tasks if task['id']==task_id]
	if len(task)==0:
		abort(404)
	if 'title' in request.json:
		task[0]['title']=request.json.get('title',task[0]['title'])
	if 'description' in request.json:
		task[0]['description']=request.json.get('title',task[0]['title'])
	if 'done' in request.json:
		task[0]['done']=request.json.get('title',task[0]['title'])
	return jsonify({'task':task[0]})

if __name__ == '__main__':
	app.run(debug=True)