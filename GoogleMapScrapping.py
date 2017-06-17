#!/usr/bin/python
import argparse

__author__ = "Isa Bostan isabostan@gmail.com"

import re
import requests
from bs4 import BeautifulSoup as bs

class GoogleMapScrapping():
    def __init__(self,**kwargs):
        super(GoogleMapScrapping,self).__init__()
        p_args = argparse.ArgumentParser(description='Search results from Google maps')
        p_args.add_argument("--search","-S", action='store', dest='s_string', help="Search string ... \n\t $python GoogleMapScrapping -S Word2Search", type=str)
        self.args = p_args.parse_args()
        self.lnk = "https://www.google.com.tr/maps/search/"
        try:
            if self.args.s_string == None:
                self.args.s_string="Hospital"
            self.search(self.args.s_string)
        except ValueError as v:
            print("Value Error: "+str(v))

    def search(self, s_value):
        try:
            self.lnk +=str(s_value)
            r = requests.get(self.lnk)
            if r.status_code==200:
                soup = bs(r.text, "html.parser")
                scrpt= soup.find("script")
                for i in str(scrpt).split("\n"):
                    if re.search("^cacheResponse",i.strip()):
                        if re.search("\[\[\"0x",i.strip()):
                            val = i.strip().split("[[\"0x")
                            for k in range(1,len(val)):
                                laddr = ""
                                lname = val[k].split(",[")[0].split(",")[2]

                                if len(val[k].split(",[")[0].split(",")):
                                    for la in range(1,len(val[k].split(",[")[0].split(","))):
                                        if not lname == val[k].split(",[")[0].split(",")[la]:
                                            laddr += val[k].split(",[")[0].split(",")[la]
                                print("Location: "+str(lname)+"\n\tAddress: "+str(laddr)+"\n")

        except Exception as ex:
            print("Search Exception: "+str(ex))

if __name__ == "__main__":

    GoogleMapScrapping()

