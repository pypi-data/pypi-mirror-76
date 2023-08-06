import requests

class API(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base = 'http://strainapi.evanbusse.com' # i dont think https works
    
    @property
    def endpoint(self):
        return f'{self.base}/{self.api_key}'
    
    def all_effects(self):
        '''List all effects and their type'''
        return requests.get(f'{self.endpoint}/searchdata/effects').json()
    def all_flavors(self):
        '''List all flavors'''
        return requests.get(f'{self.endpoint}/searchdata/flavors').json()
    
    def all_strains(self):
        '''Returns all strains. Use sparingly, as it uses a lot of data'''
        return requests.get(f'{self.endpoint}/strains/search/all').json()
    
    def by_name(self, name):
        return requests.get(f'{self.endpoint}/strains/search/name/{name}').json()
    def by_race(self, race):
        '''sativa, indica, hybrid'''
        return requests.get(f'{self.endpoint}/strains/search/race/{race}').json()
    def by_effect(self, effect):
        return requests.get(f'{self.endpoint}/strains/search/effect/{effect}').json()
    def by_flavour(self, flavour):
        return requests.get(f'{self.endpoint}/strains/search/flavour/{flavour}').json()
    
    def description(self, strain_id):
        return requests.get(f'{self.endpoint}/strains/data/desc/{strain_id}').json()
    def effects(self, strain_id):
        return requests.get(f'{self.endpoint}/strains/data/effects/{strain_id}').json()
    def flavors(self, strain_id):
        return requests.get(f'{self.endpoint}/strains/data/flavors/{strain_id}').json()