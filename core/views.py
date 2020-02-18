from django.conf import settings
from django.shortcuts import render
import pandas
import csv
# Create your views here.
import datetime


def readcsv(request):
    t1 = (datetime.datetime.now())
    csv_obj = pandas.read_csv("%s/%s" % (settings.STATICFILES_DIR, 'panda.csv'))
    data_frame = pandas.DataFrame(csv_obj)

    dic_obj2 = dic_obj = data_frame.to_dict()
    diff_dic = {}
    print(dic_obj)
    dic_obj['time_taken'] = {}
    diff_dates = [0] * len(dic_obj['Date-created'])
    for i in range(0, len(dic_obj['Date-created'])):
        diff_dates[i] = (datetime.datetime.strptime(list(dic_obj['Date-delivered'].values())[i], "%Y-%m-%d") - \
                         datetime.datetime.strptime(list(dic_obj['Date-created'].values())[i], "%Y-%m-%d")).days
        diff_dic[i] = (datetime.datetime.strptime(list(dic_obj['Date-delivered'].values())[i], "%Y-%m-%d") - \
                       datetime.datetime.strptime(list(dic_obj['Date-created'].values())[i], "%Y-%m-%d")).days
        dic_obj['time_taken'][i] = (
                datetime.datetime.strptime(list(dic_obj['Date-delivered'].values())[i], "%Y-%m-%d") - \
                datetime.datetime.strptime(list(dic_obj['Date-created'].values())[i], "%Y-%m-%d")).days

    new_decreasing = {}
    new_decreasing['name'] = {}
    new_decreasing['date-created'] = {}
    new_decreasing['date-delivered'] = {}
    new_decreasing['time_taken'] = {}
    for i in sorted(dic_obj['time_taken'].values(), reverse=True):
        for key, value in dic_obj['time_taken'].items():
            if i == value:
                new_decreasing['name'][key] = dic_obj['name'][key]
                new_decreasing['date-created'][key] = dic_obj['Date-created'][key]
                new_decreasing['date-delivered'][key] = dic_obj['Date-delivered'][key]
                new_decreasing['time_taken'][key] = dic_obj['time_taken'][key]
                del dic_obj['name'][key]
                del dic_obj['Date-created'][key]
                del dic_obj['Date-delivered'][key]
                del dic_obj['time_taken'][key]
                break

    print(new_decreasing)
    print(type(new_decreasing))
    t2 = (datetime.datetime.now())
    print(t2 - t1)
    pass


def pandacsv(request):
    csv_obj = pandas.read_csv("%s/%s" % (settings.STATICFILES_DIR, 'panda.csv'))
    df = data_frame = pandas.DataFrame(csv_obj)

    dd = pandas.to_datetime(data_frame['Date-delivered']) - pandas.to_datetime(data_frame['Date-created'])

    print(dd.dt.days)
    dd.name = 'time_taken'
    df = df.assign(time_taken=dd.dt.days)
    print(df)
    print(df.sort_values(by='time_taken', ascending=False))

    pass


def inventory_sort(request):
    csv_obj = pandas.read_excel("%s/%s" % (settings.STATICFILES_DIR, 'Inventory.xlsx'))

    df = pandas.DataFrame(csv_obj)
    df1 = df[['CATEGORY', 'SUB-CATE', 'GENDER']]
    print(df1.CATEGORY.unique())
    category_unique = df1.CATEGORY.unique()
    gender_unique = df1.GENDER.unique()
    print(gender_unique)
    sub_category_unique = df1.SUB-CATE.unique()
    print(sub_category_unique)
    # print(df[['CATEGORY','SUB-CATE','GENDER']])
    # print(df1.sort_values(by=['CATEGORY','SUB-CATE']))
    obj = {}
    # df.loc[df['CATEGORY'] == category_unique[0]]
    df_category = {i: df1.loc[df1['CATEGORY'] == i] for i in category_unique}

    # df_category = [ df1.loc[df1['CATEGORY']==i] for i in category_unique ]
    print(df_category)
    # df_category_gender = {i: [j.loc[j['GENDER'] == i] for k, j in df_category.items()] for i in gender_unique}
    df_category_gender = {k: {i: v.loc[v['GENDER'] == i] for i in gender_unique} for k, v in df_category.items()}

    # df_category_gender_sub_category =
    print(df_category_gender)
    print(obj)
    pass
