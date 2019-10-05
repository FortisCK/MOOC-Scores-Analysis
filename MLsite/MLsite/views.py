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
        uploadDir = BASE_DIR+'/upload'+'/namelist'
        if not isdir(uploadDir):
            mkdir(uploadDir)
        uploadedFile = request.FILES.get('Scores')
        if not uploadedFile:
            return render(request, 'mingdan.html', {'msg':'没有选择文件'})
        if not uploadedFile.name.endswith('.xlsx'):
            if not uploadedFile.name.endswith('.xls'):
                return render(request, 'mingdan.html', {'msg':'必须选择xlsx或xls文件'})
        dstFilename = join(uploadDir, uploadedFile.name)
        with open(dstFilename, 'wb') as fp:
            for chunk in uploadedFile.chunks():
                fp.write(chunk)
        pdData = pd.read_excel(dstFilename)
        pdData = pdData[3:][['2019-2020学年第1学期点名册', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4']]
        pdhtml = pdData.to_html(index=False)
        context = {}
        context['text'] = pdhtml
        context['msg'] = '上传成功'
        return render(request, 'mingdan.html', context)
    else:
        return render(request, 'mingdan.html',{'msg':None})
    
def onceanalyse(request):
    dstFilename = BASE_DIR+'/upload/'+'namelist/'+'(2019-2020-1)-B0300121S-JSJY0001-11dmc.xls'
    Data = pd.read_excel(dstFilename)
    Data = Data[4:][['2019-2020学年第1学期点名册', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4']]
    names = Data['Unnamed: 2'].tolist()
    IDs = Data['Unnamed: 1'].tolist()
    students = dict(zip(names, IDs))
    if request.method == 'POST':
        uploadDir = BASE_DIR+'/upload'+'/oncescore'
        if not isdir(uploadDir):
            mkdir(uploadDir)
        uploadedFile = request.FILES.get('Scores')
        if not uploadedFile:
            return render(request, 'once.html', {'msg':'没有选择文件'})
        if not uploadedFile.name.endswith('.xlsx'):
            if not uploadedFile.name.endswith('.xls'):
                return render(request, 'once.html', {'msg':'必须选择xlsx或xls文件'})
        dstFilename = join(uploadDir, uploadedFile.name)
        with open(dstFilename, 'wb') as fp:
            for chunk in uploadedFile.chunks():
                fp.write(chunk)
        pdData = pd.read_excel(dstFilename)
        rarenames = pdData['真实姓名'].tolist()
        wholenames = []
        for name in rarenames:
            if type(name)==str:
                wholenames.append(name)
        meijiao =[]
        for name in names:
            if not name in wholenames:
                meijiao.append(name)
        scores = {}
        for name in wholenames:
            temp=pdData['得分'][pdData['真实姓名']==name].tolist()
            scores[name]=temp[0]
        maxscore = max(scores.values())
        goods = []
        bads = []
        for key, value in scores.items():
            if value >= maxscore*0.9:
                goods.append(key)
            elif value < maxscore*0.6:
                bads.append(key)
        MeiJiao = {}
        Goods = {}
        Bads = {}
        for i, j in students.items():
            if i in meijiao:
                MeiJiao.update({i:j})
            elif i in goods:
                Goods.update({i:j})
            elif i in bads:
                Bads.update({i:j})
        meijiao.clear()
        goods.clear()
        bads.clear()
        for key, value in MeiJiao.items(): 
            meijiao.append(key+value)
        for key, value in Goods.items(): 
            goods.append(key+value)
        for key, value in Bads.items(): 
            bads.append(key+value)
        dic1 = {'没交作业的人':meijiao,}
        df1=pd.DataFrame(data=dic1)
        dh1=df1.to_html(index=False)
        dic2 = {'做得不好的人':bads,}
        df2=pd.DataFrame(data=dic2)
        dh2=df2.to_html(index=False)
        dic3 = {'做得好的人':goods,}
        df3=pd.DataFrame(data=dic3)
        dh3=df3.to_html(index=False)
        context = {}
        context['text1'] = dh1
        context['text2'] = dh2
        context['text3'] = dh3
        context['msg'] = '上传成功'
        return render(request, 'once.html', context)
    else:
        return render(request, 'once.html',{'msg':None})


