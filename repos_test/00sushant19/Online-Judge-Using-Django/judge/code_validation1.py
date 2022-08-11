
from .models import testcase
import os, filecmp, sys, subprocess
from online_judge.settings import BASE_DIR

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
        print("Compilation Error")
        submission.verdict = "Compilation Error"
        submission.save()
        return
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
            submission.verdict='Accepted'
            submission.save()
        else:
            submission.verdict='WA'
            submission.save()
            return

        

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

