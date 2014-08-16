from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from amoeba.models import Document
from amoeba.forms import DocumentForm
from django.conf import settings
import csv
import os

def index(request):
    context = RequestContext(request)
    documents = Document.objects.all()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)        
        if form.is_valid():
        	for document in documents :
        		file_path = os.path.join(settings.MEDIA_ROOT, document.docfile.name)
        		os.remove(file_path)
        	Document.objects.all().delete()
        	newdoc = Document(docfile = request.FILES['docfile'])
        	newdoc.save()
        	documents = Document.objects.all()
        context_dict = {'documents': documents, 'form': form}
        return render_to_response('amoeba/index.html', context_dict, context)
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    context_dict = {'documents': documents, 'form': form}

    return render_to_response('amoeba/index.html', context_dict, context)
 
def genes(request):
	for document in Document.objects.all():
		file_path = os.path.join(settings.MEDIA_ROOT, document.docfile.name)

	file=open(file_path)
	testReader=csv.reader(file,delimiter=',', quotechar='"')
	geneNameReader=[]
	context = RequestContext(request)

	if request.method=='POST':
		for row in testReader:
			if row[0][0:2]!='ID' and float(row[int(request.POST.get('time'))])>=float(request.POST.get('threshold')) :
				geneNameReader.append(row[0][0:10])
			context_dict = {'gene_list': geneNameReader, 'time' : request.POST.get('time'), 'threshold' : request.POST.get('threshold')}
	else:
		for row in testReader:
			if row[0][0:2]!='ID' :
				geneNameReader.append(row[0][0:10])
		context_dict = {'gene_list': geneNameReader}	
	return render_to_response('amoeba/genes.html', context_dict, context)

def plotProfile(request , geneId=None):
	for document in Document.objects.all():
		file_path = os.path.join(settings.MEDIA_ROOT, document.docfile.name)
	file=open(file_path)
	testReader=csv.reader(file,delimiter=',', quotechar='"')
	geneReader=[]
	geneProfile = []
	for row in testReader:
		if row[0][0:10] == request.GET['geneId']:
			geneReader = row
			break

	context = RequestContext(request)
	context_dict = {'geneId': request.GET['geneId'], 'geneProfile': geneReader }
	return render_to_response('amoeba/plotProfile.html', context_dict, context)
