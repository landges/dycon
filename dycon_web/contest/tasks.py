from dycon_web.celery import app
import zipfile
import os
import subprocess
from .models import *

# @app.task
# def submission(x,y):
# 	return x+y

@app.task
def submission_new(id):
	subm=CompetitionSubmission.objects.get(id=id)
	path_to_zip = subm.inputfile.path
	path_to_csv = subm.competition.golden_file.path
	path_to_py = subm.competition.scoring_program.path
	# path_to_csv = r'C:\Users\HP\Desktop\ans1.csv'
	# path_to_zip = r'C:\Users\HP\Desktop\ans2.zip'

	folder = path_to_zip[:-4]

	zfile = zipfile.ZipFile(path_to_zip, 'r')
	zfile.extractall(folder)
	zfile.close()
	output = subprocess.run(f"python {path_to_py} {path_to_csv} {folder}", shell=True, capture_output=True)
	score = float(output.stdout.decode("utf-8"))
	subm.score=score
	subm.save()
	return score