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
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')',
                                                                                                           '').str.replace(
        '-', '_')
    df1 = df[['category', 'sub_cate', 'gender']]
    print(df1.category.unique())
    category_unique = df1.category.unique()
    gender_unique = df1.gender.unique()
    print(gender_unique)
    sub_category_unique = df1.sub_cate.unique()
    print(sub_category_unique)

    df_category = {i: df1.loc[df1['category'] == i] for i in category_unique}
    # print(df_category)
    df_category_gender = {k: {i: v.loc[v['gender'] == i] for i in gender_unique} for k, v in df_category.items()}
    print(len(df_category_gender))
    print(df_category_gender)
    df_category_gender_sub_category = \
        {k: {k2: {i: v2.loc[v2['sub_cate'] == i] for i in sub_category_unique} for k2, v2 in v.items()} for k, v in
         df_category_gender.items()}
    print(df_category_gender_sub_category)

    pass


def inventory_groupby(request):
    # csv_obj = pandas.read_excel("%s/%s" % (settings.STATICFILES_DIR, 'Inventory.xlsx'))
    # df = pandas.DataFrame(csv_obj)
    # df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_') \
    #     .str.replace('(', '').str.replace(')', '').str.replace('-', '_')
    # params = ['category','gender']
    # df_groups = df.groupby(by=params)
    # dd = {k: v for k,v in df_groups}
    # print(dd)
    value = call_function('category', 'gender', 'sub_cate')
    pass


def call_function(*args):
    csv_obj = pandas.read_excel("%s/%s" % (settings.STATICFILES_DIR, 'Inventory.xlsx'))
    df = pandas.DataFrame(csv_obj)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_') \
        .str.replace('(', '').str.replace(')', '').str.replace('-', '_')
    try:
        df_groups = df.groupby(by=list(args))
        dd = {str(k).strip().replace('(', '').replace(')', '').
                  replace("'", '').replace(",", '').replace(' ', "_"): v.to_dict('list') for k, v in df_groups}
        print(dd)
        return dd
    except:
        return None
