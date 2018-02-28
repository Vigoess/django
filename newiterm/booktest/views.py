from datetime import date
from io import BytesIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from django.core.urlresolvers import reverse
from django.db.models import F ,Sum, Avg, Max, Min
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from booktest.models import BookInfo, HeroInfo, AreaInfo


def index(request):
    book = BookInfo.objects.get(id=1)
    # books = BookInfo.objects.filter(btitle__contains='龙')
    # books = BookInfo.objects.filter(btitle__endswith='部')
    # books = BookInfo.objects.filter(id__in=[1,4])
    # 不等于exclude
    # books = BookInfo.objects.exclude(id = 2)
    # books = BookInfo.objects.filter(bpub_date__year = 1980)
    # books = BookInfo.objects.filter(bpub_date__gt=date(1980, 1, 1))
    # books = BookInfo.objects.filter(bread__gte= F('bcomment')*2)
    # books = BookInfo.objects.filter(bread__gte=20,id__lt=4)
    # books = BookInfo.objects.filter(bread__gte=20).filter(id__lt=4)
    # books = BookInfo.objects.filter(Q(bread__gte=20)|Q(id__lt=4))
    # books = BookInfo.objects.filter(Q(bread__gte=20)&Q(id__lt=4))
    # books = BookInfo.objects.filter(~Q(id__gte= 3))
    # books = BookInfo.objects.filter(Q(bread__gt = 20)&Q(bcomment__lt=40))
    # books = BookInfo.objects.filter(Q(bread__gt=20)|Q(bcomment__lt=40))
    # dict_num =BookInfo.objects.aggregate(Sum('bcomment'))
    # num = dict_num.get('bcomment__sum')
    # num = HeroInfo.objects.count()
    # dict_num=BookInfo.objects.aggregate(Avg('bread'))
    # num = dict_num.get('bread__avg')
    # dict_date = BookInfo.objects.aggregate(Max('bpub_date'))
    # num = dict_date.get('bpub_date__max')
    dict_bread =BookInfo.objects.aggregate(Max('bread'))
    # num = dict_bread.get('bread__min')
    num = dict_bread['bread__max']
    #查询集
    books = BookInfo.objects.all()[1:2]
    context = {'book':book,'books':books,'num':num,'dict_bread':dict_bread}

    return render(request,'booktest/index.html',context)

def test_join(request):
    book =  BookInfo.objects.get(pk=3)
    heros = book.heroinfo_set.all()
    hero = HeroInfo.objects.get(id = 5)
    book1 = hero.hbook

    context ={'heros':heros,'book1':book1}
    return render(request,'booktest/test_join.html',context)

def test_join1(request):
    #关联查询，查询英雄技能有'六"的书名
    books = BookInfo.objects.filter(heroinfo__hcontent__contains='六')
    #查询书名为天龙八部的所有英雄
    heros = HeroInfo.objects.filter(hbook__btitle ='天龙八部')
    #查询阅读量超过12的书的英雄的技能有哪些
    heros1 = HeroInfo.objects.filter(hbook__bread__gt=12)

    context = {'books':books,'heros':heros,'heros1':heros1}
    return render(request,'booktest/test_join1.html',context)

def testself(request):
    #查询合肥市
    # city = AreaInfo.objects.get(atitle='合肥市')
    city = AreaInfo.objects.filter(atitle='上海市')
    if city.count()>1:
        city = city[1]
    else:
        city = city[0]
    #查询合肥市所属的省份
    parent = city.aParent
    #查询合肥市下属区域
    lowcity = city.areainfo_set.all()



    context = {'city':city,'parent':parent,'lowcity':lowcity}
    return render(request,'booktest/testself.html',context)







def test_var(request):
    books = BookInfo.objects.all()
    dict = {'title':'标题'}
    book = BookInfo()
    book.btitle = '元尊'
    context = {'books':books,'book':book,'dict':dict}
    return render(request,'booktest/test_var.html',context)

def show_book(request):
    books=BookInfo.objects.all()
    a=13
    context = {'books':books,'a':a}
    return  render(request,'booktest/show_book.html',context)

def extend_show(request):
    return render(request,'booktest/extend_show.html')

def escape_show(request):
    context = {'content':'<h1>小强</h1>'}
    return render(request,'booktest/escape_show.html',context)




def verify_code(request):
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    buf = BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

def verify_show(request):

    return render(request,'booktest/verify_show.html')
def check_verify(request):
    code = request.POST.get('code')
    verify_code = request.session['verifycode']
    if code.lower() ==verify_code.lower():
        return HttpResponse('ok')
    else:
        return HttpResponse('not ok')

def fan1(request):
    a=55
    b='youeryuan'
    c='男'
    context = {'a':a,'b':b,'c':c}
    return render(request,'booktest/fan1.html',context)


def fan2(request):
    return HttpResponse('fan2')


def fan3(request):
    a = 89
    b = 'youeryuan'
    c = '人妖'
    # return redirect(reverse('booktest:fan_test',args=(a,b,c)))
    return redirect(reverse('booktest:fan_test',kwargs={'name':b,'age':a,'gender':c}))

def fan_test(request,age,gender,name):
    context = {'age':age,'gender':gender,'name':name}
    return render(request,'booktest/fan_show.html',context)
