from django.shortcuts import render
from django.views.generic import (TemplateView, ListView, DetailView,
                                  FormView, CreateView, DeleteView, UpdateView)
from .models import Standard, Subject, Lesson
from .forms import LessonForm, CommentForm, ReplyForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
# Create your views here.

class StandardListView(ListView):
    context_object_name = 'standards'
    model = Standard
    template_name = 'curriculum/standard_list_view.html'


class SubjectListView(DetailView):
    context_object_name = 'standard'
    model = Standard
    template_name = 'curriculum/subject_list_view.html'


class LessonListView(DetailView):
    context_object_name = 'subjects'
    model = Subject
    template_name = 'curriculum/lesson_list_view.html'

class LessonDetailView(DetailView, FormView):
    context_object_name = 'lessons'
    model = Lesson
    template_name = 'curriculum/lesson_detail_view.html'
    form_class = CommentForm
    second_form_class = ReplyForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.form_class
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'
        
        form = self.get_form(form_class)

        if form_name == 'form' and form.is_valid():
            print('Comment Form is returned')
            return self.form_valid(form)
        elif form_name == 'form2' and form.is_valid():
            print('reply form is returned')
            return self.form2_valid(form)
    
    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.standard
        subject = self.object.subject
        return reverse_lazy('curriculum:lesson_detail', kwargs={'standard': standard.slug, 'subject': subject.slug, 'slug': self.object.slug})

    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.lesson_name = self.object.comments.name
        fm.lesson_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())


    def get_context_data(self, **kwargs):
        context = super(LessonDetailView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class()

        return context
# class LessonCreateView(CreateView):
#     form_class = LessonForm
#     context_object_name = 'lessons'
#     model=Lesson
#     template_name = 'curriculum/lesson_create_view.html'
    
#     def get_success_url(self):
#         self.object = self.get_object()
#         standard = self.object.standard
#         return reverse_lazy('curriculum:lesson_list', kwargs={'standard':standard.slug, 
#                                                               'slug': self.object.slug})
    
#     def form_valid(self, form, *args, **kwargs):
#         self.object = self.get_object()
#         fm = form.save(commit=False)
#         fm.created_by = self.request.user
#         fm.standard = self.object.standard
#         fm.subject = self.object
#         fm.save()
#         return HttpResponseRedirect(self.get_success_url(*args, **kwargs))
class LessonCreateView(CreateView):
    form_class = LessonForm
    context_object_name = 'lessons'
    model = Lesson
    template_name = 'curriculum/lesson_create_view.html'
    
    def get_success_url(self):
        subject = self.object.subject
        standard = self.object.standard
        return reverse_lazy('curriculum:lesson_list', kwargs={'standard': standard.slug, 'slug': subject.slug })
    
    def form_valid(self, form, *args, **kwargs):
        subject_slug = self.kwargs.get('slug')
        subject = Subject.objects.get(slug=subject_slug)
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.standard = subject.standard
        fm.subject = subject
        fm.save()
        self.object = fm
        return HttpResponseRedirect(self.get_success_url(*args, **kwargs))

class LessonUpdateView(UpdateView):
    #fields = ('name', 'position', 'videos', 'ppt', 'Notes')
    form_class = LessonForm
    context_object_name = 'lessons'
    model = Lesson
    template_name = 'curriculum/lesson_update_view.html'

class LessonDeleteView(DeleteView):
    #fields = ('name', 'position', 'videos', 'ppt', 'Notes')
    #form_class = LessonForm
    context_object_name = 'lessons'
    model = Lesson
    template_name = 'curriculum/lesson_delete_view.html'
    
    def get_success_url(self):
        subject = self.object.subject
        standard = self.object.standard
        return reverse_lazy('curriculum:lesson_list', kwargs={'standard': standard.slug, 'slug': subject.slug })