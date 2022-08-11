from django.contrib import admin

from .models import problem,solution,testcase

admin.site.register(problem)
admin.site.register(solution)
admin.site.register(testcase)
