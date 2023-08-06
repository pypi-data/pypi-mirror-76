from urllib import parse
import urllib
import urllib.request
import requests,json
ak='PNngqzs09GAwTs0MCQqGIBvLtOe342ZU'
def get_ipaddress(ip):
     if ip.count(".")!=3:
         return -1
     else:
         url = 'http://api.map.baidu.com/location/ip?ak='+ak+'&ip='+urllib.parse.quote(ip)+'&coor=bd09ll'
         address=urllib.request.urlopen(url).read().decode("utf-8")
         if 0:
             return -1
         else:
             if "status" in address:
                address = json.loads(address)
                if address['status']==0:
                    content=address['content']
                    return content['address']
                else:
                    return -1
def get_traffic(road,city):
    url='http://api.map.baidu.com/traffic/v1/road?road_name='+urllib.parse.quote(road)+'&city='+urllib.parse.quote(city)+'&ak='+ak
    address = urllib.request.urlopen(url).read().decode("utf-8")
    address = json.loads(address)
    if address['status']==0:
        return address['description']
    else:
        return -1

