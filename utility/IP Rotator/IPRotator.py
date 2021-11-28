'''this is the new version'''

import requests
from bs4 import BeautifulSoup
# from collections import deque
import multiprocessing as mp
import random
import json
import os
import logging
from datetime import datetime

# start logging
if not os.path.exists('./logs'):
    # if logs dir does not exist, create
    os.mkdir('logs')
logging.basicConfig(filename='logs/IPRotator.log', encoding='utf-8', level=logging.DEBUG)
logging.debug('imported: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%m:%S')))
            
class IPRotator():
    '''
    Class to help rotate IPs
    
    Attributes
    ----------
    `proxies`: Queue`
        list of proxies (stored as str with format - `<ip address>:<port>`)

    Methods
    -------
    `get_proxy_list()`
        gets free proxies from websites
    `get_proxy(url=None)`
        sends a request with a proxy address to the given url
    `refresh_proxies()`
        refreshes with new set of proxies 
    '''

    # constant attributes
    REFERRERS = [
        "https://duckduckgo.com/",
        "https://www.google.com/",
        "http://www.bing.com/",
        "https://in.yahoo.com/"
    ]

    UA_FILE = './user_agents.json'

    def __init__(self, ua_file=None):
        if ua_file:
            self.UA_FILE = ua_file
        self.proxies = self.get_proxy_list()
        # read user_agents from file
        self.user_agents = self.read_user_agents_file()
    
    def get_referrer(self):
        '''randomly returns a referrer url'''
        return self.REFERRERS[random.randint(0, len(self.REFERRERS))]

    @staticmethod
    def get_proxy_list():
            '''returns Queue of proxies available

            Returns:
                Queue: list of proxies (stored as str with format - `<ip address>:<port>`)
            '''
            logging.info('{} start: get_proxy_list'.format(os.getpid()))
            def parse_table(proxy_list_url):
                req = requests.get(proxy_list_url)
                req.raise_for_status()

                soup = BeautifulSoup(req.content, 'html.parser')
                proxy_table = soup.find('table', {'class': ['table-striped']})
                headers = [th.text.lower() for th in proxy_table.find_all('th')]

                proxies_list = []
                # skip first row of proxy table (headers)
                for row in proxy_table.find_all('tr')[1:]:
                    cells = [td.text for td in row.find_all('td')]
                    proxies_list.append(dict(zip(headers, cells)))
                # only use proxies with https=yes
                proxies = [p for p in proxies_list if p['https'].strip().lower()=='yes']
                proxies = ["{}:{}".format(plr['ip address'], plr['port']) for plr in proxies]
                return proxies

            proxies = []
            proxy_sites = ['https://free-proxy-list.net', 'https://sslproxies.org']
            [proxies.extend(parse_table(url)) for url in proxy_sites]
            proxies_Q = mp.Queue()
            for proxy in set(proxies):
                proxies_Q.put(proxy)
            return proxies_Q

    def get_proxy(self, url=None, gen_header=False):
        '''goes through proxies and returns any usable proxies and response, returns none if NA

        Parameters:
            url::str
                url to test proxy with; if there is no url, 1st proxy dict is returned;
                if there is url, response with first usable proxy returned
                default = None
            gen_header::bool
                to get a random request header to use with proxy
                default = False

        Returns:
            dict: proxy in http and https
            requests.Response object: response object from request to url with proxy
        '''
        logging.info('{} start: get_proxy(url={}, gen_header={})'.format(os.getpid(), url, gen_header))
        # if need header, get one
        if gen_header:
            send_header = self.get_header()

        # check if proxies is empty, if yes, refresh proxies
        if self.proxies.empty(): self.refresh_proxies()
        while not self.proxies.empty():
            proxy = self.proxies.get()
            try:
                proxy_dict = {"http": "http://"+proxy, "https": "https://"+proxy}
                # res = requests.get('https://httpbin.org/ip', proxies=proxy_dict, timeout=15)
                # if there is an url input
                if url:
                    if gen_header:
                        res = requests.get(url, proxies=proxy_dict, headers=send_header,timeout=10)
                    else:
                        res = requests.get(url, proxies=proxy_dict, timeout=10)
                    return proxy_dict, res
                else:
                    # if there is no url input
                    return proxy_dict, None
            except Exception as exc:
                logging.info('{} get_proxy error {} :: skipping proxy {}'.format(os.getpid(), exc.__class__.__name__, proxy))
                pass
        # empty proxies
        return None, None

    def refresh_proxies(self):
        '''re-retrieve proxies'''
        logging.info('{} refresh_proxies'.format(os.getpid()))
        self.proxies = self.get_proxy_list()

    def read_user_agents_file(self):
        '''return list of user agent strings if user_agents.json exists'''
        logging.info('{} read_user_agents_file'.format(os.getpid()))
        user_agents = []
        if os.path.isfile(self.UA_FILE):
            json_content = json.load(open(self.UA_FILE, 'r'))
            user_agents = json_content['user_agents']
        else:
            user_agents, export_file_name = self.scrap_user_agents()
            self.UA_FILE = export_file_name
        return user_agents

    @staticmethod
    def scrap_user_agents(export_file_name='./user_agents.json'):
        '''saves list of user agents to a json file'''
        logging.info('{} scrap_user_agents'.format(os.getpid()))
        UA_LINKS = [
            'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/windows/',
            'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/windows/2',
            'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/linux/',
            'https://developers.whatismybrowser.com/useragents/explore/software_name/safari/',
            'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/chrome-os/',
            'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/ios/',
            'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/mac-os-x/'
        ]
        user_agents = []
        for url in UA_LINKS:
            req  = requests.request('get', url)
            req.raise_for_status
            soup = BeautifulSoup(req.content, 'html.parser')

            try:
                ua_table = soup.find('table', {'class': ['listing-of-useragents']})
                ua_table_rows = ua_table.find_all('tr')
                ua_cells = [row.find_all('td')[0] for row in ua_table_rows if len(row.find_all('td')) > 0]
                ua = [cell.find('a').text.strip() for cell in ua_cells if cell.find('a')]
                user_agents.extend(ua)
            except:
                continue
        
        # save user agent strings to file
        with open(export_file_name, 'w') as json_file:
            json.dump({'user_agents': user_agents}, json_file, indent=4)
        
        return user_agents, export_file_name

    def get_header(self):
        '''randomly put together a header'''
        logging.info('{} get_header started'.format(os.getpid()))
        user_agent = self.user_agents[random.randint(0, len(self.user_agents))]
        referer = self.REFERRERS[random.randint(0, len(self.REFERRERS))]
        header = {
            'user-agent': user_agent,
            'referer': referer
        }
        logging.info('{} get_header: header = {}'.format(os.getpid(), header))
        return header