from celery import Celery

app = Celery('tasks') # defining app name to be used as our flag

@app.task
def add(x, y):
	return x + y

