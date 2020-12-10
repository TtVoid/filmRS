# -*- coding = utf-8 -*-

import RSModel.utils
from RSModel.LFM import LFM
from RSModel.dataset import DataSet
from RSModel.utils import LogTime


def run_model(model_name, dataset_name, test_size=0.3, clean=False):
    print('*' * 70)
    print('\tThis is %s model trained on %s with test_size = %.2f' % (model_name, dataset_name, test_size))
    print('*' * 70 + '\n')
    model_manager = RSModel.utils.ModelManager(dataset_name, test_size)     #初始化模型管理器
    model_manager.clean_workspace(clean)
    # try:
    #     trainset = model_manager.load_model('trainset')
    #     testset = model_manager.load_model('testset')
    # except OSError:     # load_model函数中 raise OSError后 执行
    ratings = DataSet.load_dataset(name=dataset_name)
    trainset, testset = DataSet.train_test_split(ratings, test_size=test_size)
    model_manager.save_model(trainset, 'trainset')      #保存训练集
    model_manager.save_model(testset, 'testset')        #保存测试集
    '''Do you want to clean workspace and retrain model again?'''
    '''if you want to change test_size or retrain model, please set clean_workspace True'''

    # K, epochs, alpha, lamb, n_rec_movie
    model = LFM(48, 50, 0.03, 0.01, 10)
    model.fit(trainset)
    # recommend_test(model, [1, 100, 233, 666, 888])
    recommend_test(model, [1, 100, 233, 333, 444])
    model.test(testset)


def recommend_test(model, user_list):
    for user in user_list:
        recommend = model.recommend(str(user))
        print("recommend for userid = %s:" % user)
        print(recommend)
        print()


def main():
    main_time = LogTime(words="Main Function")
    dataset_name = 'ml-latest-small'
    model_type = 'LFM'
    test_size = 0.1
    run_model(model_type, dataset_name, test_size, True)
    main_time.finish()
