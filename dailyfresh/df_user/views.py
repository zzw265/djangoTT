from django.shortcuts import render,redirect
from .models import *
from hashlib import sha1
from django.http import JsonResponse,HttpResponseRedirect

# Create your views here.
def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):
    #接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    cpwd = post.get('cpwd')
    email = post.get('email')
    #判断两次密码
    if upwd!=cpwd:
        return redirect('/user/register/')
    #密码加密
    s1 = sha1()
    upwd1 = upwd.encode('utf-8')
    s1.update(upwd1)
    upwd2 = s1.hexdigest()
    #创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd2
    user.uemail = email
    user.save()
    #注册成功，转到登录页面
    return redirect('/user/login')

def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):
    #默认给cookies是空，如果有着读cookies的值
    uname = request.COOKIES.get('uname','')
    context = {'title':'用户登录', 'error_name':0, 'error_pwd':0, 'uname':uname}
    return render(request,'df_user/login.html',context)

def login_handle(requeset):
    #接收请求信息
    uname = requeset.POST.get('username')
    upwd = requeset.POST.get('pwd')
    #如果选中则提交过来jizhu的值为1，则0就用不上，如果不选中则没有提交值过来，则用设置默认值0
    jizhu = requeset.POST.get('jizhu',0)
    #根据用户名查询对象,filter查到的数据不存在则返回[]，如果用get查，不存在则报错
    users = UserInfo.objects.filter(uname = uname)
    if len(users)==1:
        s1 = sha1()
        upwd1 = upwd.encode('utf-8')
        s1.update(upwd1)
        if s1.hexdigest()==users[0].upwd:
            #HttpResponse填写的参数是地址
            red = HttpResponseRedirect('/user/info/')
            #记住用户名
            if jizhu!=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            requeset.session['user_id'] = users[0].id
            requeset.session['user_name'] = uname
            return red
        else:
            context = {'title':'用户登录', 'error_name':0, 'error_pwd':1, 'uname':uname, 'upwd':upwd}
            return render(requeset, 'df_user/login.html', context)

    else:
        context = {'title':'用户登录', 'error_name':1, 'error_pwd':0, 'uname':uname, 'upwd':upwd}
        return render(requeset, 'df_user/login.html', context)

def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    context = {
        'title':'用户中心',
        'user_email':user_email,
        'user_name':request.session['user_name']
    }
    return render(request, 'df_user/user_center_info.html', context)

def order(request):
    context = {'title':'用户中心'}
    return render(request, 'df_user/user_center_order.html', context)

def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title':'用户中心','user':user}
    return render(request, 'df_user/user_center_site.html', context)
