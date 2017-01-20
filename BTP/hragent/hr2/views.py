from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.http import JsonResponse
import json
from hr2.forms import DocumentForm, PostingForm
class IndexView(FormView):
	template_name = 'index.html'
	def get_context_data(self, **kwargs):
		context = dict({'form':DocumentForm(), 'posting_form':PostingForm()})
		return context  


