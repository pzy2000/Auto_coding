from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import problem,solution
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .our_forms import code_form, problem_form, testcase_form
from .code_validation import check_code


def display_problems(request):
    context={
        'problems': problem.objects.all()
    }
    return render (request, 'problem_page.html',context)

@login_required(login_url='user_login')
def problem_detail(request, prob_id):
    obj=get_object_or_404(problem, id = prob_id)
    if request.method == 'POST':
        form=code_form(request.POST)
        if(form.is_valid()):
            sub=form.save()
            sub.curr_problem=obj
            sub.submitter = request.user.username
            #sub.submitter = coder.objects.get(user = request.user)
            sub.save()
            check_code(sub)
        return redirect('past_submissions',prob_id)
    else:
        form=code_form()
        context = {
            'problem': problem.objects.get(id=prob_id),
            'form': form,
        }
        template='detail_problem.html'
        return  render (request, template, context)

@login_required(login_url='user_login')
def submit(request,prob_id):
    obj=problem.objects.get(id=prob_id)
    qs=solution.objects.filter(curr_problem=obj).filter(submitter=request.user.username).order_by('-id')
    if(len(qs)==0):
        template='no_submission.html'
        return render(request,template)
    context= {
        'submissions': qs
    }
    template='submission.html'
    return render(request,template,context)

@login_required(login_url='user_login')
def show_code(request,prob_id,submission_id):
    obj=solution.objects.get(id=submission_id)
    context= {
        'obj': obj
    }
    template='display_code.html'
    return render(request,template,context)

@staff_member_required
def add_problem(request):
    if(request.method=='POST'):
        form=problem_form(request.POST)
        if(form.is_valid()):
            sub=form.save()
        return redirect ('add_testcase',sub.id)
    else:
        form=problem_form()
        context= {
            'form': form
        }
        template='add_prob.html'
        return render(request,template,context)

@staff_member_required
def add_testcase(request,prob_id):
    if(request.method=='POST'):
        obj=get_object_or_404(problem, id = prob_id)
        form=testcase_form(request.POST)
        if(form.is_valid()):
            sub=form.save()
            sub.curr_problem=obj
            sub.save()
        return redirect('problem_page')
    else:
        form=testcase_form()
        context= {
            'form': form
        }
        template = 'add_test.html'
        return render(request,template,context)

@staff_member_required
def del_prob(request, prob_id):
    obj=problem.objects.get(id=prob_id)
    obj.delete()
    return redirect('problem_page')



