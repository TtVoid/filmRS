import os
import pickle
from operator import itemgetter

from django.shortcuts import render

from django.db import connection

from model.models import Movies, Collect, Rate, Search, Ratings
import RSModel.utils

import collections
from collections import defaultdict


def main(request):
    context = {}
    films = Movies.objects.all().order_by("-release_time")[:24]
    context['status'] = 'normal'
    context['films'] = films

    print('userid:')
    print(request.session.get('userId'))
    recommendFilms = recommend(request.session.get('userId'), 6)  # 获取推荐的movieid
    context['recommendFilms'] = Movies.objects.filter(id__in=recommendFilms)

    return render(request, "main.html", context)


'''
#根据评分推荐电影
参数：
    user：用户id
    n_rec_movie：推荐的电影数量
'''
def ratingRecommend(userid, n_rec_movie, P, Q):
    # P = []
    # Q = []
    trainset = {}
    items_set = set()

    # 获取 P、Q、trainset
    for root, dirs, files in os.walk('RSModel/model/'):
        for file in files:
            # print(file)
            # if file[-5] == 'P':
            #     P = pickle.load(open('RSModel/model/' + file, "rb"))
            # if file[-5] == 'Q':
            #     Q = pickle.load(open('RSModel/model/' + file, "rb"))
            if file[28:36] == 'trainset':
                trainset = pickle.load(open('RSModel/model/' + file, "rb"))

    # 获取 items_set
    for user, movies in trainset.items():
        for item in movies:
            items_set.add(item)

    # interacted_items = trainset[[].append(user)]  # 评论过的电影
    interacted_items= dict()
    ratings=Ratings.objects.filter(userid=userid)
    for ratingItem in ratings:
        interacted_items[ratingItem.movieid]=ratingItem.rating
        # interacted_items.append({ratingItem.movieid:ratingItem.rating})
    rates=Rate.objects.filter(userid=userid)
    print("rates::::::")
    print(rates[2].movieid)
    for rateItem in rates:
        interacted_items[rateItem.movieid]=rateItem.rating
        # interacted_items.append({rateItem.movieid:ratingItem.rating})

    print('interacted_items.keys(): ')
    # print(interacted_items.keys())

    rank = collections.defaultdict(float)
    for item in items_set:
        # print(item)
        if int(item) in interacted_items.keys():
            print(item)
            continue
        for k, Qik in enumerate(Q[item]):  # 算出评分向量
            rank[item] += P[str(userid)][k] * Qik
    recommendedFilms = [movie for movie, _ in sorted(rank.items(), key=itemgetter(1), reverse=True)][
                       :n_rec_movie]  # 对评分向量排序

    return recommendedFilms


'''
#根据隐式反馈推荐电影
参数：
    user：用户id
    n_rec_movie：推荐的电影数量
'''
def recommend(userid, n_rec_movie):
    rate = Rate.objects.filter(userid=userid).order_by("movieid")     #查询该用户新评分
    collect = Collect.objects.filter(userid=userid).order_by("movieid")     #查询该用户收藏
    search = Search.objects.filter(userid=userid).order_by("movieid")     #查询该用户搜索

    #计算 { movieid:wui, ..., movieid:wui }
    samples=dict()
    for rateItem in rate:       #根据评分定 权重 w
        if(rateItem.rating==3):
            samples[rateItem.movieid]=1
        elif(rateItem.rating==4):
            samples[rateItem.movieid]=2
        elif(rateItem.rating==5):
            samples[rateItem.movieid]=3
    for collectItem in collect:       #根据收藏定 权重 w
        if(collectItem.movieid in samples.keys() and samples[collectItem.movieid]<2):
            samples[collectItem.movieid] = 2
    for searchItem in search:       #根据搜索定 权重 w
        if(not searchItem.movieid in samples.keys()):
            samples[searchItem.movieid] = 1

    P = []
    Q = []
    trainset = {}
    items_set = set()
    K = 48
    lamb=0.01

    # 获取 P、Q、trainset
    for root, dirs, files in os.walk('RSModel/model/'):
        for file in files:
            # print(file)
            if file[-5] == 'P':
                P = pickle.load(open('RSModel/model/' + file, "rb"))
                K = int(file[30:file.index('-epochs')])
                lamb = float(file[file.index('lamb')+5:file.index('-P.pkl')])
            if file[-5] == 'Q':
                Q = pickle.load(open('RSModel/model/' + file, "rb"))

    for item, wui in samples.items():
        rui = 1
        eui = rui - predict(userid, item, K, P, Q)  # 计算误差
        eata = 0.00001 + 1 * wui
        for k in range(K):  # SGD   随机梯度下降法训练参数P和Q
            P[str(userid)][k] += eata * (eui * Q[str(item)][k] - lamb * P[str(userid)][k])
            Q[str(item)][k] += eata * (eui * P[str(userid)][k] - lamb * Q[str(item)][k])

    recommendFilms = ratingRecommend(userid, n_rec_movie, P, Q)
    return recommendFilms


#根据 P 和 Q 预测评分
def predict(userid, item, K, P, Q):
    print(userid)
    print(item)
    print(K)
    print(len(P))
    print(len(Q))
    print(P[str(1)][1])
    rate_e = 0
    for k in range(K):
        Puk = P[str(userid)][k]
        Qki = Q[str(item)][k]
        rate_e += Puk * Qki
    return rate_e