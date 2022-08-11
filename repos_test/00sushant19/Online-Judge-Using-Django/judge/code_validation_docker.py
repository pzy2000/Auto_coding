from judge.models import problem, testcase, solution
import subprocess, os, docker, filecmp, time
from dotenv import load_dotenv, find_dotenv
#from celery.decorators import task

def code_check(submission):
    with open("sol.cpp", "w") as f:
        f.write(submission.code)
    f.close()
    client = docker.from_env()
    #container = client.containers.run(image='gcc', detach=True, tty=True)
    container = client.containers.run(image='gcc', detach=True, tty=True, mem_limit="512m", mem_swappiness=0)
    os.system("docker cp sol.cpp {}:/sol.cpp".format(container.short_id))
    container.exec_run("g++ sol.cpp")
    container.exec_run("chmod +x a.out")
    time.sleep(1)
    container.exec_run("touch output.txt")
    z=testcase.objects.filter(curr_problem=submission.curr_problem)
    for test in z:
        testinput = test.input
        testoutput=test.output
        # with open(f_input,'r') as f1:
        #     cont=f1.read()
        # f1.close()
        with open("input_docker.txt", 'w') as f:
            f.write(testinput)
        f.close()
        os.system("docker cp input_docker.txt {}:/input_docker.txt".format(container.short_id))
        output = container.exec_run(['sh', '-c',  './a.out < input_docker.txt > output.txt'])
        os.system("docker cp {}:/output.txt output.txt".format(container.short_id))

        #dout="S:\study\online_judge\output.txt"
        with open('output.txt', 'r') as f:
            fcont=f.read()
        f.close()
        # with open(f_output, 'r') as f1:
        #     f1cont=f1.read()
        # f1.close()
        if checker(fcont, testoutput):
            submission.verdict = "Accepted"
            submission.save()
        else:
            submission.verdict = "WA"
            submission.save()
            break
        # if(filecmp.cmp(dout,f_output,shallow=False)):
        #     submission.verdict='Accepted'
        #     submission.save()
        # else:
        #     print(i)
        #     submission.verdict='WA'
        #     submission.save()

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

