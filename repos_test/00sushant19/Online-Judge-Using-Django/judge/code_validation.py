from .models import testcase, problem, solution
import os, filecmp, sys, subprocess
from online_judge.settings import BASE_DIR
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
import os, subprocess, sys, time
import docker
from django.template.defaulttags import register
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())



def check_code(submission):
    #print(BASE_DIR)
    with open("sol.cpp", "w") as f:
        f.write(submission.code)
    f.close()
    if sys.platform == 'linux':
        command =['g++ sol.cpp']
    else:
        path_to_code = BASE_DIR
        command = 'g++ ' + os.path.join(path_to_code, 'sol.cpp')

    # Try code compilation
    try:
        subprocess.run(command, capture_output = True, check = True)
    except subprocess.CalledProcessError:
        submission.verdict = "CE"
        submission.save()
        return
    submission.verdict='Compiled'
    use_docker=True
    if(use_docker):
        return code_validation_docker(submission)
    if sys.platform == 'linux':
        command = ['./a.out']
    else:
        command = ['a.exe']

    z=testcase.objects.filter(curr_problem=submission.curr_problem)
    for test in z:
        testinput=test.input
        testoutput=test.output
        try:
            output = subprocess.run(command, capture_output = True, \
                    text = True, input = testinput, check = True, timeout = submission.curr_problem.time_limit)
        except subprocess.TimeoutExpired:
            submission.verdict = "TLE"
            submission.save()
            return

        #Calculate the verdict and save it
        if(checker(output.stdout,testoutput)):
            submission.verdict='AC'
            submission.save()
        else:
            submission.verdict='WA'
            submission.save()
            return


def code_validation_docker(submission):
	client = docker.from_env(timeout=1)
	container = client.containers.run(image='gcc', detach=True, tty=True, mem_limit="512m", mem_swappiness=0, cpu_period=100000, cpu_quota=50000)
	os.system("docker cp sol.cpp {}:/sol.cpp".format(container.short_id))
	container.exec_run("g++ sol.cpp")
	container.exec_run("chmod +x a.out")
	time.sleep(1)
	container.exec_run("touch output.txt")
	try:
		test_cases = testcase.objects.filter(curr_problem=submission.curr_problem)
	except testcase.DoesNotExist:
		raise Http404("Given query not found....")

	for test_case in test_cases:
		f_input = test_case.input
		with open("input_docker.txt", 'w') as f:
			f.write(f_input)
		os.system("docker cp input_docker.txt {}:/input_docker.txt".format(container.short_id))
		# output = container.exec_run(['sh', '-c', './a.out < input_docker.txt > output.txt'])
		try:
			cmd = 'docker exec ' + str(container.id) + ' sh -c "{}"'.format("./a.out < input_docker.txt > output.txt")
			output = subprocess.run(cmd, shell = True, timeout=submission.curr_problem.time_limit)
		except subprocess.TimeoutExpired:
			submission.verdict = "TLE"
			submission.save()
			container.kill()
			container.stop()
			container.remove()
			return
		if output.returncode != 0:
			submission.verdict = "Runtime Error"
			submission.save()
			container.kill()
			container.stop()
			container.remove()
			return
		os.system("docker cp {}:/output.txt output.txt".format(container.short_id))
		docker_output = ""
		with open("output.txt", "r") as f:
			docker_output = f.read()
		if checker(docker_output, test_case.output):
			submission.verdict = "AC"
			submission.save()
		else:
			submission.verdict = "WA"
			submission.save()
			container.kill()
			container.stop()
			container.remove()
			return
		with open("output.txt", "w") as f:
			f.write("")
	container.kill()
	container.stop()
	container.remove()


def checker(output, correct_ouput):
    output = output.split('\n')
    correct_ouput = correct_ouput.split('\n')
    if len(output) != len(correct_ouput):
        return False
    for i in range(len(output)):
        if list(filter(None, output[i].split(' '))) != \
                list(filter(None, correct_ouput[i].split(' '))):
            return False
    return True