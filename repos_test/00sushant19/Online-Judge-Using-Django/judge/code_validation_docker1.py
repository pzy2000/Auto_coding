import subprocess as sp
from time import time
import os

import docker
from docker.models.containers import Container
from .models import testcase

from . import constants as _
from .constants import HOST_PATH

__client = docker.from_env()


def code_check(submission):
    '''
    Tests `submission` against the gcc judge
    '''
    filename = 'submit_code'
    test=testcase.objects.get(curr_problem=submission.curr_problem)
    return __chief_judge(
        submission=submission,
        testcases=test,
        ext='cpp',
        compile='gcc -o {} {}.cpp'.format(filename, filename),
        run='./{}'.format(filename),
        clear='rm {} {}.c'.format(filename, filename),
        cont_name=_.Judge.GCCCONT,
        docker_image=_.Judge.GCCIMG,
    )



def __chief_judge(submission, testcases, ext, clear, run, cont_name, docker_image, compile=None):
    #filename = 'submit_code' + '.' + ext
    #hostfile = '/'+filename

    file = open('submit_code.cpp', 'w+')
    file.write(submission.code)
    file.close()

    container: docker.models.containers.Container = None
    try:
        container: Container = __client.containers.get(cont_name)
        if(container.status != 'running'):
            container.start()
    except docker.errors.NotFound:
        container = __client.containers.run(docker_image,
                                            stdin_open=True,
                                            detach=True,
                                            tty=True,
                                            name=cont_name)

    #__copy_to_container(filename, filename, container)
    os.system("docker cp submit_code.cpp {}:/submit_code.cpp".format(container.short_id))
    maxtime = 0.0
    verdict = submission.verdict='Accepted'
    submission.save()

    # def close():
    #     sp.run(['rm', hostfile])
    #     sp.run('docker exec ' + cont_name + ' ' + clear, shell=True)
    #     return {'verdict': verdict, 'time': maxtime}

    if compile:
        cp = sp.run('docker exec ' + cont_name + ' ' + compile, shell=True)
        print(cp.returncode)
        print(cp.returncode)
        if cp.returncode != 0:
            submission.verdict = 'CE'
            submission.save()
            return #close()

    print(1234)
    input=testcases.input
    output=testcases.output
    input=input.split(',')
    output1=output.split(',')
    n=len(input)
    for i in range(n):
        start = time()
        with open(input[i],'w+') as f:
            given_intput=f.read()
        f.close()
        #with open()
        try:
            cp = sp.run('docker exec ' + cont_name + ' sh -c \'echo "{}" | {}\''.format(given_intput, run),
                        shell=True,
                        capture_output=True,
                        timeout=1000)
        except sp.TimeoutExpired:
            maxtime = (time() - start) * 1000
            submission.verdict = 'TE'
            break

        maxtime = max(maxtime, (time() - start) * 1000)

        if cp.returncode != 0:
            submission.verdict = 'RE'
            break

        useroutput = cp.stdout.decode().strip().rstrip("\n").strip()
        with open(output1[i], 'w+') as f:
            given_output=f.read()
        f.close()
        if not useroutput == given_output:
            submission.verdict = 'WA'
            break

    return #close()


def __copy_to_container(src, dst, container):
    src = _.HOST_PATH + src
    dst = _.CONT_PATH + dst
    sp.run(['docker', 'cp', src, container.id+':'+dst])
