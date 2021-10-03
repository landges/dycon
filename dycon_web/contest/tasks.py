from dycon_web.celery import app

@app.task
def submission(x,y):
	return x+y