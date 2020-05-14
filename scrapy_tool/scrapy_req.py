from scrapy import Spider
from scrapy.selector import Selector
import requests
from bs4 import BeautifulSoup

class My_Spider(Spider):
    name = "scrap Footballer (Coach)"
    url = "https://www.premierleague.com/clubs/1/Arsenal/directory.html"
    protocol = "http"
    url = 'https://www.premierleague.com/tables'
    
    def parseCoach(self):
        resp = requests.get('https://www.premierleague.com/clubs/1/Arsenal/directory')
        sel = Selector(resp)
        res = sel.xpath('//section[@class="clubDirectory"]/div[2]/div[3]/div[3]/div[1]/div[1]/div[2]/p/text()').get()
        return res
        
    def parseTeamPos(self):
        resp = requests.get('https://www.premierleague.com/tables')
        values = {
            'pos':'N/A',
            'wins':'N/A',
            'loss':'N/A',
            'tots':'N/A'
        }
        sel = Selector(resp)
        pos = sel.xpath('/html[1]/body[1]/main[1]/div[2]/div[4]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[@data-filtered-table-row-name="Arsenal"]/td[2]/span[1]/text()').get()
        win = sel.xpath('/html[1]/body[1]/main[1]/div[2]/div[4]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[@data-filtered-table-row-name="Arsenal"]/td[5]/text()').get()
        los = sel.xpath('/html[1]/body[1]/main[1]/div[2]/div[4]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[@data-filtered-table-row-name="Arsenal"]/td[7]/text()').get()
        tots = sel.xpath('/html[1]/body[1]/main[1]/div[2]/div[4]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[@data-filtered-table-row-name="Arsenal"]/td[11]/text()').get()
        values.update({'pos':pos})
        values.update({'wins':win})
        values.update({'loss':los})
        values.update({'tots':tots})
        return values
        
    def teamInfo(self):
        resp = requests.get('https://www.soccerbase.com/teams/team.sd?team_id=142')
        values = {
            'name':'N/A',
            'stadium':'N/A',
            'manager':'N/A',
            'Year':'N/A',
            'aka':'N/A',
            'chairman':'N/A'
        }
        sel = Selector(resp)
        name = sel.xpath('/html/body/div[2]/div[4]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr[3]/td/div/table/tbody/tr/td/text()').get()
        stadium = sel.xpath('/html/body/div[2]/div[4]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr[2]/td[1]/strong[1]/text()').get()
        manager = sel.xpath('/html/body/div[2]/div[4]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr[3]/td[1]/strong/text()').get()
        aka = sel.xpath('/html/body/div[2]/div[4]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr[1]/td[1]/strong[1]/text()').get()
        year = sel.xpath('/html/body/div[2]/div[4]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr[4]/td/strong/text()').get()
        chairman = sel.xpath('/html/body/div[2]/div[4]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr[5]/td/strong/text()').get()
        city = sel.xpath('/html/body/div[2]/div[4]/div[1]/div[3]/div[1]/div[1]/div[2]/table[1]/tr[3]/td/strong/text()').get()
        values.update({"name":name})
        values.update({"stadium":stadium})
        values.update({"manager":manager})
        values.update({"aka":aka})
        values.update({"year":year})
        values.update({"chairman":chairman})
        values.update({"city":city})
        
        return values
        
    def caronaInfo(self):
        resp = requests.get('https://www.worldometers.info/coronavirus/')
        values = {
            'world':'N/A',
            'india':'N/A',
            'deathCases':'N/A',
            'recCases':'N/A',
            'newCases':'N/A',
            'totalDeath':'N/A',
            'totalRec':'N/A'
        }
        sel = Selector(resp)
        soup = BeautifulSoup(sel.get(),"html.parser")
        world = soup.find(id="main_table_countries_today").find("td",string="World").parent.td.next_sibling.next_sibling.string
        india = soup.find(id="main_table_countries_today").find("a",string="India").parent.parent.td.next_sibling.next_sibling.string
        deathCases = soup.find(id="main_table_countries_today").find("a",string="India").parent.parent.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string
        recCases = soup.find(id="main_table_countries_today").find("a",string="India").parent.parent.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string
        newCases = soup.find(id="main_table_countries_today").find("a",string="India").parent.parent.td.next_sibling.next_sibling.next_sibling.next_sibling.string
        totalDeath = soup.find_all(id="maincounter-wrap")[1].span.string
        totalRec = soup.find_all(id="maincounter-wrap")[2].span.string
        
        values.update({"world":world})
        values.update({"totalDeath":totalDeath})
        values.update({"totalRec":totalRec})
        values.update({"india":india})
        values.update({"deathCases":deathCases})
        values.update({"recCases":recCases})
        values.update({"newCases":newCases})
        
        return values
        
    def parseTemp(self):
        res = requests.get('https://api.weatherbit.io/v2.0/current?city=Mumbai,IN&key=7f0a8ccd238f4fbd9327aafab0ba171f')
        
        data = res.json()
        values = {
            'temp':'N/A',
            'press':'N/A',
            'place':'N/A',
            'clouds':'N/A',
            'wind_speed':'N/A',
            'wind_dir':'N/A',
            'slp':'N/A',
            'ob_time':'N/A'
        }
        
        temp = data['data'][0]['temp']
        press = data['data'][0]['pres']
        place = data['data'][0]['city_name']
        clouds = data['data'][0]['weather']['description']
        wind_speed = data['data'][0]['wind_spd']
        wind_dir = data['data'][0]['wind_cdir_full'].title()
        slp = data['data'][0]['slp']
        ob_time = data['data'][0]['ob_time']
        values.update({"place":place})
        values.update({"temp":temp})
        values.update({"press":press})
        values.update({"clouds":clouds})
        values.update({"wind_speed":wind_speed})
        values.update({"wind_dir":wind_dir})
        values.update({"slp":slp})
        values.update({"ob_time":ob_time})
        return values