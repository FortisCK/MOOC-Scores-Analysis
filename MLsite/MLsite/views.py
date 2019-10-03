from django.shortcuts import render
from os.path import isdir, dirname, join
from os import mkdir
from .settings import BASE_DIR
import pandas as pd

def home(request):
    context = {}
    return render(request, 'index.html', context)

def upload(request):
    if request.method == 'POST':
        uploadDir = BASE_DIR+'/upload'
        if not isdir(uploadDir):
            mkdir(uploadDir)
        uploadedFile = request.FILES.get('Scores')
        if not uploadedFile:
            return render(request, 'index.html', {'msg':'没有选择文件'})
        if not uploadedFile.name.endswith('.xlsx'):
            if not uploadedFile.name.endswith('.xls'):
                return render(request, 'index.html', {'msg':'必须选择xlsx或xls文件'})
        dstFilename = join(uploadDir, uploadedFile.name)
        with open(dstFilename, 'wb') as fp:
            for chunk in uploadedFile.chunks():
                fp.write(chunk)
        pdData = pd.read_excel(dstFilename)
        pdData = pdData[3:][['2019-2020学年第1学期点名册', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4']]
        pdhtml = pdData.to_html()
        context = {}
        context['text'] = pdhtml
        context['msg'] = '上传成功'
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html',{'msg':None})

