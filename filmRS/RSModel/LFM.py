#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: fuxuemingzhu 
@site: www.fuxuemingzhu.cn

@file: LFM.py
@time: 18-6-19 下午2:38

Description : Latent Factor Model
"""
import collections
import random
from operator import itemgetter

import math

from collections import defaultdict

import RSModel.utils
from RSModel.utils import LogTime


class LFM:
    """
    Latent Factor Model.
    Top-N recommendation.
    """

    def __init__(self, K, epochs, alpha, lamb, n_rec_movie=10, save_model=True):
        """
        Init LFM with K, T, alpha, lamb
        :param K: Latent Factor dimension
        :param epochs: epochs to go
        :param alpha: study rate
        :param lamb: regular params
        :param save_model: save model
        """
        print("LFM start...\n")
        self.K = K
        self.epochs = epochs
        self.alpha = alpha
        self.lamb = lamb
        self.n_rec_movie = n_rec_movie
        self.save_model = save_model
        self.users_set, self.items_set = set(), set()
        self.items_list = list()
        self.P, self.Q = None, None
        self.trainset = None
        self.testset = None
        self.item_popular, self.items_count = None, None
        self.model_name = 'K={}-epochs={}-alpha={}-lamb={}'.format(self.K, self.epochs, self.alpha, self.lamb)

    def init_model(self, users_set, items_set, K):
        """
        Init model, set P and Q with random numbers.
        :param users_set: Users set
        :param items_set: Items set
        :param K: Latent factor dimension.
        :return: None
        """
        self.P = dict()
        self.Q = dict()
        for user in users_set:
            self.P[user] = [random.random()/math.sqrt(K) for _ in range(K)]     #初始化随机 P矩阵
        for item in items_set:
            self.Q[item] = [random.random()/math.sqrt(K) for _ in range(K)]     #初始化随机 Q矩阵

    def init_users_items_set(self, trainset):
        """
        Get users set and items set.
        :param trainset: train dataset
        :return: Basic users and items set, etc.
        """
        users_set, items_set = set(), set()
        items_list = []
        item_popular = defaultdict(int)     #设置为 int类型的字典
        for user, movies in trainset.items():
            for item in movies:
                item_popular[item] += 1
                users_set.add(user)
                items_set.add(item)
                items_list.append(item)
        items_count = len(items_set)
        return users_set, items_set, items_list, item_popular, items_count

    def gen_negative_sample(self, items=dict):
        """
        Generate negative samples
        :param items: Original items, positive sample       { movieid:rating, ..., movieid:rating }
        :return: Positive and negative samples
        """
        samples = dict()
        for item, rate in items.items():
            samples[item] = 1
        for i in range(len(items) * 11):
            item = self.items_list[random.randint(0, len(self.items_list) - 1)]   #在items_list中随机取一部电影
            if item in samples:
                continue
            samples[item] = 0
            if len(samples) >= 10 * len(items):     #保证正负样本比例为 1:9
                break
        # print(samples)
        return samples

    def predict(self, user, item):
        """
        Predict the rate for item given user and P and Q.
        :param user: Given a user
        :param item: Given a item to predict the rate
        :return: The predict rate
        """
        rate_e = 0
        for k in range(self.K):
            Puk = self.P[user][k]
            Qki = self.Q[item][k]
            rate_e += Puk * Qki
        return rate_e

    def train(self, trainset):
        """
        Train model.
        :param trainset: Origin trainset.
        :return: None
        """
        for epoch in range(self.epochs):
            print('epoch:', epoch)
            for user in trainset:
                # print(user)
                # print(trainset[user])
                samples = self.gen_negative_sample(trainset[user])      #生成负样本，返回正负样本字典 1:9
                for item, rui in samples.items():
                    eui = rui - self.predict(user, item)        #计算误差
                    for k in range(self.K):     # SGD   随机梯度下降法训练参数P和Q
                        self.P[user][k] += self.alpha * (eui * self.Q[item][k] - self.lamb * self.P[user][k])
                        self.Q[item][k] += self.alpha * (eui * self.P[user][k] - self.lamb * self.Q[item][k])
            self.alpha *= 0.9
            # print(self.P)
            # print(self.Q)

    def fit(self, trainset):
        """
        Fit the trainset by optimize the P and Q.
        :param trainset: train dataset
        :return: None
        """
        self.trainset = trainset
        self.users_set, self.items_set, self.items_list, self.item_popular, self.items_count = \
            self.init_users_items_set(trainset)
        model_manager = RSModel.utils.ModelManager()
        try:
            self.P = model_manager.load_model(self.model_name + '-P')       #读取 P矩阵
            self.Q = model_manager.load_model(self.model_name + '-Q')       #读取 Q矩阵
            print('User origin similarity model has saved before.\nLoad model success...\n')
        except OSError:
            print('No model saved before.\nTrain a new model...')
            self.init_model(self.users_set, self.items_set, self.K)     #初始化 P和 Q 矩阵
            self.train(self.trainset)
            print('Train a new model success.')
            if self.save_model:
                model_manager.save_model(self.P, self.model_name + '-P')
                model_manager.save_model(self.Q, self.model_name + '-Q')
            print('The new model has saved success.\n')
        return self.P, self.Q

    def recommend(self, user):
        """
        Recommend N movies for the user.
        :param user: The user we recommend movies to.
        :return: the N best score movies
        """
        rank = collections.defaultdict(float)
        interacted_items = self.trainset[user]
        for item in self.items_set:
            if item in interacted_items.keys():
                continue
            for k, Qik in enumerate(self.Q[item]):      #算出评分向量
                rank[item] += self.P[user][k] * Qik
        return [movie for movie, _ in sorted(rank.items(), key=itemgetter(1), reverse=True)][:self.n_rec_movie]     #对评分向量排序，返回

    def test(self, testset):
        """
        Test the recommendation system by recommending scores to all users in testset.
        :param testset: test dataset
        :return: None
        """
        self.testset = testset
        print('Test recommendation system start...')
        #  varables for precision and recall
        hit = 0
        rec_count = 0
        test_count = 0
        # varables for coverage
        all_rec_movies = set()
        # varables for popularity
        popular_sum = 0

        # record the calculate time has spent.
        test_time = LogTime(print_step=1000)
        for user in self.users_set:
            test_movies = self.testset.get(user, {})
            rec_movies = self.recommend(user)  # type:list
            for movie in rec_movies:
                if movie in test_movies.keys():     #推荐的电影在测试集中，命中
                    hit += 1
                all_rec_movies.add(movie)
                popular_sum += math.log(1 + self.item_popular[movie])       #取 e的对数
                # log steps and times.
            rec_count += self.n_rec_movie       #总推荐电影数
            test_count += len(test_movies)      #总测试数
            # print time per 500 times.
            test_time.count_time()
        precision = hit / (1.0 * rec_count)     # 准确率 = 命中数 / 推荐总数
        recall = hit / (1.0 * test_count)
        coverage = len(all_rec_movies) / (1.0 * self.items_count)
        popularity = popular_sum / (1.0 * rec_count)
        print('Test recommendation system success.')
        test_time.finish()
        print('precision=%.4f\trecall=%.4f\tcoverage=%.4f\tpopularity=%.4f\n' %
              (precision, recall, coverage, popularity))
