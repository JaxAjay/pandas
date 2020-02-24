import json

from django.conf import settings
from django.http import HttpResponse
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
    df.columns = df.columns.str.strip().str.lower() \
        .str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('-', '_')
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
    value = call_function('brand', 'category')
    return HttpResponse(json.dumps(value, default=str), status=200)


def call_function(*args):
    csv_obj = pandas.read_excel("%s/%s" % (settings.STATICFILES_DIR, 'Inventory.xlsx'))
    df = pandas.DataFrame(csv_obj)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_') \
        .str.replace('(', '').str.replace(')', '').str.replace('-', '_')
    try:
        df_groups = df.groupby(by=list(args))
        dd = {str(k).strip().replace('(', '').replace(')', '').
                  replace("'", '').replace(",", '').replace(' ', "_"): v.to_dict('list') for k, v in df_groups}
        # print(dd)
        return dd
    except:
        return None


import random


def panda_tuts(request):
    df = pandas.read_excel("%s/%s" % (settings.STATICFILES_DIR, 'Archived_Transaction.xlsx'), sheet_name=0)

    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_') \
        .str.replace('(', '').str.replace(')', '').str.replace('-', '_')
    df1 = df
    df3 = df1.drop_duplicates(subset=['ordernumber', 'po_productid1', 'shipmentcreateddt',
                                      'po_quantityordered', 'sh_unitsshipped']).dropna(subset=['sh_unitsshipped'])

    t2 = df3.groupby(['transactionid'])

    new_df = pandas.DataFrame()

    for k, v in t2:
        if v['po_quantityordered'].sum() == v['sh_unitsshipped'].sum():
            new_df = new_df.append(v, ignore_index=True)
        else:
            for k2, v2 in v.groupby(['po_productid1']):
                # check2.append({k2: v2})
                # v3 = v2.sort_values['sh_unitsshipped']
                # check1.append({k2: v3})
                x = int(v2.iloc[0]['po_quantityordered'])
                y = 0
                for index, row in v2.iterrows():
                    # print(row)
                    y += int(row['sh_unitsshipped'])
                    if x >= y:
                        new_df = new_df.append(row)
                    else:
                        pass

    new_df = new_df[df3.columns]
    # new_df.to_excel('archieved_transaction.xlsx',index=False)
    print(len(df3), len(new_df))
    pass


def add_batch_column(request):
    df = pandas.read_excel("%s/%s" % (settings.STATICFILES_DIR, 'archieved_transaction.xlsx'), sheet_name=0)

    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_') \
        .str.replace('(', '').str.replace(')', '').str.replace('-', '_')
    # print(df.columns)
    df1 = df
    df_group = df1.groupby(['ordernumber', 'po_productid1'])
    new_df = pandas.DataFrame()
    for k, v in df_group:
        v.sort_values('shipmentcreateddt', ascending=True, inplace=True)
        v.insert(len(v.columns), 'batch_deploy', [x for x in range(0, len(v))])
        new_df = new_df.append(v)

    new_df.to_csv('archieved_transaction_batch_deploy.csv', index=False, date_format='%Y-%m-%d, %H:%M:%S')
    # new_df.to_excel('transaction_batch_deploy.xlsx',index=False)
    pass


def test_function(request):
    df = pandas.read_excel("%s/%s" % (settings.STATICFILES_DIR, 'archieved_transaction.xlsx'), sheet_name=0)

    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_') \
        .str.replace('(', '').str.replace(')', '').str.replace('-', '_')

    df1 = df[['ordernumber', 'po_productid1']]
    print(df1)
    print(dir(df1))
    print(df1['ordernumber'].unique(), type(df1))

    pass


def number_of_distinct_column(request):
    df = pandas.read_csv("%s/%s" % (settings.STATICFILES_DIR, 'archieved_transaction_batch_deploy.csv'))

    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_') \
        .str.replace('(', '').str.replace(')', '').str.replace('-', '_')
    print(df.columns)
    df1 = df[['ordernumber', 'pocreateddt', 'po_productid1', 'po_quantityordered', 'sh_unitsshipped']]
    print(df1.head(10))
    groups = df.groupby(['ordernumber'])
    new_df = pandas.DataFrame()
    for k, v in groups:
        distinct = v.groupby('po_productid1')
        y = 0
        y += distinct.first()['po_quantityordered'].sum()
        v.insert(len(v.columns), 'distinct_products', [len(distinct) for _ in range(0, len(v))])
        v.insert(len(v.columns), 'bulk_order', [y for _ in range(0, len(v))])
        new_df = new_df.append(v)
    # print(new_df)
    new_df.to_csv('archieved_transaction_new.csv', index=False, date_format='%Y-%m-%d, %H:%M:%S')

    pass


def yet_to_shipped(request):
    df = pandas.read_csv("%s/%s" % (settings.STATICFILES_DIR, 'archieved_transaction_new.csv'))

    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_') \
        .str.replace('(', '').str.replace(')', '').str.replace('-', '_')

    df1 = df[['ordernumber', 'pocreateddt', 'po_productid1', 'po_quantityordered',
              'sh_unitsshipped', 'shipmentcreateddt']]

    new_df = pandas.DataFrame()
    for k, v in df.groupby(['po_productid1', 'ordernumber']):
        total = 0
        for i in v['po_quantityordered'].unique():
            total += i
        v.insert(len(v.columns), 'yet_to_ship', [(total - i) for i in calculate_total(v.iterrows())])
        new_df = new_df.append(v)

    new_df.to_csv('archieved_transaction_ship.csv', index=False, date_format='%Y-%m-%d, %H:%M:%S')

    pass


def calculate_total(x):
    val = 0
    lis = []
    for i, j in x:
        val += j['sh_unitsshipped']
        lis.append(val)
    return lis


def yet_to_ship2(request):
    df = pandas.read_csv("%s/%s" % (settings.STATICFILES_DIR, 'archieved_transaction_new.csv'))

    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_') \
        .str.replace('(', '').str.replace(')', '').str.replace('-', '_')

    df1 = df[['ordernumber', 'pocreateddt', 'po_productid1', 'po_quantityordered',
              'sh_unitsshipped', 'shipmentcreateddt']]

    groups = df1.head(50).groupby(['po_productid1'])

    for k, v in groups:
        v1 = v.sort_values('pocreateddt', inplace=False)
        v2 = v1.copy()
        print(v1)
        print('------------------------')
        print(v2.sort_values('shipmentcreateddt', inplace=True))
        # print('###################################')
        for row , columns in v1.iterrows():
            print(row , columns)

    pass
