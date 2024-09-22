# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 14:46:46 2024

@author: Jason
"""

import requests
import time
import yaml
import sys

def load_input_file(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def check_endpoint(endpoint):
    url = endpoint.get("url")
    
    start_time = time.time()
    
    try:
        r = requests.request("GET", url, timeout=0.5)                 #500ms timeout, we are measuring in s
        latency = (time.time() - start_time) * 1000                 #convert time to ms
        if (200 <= r.status_code < 300) and latency < 500:          #if status code is 2xx and latency < 500ms, return UP (True)      
            return True
    except requests.RequestException:
        pass
    return False
        
def log_availability(domains):
    for domain, stats in domains.items():
        up_count, total_count = stats
        availability = round(100 * up_count / total_count)
        print(f"{domain} has {availability}% availability percentage")

def monitor_endpoints(config_file):
    endpoints = load_input_file(config_file)
    domain_stats = {}                                               #{domain name : [up_count, total_count]}
    
    while True:
        for endpoint in endpoints:
            url = endpoint["url"]
            domain = url.split('/')[2]           #domain name, split at https://domainname.com/etc
            
            if domain not in domain_stats:
                domain_stats[domain] = [0, 0]
            
            domain_stats[domain][1] += 1                        #increment total count
            if check_endpoint(endpoint):
                domain_stats[domain][0] +=1                     #if domain is up, increment up count
    
        log_availability(domain_stats)
        
        time.sleep(15)

if __name__ == "__main__":
    #config_file = "sample_input.yml"                                #Replace sample_input.yml with path to yml file
    config_file = sys.argv[1]
    monitor_endpoints(config_file)

#monitor_endpoints("sample_input.yml")
