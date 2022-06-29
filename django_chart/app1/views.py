from django.shortcuts import render
import wbgapi as wb
from .models import *
import requests


def store(request):
    products = Product.objects.all()
    context = {"products":products}
    print(products)
    
    return render(request, 'app1/store.html', context)

def cart(request):
    cities_dict = {'paris':40, 'tver':7}
    cities = {key: ('warm' if value >= 40 else 'cold') for (key, value) in cities_dict.items() }
    print(cities)
    
    return render(request, 'app1/cart.html')

def checkout(request):

    r = requests.get('https://data.nasdaq.com/api/v3/datasets/UNDATA/GID_IFIR_CAN.csv?column_index=2order=asc&start_date=1980-01-01&end_date=1990-12-31&collapse=annual')
    print(r)    
    print(r.text)    


    # TO USE  ALL AVAILABLE LIBRARIES
    # print(wb.series.info())
    # print(wb.series.info(q='current account'))
    # for id in wb.series.list(q='external debt'):
    #     print(id)

    dates = []
    values = []
    for i in wb.data.fetch('BN.CAB.XOKA.CD', ['RUS']):
    # for i in wb.data.fetch('BN.CAB.XOKA.GD.ZS', ['RUS']):
        if int(i['time'].split('R')[1]) > 1959 and i['value'] != None:
            dates.append(int(i['time'].split('R')[1]))
            values.append(round(i['value'],2))
            print(i['value'], i['time'].split('R')[1])
    
    
    print(wb.series.info(q='current account'))
    
    
    
    context = {'values':values[::-1], 'dates':dates[::-1] }
    return render(request, 'app1/checkout.html', context)
