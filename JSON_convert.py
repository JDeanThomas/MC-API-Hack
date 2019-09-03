#!/usr/bin/env python3

import sys
import json 
import csv
 
def JSON_to_CSV(filename):
    f = open(filename)
    members = json.load(f)
    f.close()

    f = csv.writer(open("Members.csv", "w+"))

    f.writerow(["prefix", "company", "x-api-uri", "lastname", "mcrecordtype", 
                "datecreated", "datelastupdated", "mcaccountstatus", "mcaccounttype", 
                "professionalsuffix", "suffix", "firstname", "middlename", "membernumber"])


    for member in members['members']:
        #print(member)
        f.writerow([member["prefix"], member["company"], member["x-api-uri"],
                    member["lastname"], member["mcrecordtype"],
                    member["datecreated"], member["datelastupdated"], 
                    member["mcaccountstatus"], member["mcaccounttype"],
                    member["professionalsuffix"], member["suffix"], member["firstname"],
                    member["middlename"], member["membernumber"]])


if __name__ == '__main__':
    """ 
    Run file as standalone script
    """
    if sys.stdin.isatty():
        filename = sys.argv[-1]
        JSON_to_CSV(filename)