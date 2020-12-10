from django.shortcuts import render, redirect

from django.db import connection
from model.models import Movies, Ratings, Collect, Search, Rate


def filmDetail(request,id,status):
    if(status=='search'):   #判断是否通过搜索进入本页面
        searchItem=Search.objects.filter(userid=request.session.get('userId'),movieid=id)
        if(not searchItem.exists()):       #如果该用户还没有搜索过该电影
            Search(userid=request.session.get('userId'), movieid=id).save()

    context = {}

    # 根据id查询movie
    context['film'] = Movies.objects.filter(id=id)

    #计算平均评分
    context['avgRating']=calculateAvgRating(id)

    #收藏信息
    context['collected']=haveCollected(request.session.get('userId'), id)
    print(context['collected'])

    #评分信息
    context['ratingStatus'] = haveRated(request.session.get('userId'), id)

    return render(request, "filmDetail.html",context)

def clickCollect(request,id):
    print(request.session.get('is_login'))
    print(request.session.get('userId'))
    if((not request.session.get('is_login')) or request.session.get('userId')==None):
        return render(request, "login.html")

    context = {}

    # 根据id查询movie
    context['film'] = Movies.objects.filter(id=id)

    # 计算平均评分
    context['avgRating'] = calculateAvgRating(id)

    # 评分信息
    context['ratingStatus'] = haveRated(request.session.get('userId'), id)

    collected=Collect.objects.filter(userid=request.session.get('userId'),movieid=id)
    if collected.exists():     #收藏过
        Collect.objects.filter(userid=request.session.get('userId'),movieid=id).delete()
        context['collected']=False
    else:     #没收藏过
        Collect(userid=request.session.get('userId'),movieid=id).save()     #添加收藏数据
        context['collected']=True       #收藏

    return render(request, "filmDetail.html", context)



#点击评分
def clickRate(request,id,rating):
    print(rating)

    context = {}

    # 根据id查询movie
    context['film'] = Movies.objects.filter(id=id)

    # 计算平均评分
    context['avgRating'] = calculateAvgRating(id)

    # 收藏信息
    context['collected'] = haveCollected(request.session.get('userId'), id)

    Rate(userid=request.session.get('userId'), movieid=id, rating=rating).save()  # 添加评分数据
    context['ratingStatus']=[]
    for i in range(5):
        print(i)
        if (i+1)==int(rating):
            context['ratingStatus'].append({'disabled': 'disabled', 'active': 'active'})
        else:
            context['ratingStatus'].append({'disabled': 'disabled', 'active': ''})

    print(context['ratingStatus'])
    return render(request, "filmDetail.html", context)



#计算平均评分
def calculateAvgRating(id):
    cursor = connection.cursor()
    cursor.execute(
        "select avg(rating) as avgRating from ratings,movies where movies.id=" + id + " and ratings.movieId=movies.id")
    return round(cursor.fetchall()[0][0], 2)  # 计算平均评分



#查询本片是否被收藏
def haveCollected(userid,movieid):
    collected = Collect.objects.filter(userid=userid, movieid=movieid)  # 查询收藏记录
    if collected.exists():  # 有收藏
        return True
    else:
        return False

#查询本片是否被评分
def haveRated(userid,movieid):
    oldRating = Ratings.objects.filter(userid=userid, movieid=movieid)
    newRating = Rate.objects.filter(userid=userid, movieid=movieid)
    context={}
    context['ratingStatus'] = []
    if oldRating.exists():
        context['rating'] = oldRating[0].rating
        for i in range(5):
            if i + 1 == oldRating[0].rating:
                context['ratingStatus'].append({'disabled': 'disabled', 'active': 'active'})
            else:
                context['ratingStatus'].append({'disabled': 'disabled', 'active': ''})
    elif newRating.exists():
        context['rating'] = newRating[0].rating
        for i in range(5):
            if i + 1 == newRating[0].rating:
                context['ratingStatus'].append({'disabled': 'disabled', 'active': 'active'})
            else:
                context['ratingStatus'].append({'disabled': 'disabled', 'active': ''})
    else:
        for i in range(5):
            context['ratingStatus'].append({'disabled': '', 'active': ''})

    return context['ratingStatus']