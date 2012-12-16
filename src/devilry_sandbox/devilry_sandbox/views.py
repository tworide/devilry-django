from django.views.generic import TemplateView, View
from django.shortcuts import redirect
from django.db import transaction

from .sandbox import Sandbox


class CreateSubjectIntroView(TemplateView):
    template_name = 'devilry_sandbox/createsubject.django.html'


class CreateSubjectCreateView(View):
    def post(self, request):
        with transaction.commit_on_success():
            sandbox = Sandbox()
            testuser = sandbox.create_user('testuser', 'Test User')
            sandbox.subject.admins.add(testuser)
            sandbox.create_period('approx-spring2013', 'Spring 2013')
            return redirect('devilry-sandbox-createsubject-success',
                unique_number=str(sandbox.unique_number))


class CreateSubjectSuccessView(TemplateView):
    template_name = 'devilry_sandbox/createsubject.django.html'
    def get_context_data(self, **kwargs):
        context = super(CreateSubjectSuccessView, self).get_context_data(**kwargs)
        context['success'] = True
        context['unique_number'] = self.kwargs['unique_number']
        return context