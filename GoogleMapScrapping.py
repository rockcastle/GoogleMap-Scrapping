#!/usr/bin/python
import argparse
import json
import traceback
import requests

__author__ = "Isa Bostan isabostan@gmail.com"


latitude = None  # Set this if IP location lookup does not work for you (must be a string)
longitude = None
api_key= ""
plc_ids = []

class GoogleMapScrapping():
    def __init__(self,**kwargs):
        super(GoogleMapScrapping,self).__init__()
        p_args = argparse.ArgumentParser(description='Search results from Google maps')
        p_args.add_argument("--search","-S", action='store', dest='s_string', help="Search string ... \n\t $python GoogleMapScrapping -S Word2Search", type=str)
        self.args = p_args.parse_args()
        self.lnk = "https://maps.googleapis.com/maps/api/place/radarsearch/json?radius=5000&key="
        try:
            if api_key=="":
                print("Please set your api key..")
                exit()
            else:
                self.lnk += api_key
            if self.args.s_string == None:
                self.args.s_string="hospital"
                self.kword= "health"#&keyword=health
                self.lnk += "&type="+self.args.s_string+"&keyword="+self.kword

            self.get_lat_lon()
        except ValueError as v:
            print("Value Error: "+str(v))

    def search(self):
        try:
            for i in plc_ids:
                lnk1 = "https://maps.googleapis.com/maps/api/place/details/json?key=" + api_key+"&placeid="+str(i)
                print()
                print(lnk1)
                r = requests.get(lnk1)
                if r.status_code==200:
                    place = json.loads(r.text)
                    if "formatted_phone_number" in place["result"].keys():
                        phone=""
                        if len(place["result"]["formatted_phone_number"]):
                            phone = place["result"]["formatted_phone_number"]
                            #if re.search("\W",phone):
                            #    phone = re.sub("\W"," ",phone)
                    else:
                        phone = "Not available"

                    if "formatted_address" in place["result"].keys():
                        adr=""
                        if len(place["result"]["formatted_address"]):
                            adr = place["result"]["formatted_address"]
                    else:
                        adr = "Not available"

                    if "website" in place["result"].keys():
                        webs=""
                        if len(place["result"]["website"]):
                            webs = place["result"]["website"]
                    else:
                        webs = "Not available"
                    print(str(place["result"]["name"])+"\n\tPhone: "+str(phone)+"\n\tAddress: "+str(adr)+"\n\tWebsite: "+str(webs))

        except Exception as ex:
            print("Search Exception: "+str(ex))

    def get_ip(self):
        try:
            ip_url = "http://jsonip.com/"
            req = requests.get(ip_url)
            if req.status_code == 200:
                ip_json = json.loads(req.text)
                return ip_json['ip']
        except requests.ConnectionError as e:
            traceback.print_exc()
            return "Error: %s. Cannot get ip." % e

    def get_lat_lon(self):
        try:
            #self.get_ip()
            if latitude is None and longitude is None:
                # get location
                location_req_url = "http://freegeoip.net/json/%s" % self.get_ip()
                r = requests.get(location_req_url)
                if r.status_code == 200:
                    location_obj = json.loads(r.text)
                    lon = location_obj["longitude"]
                    lat = location_obj["latitude"]
                    self.lnk += "&location="+str(lat)+","+str(lon)

                    r.close()
                else:
                    r.close()
                    pass

                r1 = requests.get(self.lnk)
                if r1.status_code==200:
                    plc_ids.clear()
                    place_ids = json.loads(r1.text)
                    for k in place_ids["results"]:
                        plc_ids.append(k["place_id"])
                if len(plc_ids):
                    self.search()
                else:
                    r1.close()
                    print("No place found")
                    exit()


        except Exception as e:
            print("Not connect: " + str(e))

if __name__ == "__main__":

    GoogleMapScrapping()
