from dycon_web.celery import app
import zipfile
import os
import subprocess
from .models import *
import shutil
from django.core.files.base import ContentFile, File

# @app.task
# def submission(x,y):
# 	return x+y

@app.task
def submission_new(id):
	subm=CompetitionSubmission.objects.get(id=id)
	subm.status = "running"
	subm.save()
	docker_name=subm.competition.ingestion_program_docker_image
	path_to_subm = subm.inputfile.path
	path_to_valid = subm.competition.ingestion_program.path
	

	folder = path_to_subm[:-4]+'/'

	zfile = zipfile.ZipFile(path_to_subm, 'r')
	zfile.extractall(folder)
	zfile.close()
	zfile = zipfile.ZipFile(path_to_valid, 'r')
	zfile.extractall(folder)
	zfile.close()
	output = subprocess.check_output(f'docker run --rm -v {folder}:/code {docker_name}'.split(' '))
	score = 0.0
	try:
		score = float(output.decode("utf-8"))
		subm.status = "finished"
	except:
		score = 0.0
		subm.status = "failed"
	subm.output_file.save('errors_output.txt',ContentFile(output.decode("utf-8")))
	subm.score=score
	subm.save()
	return score

# run=subprocess.run(["docker", "run", "--rm", "-d", "--name", "valid6", "-d", "valid"])
# out = a=subprocess.check_output(["docker", "logs", "valid6"])
# copy_and_run = docker run --rm -v /tmp/src:/code --name val44 val ./ans2
#subprocess.run('docker run --rm -v /tmp/src:/code --name val44 val ./ans2'.split(' '))
# subprocess.check_output('docker run --rm -v /tmp/src:/code --name val46 val ./ans2'.split(' '))

# @app.task
# def load_contest(id):
# 	comp = Competition.objects.get(id=id)
# 	path_dockerfile = comp.docker_config.path
# 	path_dockerfile_folder = path_dockerfile[:-4]+'/'
# 	zfile = zipfile.ZipFile(path_dockerfile, 'r')
# 	zfile.extractall(path_dockerfile_folder)
# 	zfile.close()
# 	os.chdir(path_dockerfile_folder)
# 	subprocess.run(["docker","build",f"--file={name_config}","-t",comp.ingestion_program_docker_image, "."])
# 	comp.published=True
# 	comp.save()


@app.task
def load_contest(id):
	comp = Competition.objects.get(id=id)
	path_dockerfile = comp.docker_config.path
	path_dockerfile = '/'.join(path_dockerfile.split('/')[:-1])+'/'
	os.chdir(path_dockerfile)
	os.mkdir(f'build{comp.id}')
	shutil.copy(comp.docker_config.path,f'{path_dockerfile}/build{comp.id}/')
	shutil.copy(comp.requirements.path,f'{path_dockerfile}/build{comp.id}/')
	os.chdir(f'build{comp.id}')
	name_config=comp.docker_config.path.split('/')[-1]
	subprocess.run(["docker","build",f"--file={name_config}","-t",comp.ingestion_program_docker_image, "."])
	comp.published=True
	comp.save()



@app.task
def update_docker_image(name):
	subprocess.run(["docker","build","-t",name, "."])
