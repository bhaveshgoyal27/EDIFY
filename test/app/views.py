from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from collections import Counter
from django.urls import reverse
from django.shortcuts import redirect
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from io import StringIO
import base64
import io

def index(request):
	return render(request,'index.html')

def upload(request):
	if request.method=="POST":
		csv_file = request.FILES["csv_file"]
		if not csv_file.name.endswith('.csv'):
			return HttpResponse("error1")
			messages.error(request,'File is not CSV type')
			return HttpResponseRedirect(reverse("upload"))
	#if file is too large, return message
		if csv_file.multiple_chunks():
			return HttpResponse("error2")
			messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
			return HttpResponseRedirect(reverse("upload"))
		if csv_file:
			#return HttpResponse("success")
			df = pd.read_csv(csv_file)
			l = df.columns.tolist()
			d= df.describe()
			d={'mean':df.mean(),'median': df.median().dropna(),'max': df.max(),'min':df.min(),'std':df.std().dropna()}
			mean={}
			median={}
			max1={}
			min1={}
			std={}
			for i in l:
				mean[i]=df[i].mean()
				median[i]=df[i].median()
				max1[i]=df[i].max()
				min1[i]=df[i].min()
				std[i]=df[i].std()
			plt.tight_layout()
			a = df.columns.tolist()
			b = len(a)
			plt.subplots_adjust(left=3, bottom=3, right=5, top=5, wspace=1, hspace=1)
			for i in range(b**2):
				plt.subplot(b,b,i+1)
				plt.plot(df[a[i//b]],df[a[i%b]])
				plt.xlabel(a[i//b])
				plt.ylabel(a[i%b])
			plt.autofmt_xdate()
			canvas=FigureCanvas(plt)
			canvas.print_png(response)
			buf = io.BytesIO()
			plt.savefig(buf, format='png')
			buf.seek(0)
			buffer = b''.join(buf)
			b2 = base64.b64encode(buffer)
			plt2=b2.decode('utf-8')
			plt.savefig('./static/assets/1.png')
			return render(request,'upload.html',{'mean':mean,'median':median,'max':max1,'min':min1,'std':std,'name':l})
		else:
			return HttpResponse("error3")
			return render(request,'index.html')
	else:
		return redirect('/')