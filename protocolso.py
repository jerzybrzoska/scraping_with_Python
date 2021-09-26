#!/usr/bin/python3

import datetime
import requests
import json

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
#from selenium.webdriver.chrome.options import Options

#options = Options()

#options.add_argument("--headless")
path = "/usr/local/bin/chromedriver"
#driver = webdriver.Chrome(path, options=options)
driver = webdriver.Chrome(path)


driver.implicitly_wait(10)

def bitnodes():
    driver.get("https://bitnodes.io/")
    #Our target is to get this element <t class="text-center"><h2><a href="/nodes/">11431 nodes</a></h2></td>
    wait = WebDriverWait(driver,30)
    
    option = wait.until(EC.presence_of_element_located((By.XPATH,"//table[@class='table table-condensed total-nodes']//a[@href='/nodes/']")))
    option = int(option.text.replace(" NODES", "", 1))
    return(option)
    

def lighningnodes():
    driver.get("https://1ml.com/statistics")
#Our target <div class="col-md-3"><div class="panel panel-default"><div class="panel-heading"><h2 class="panel-title">Number of Nodes</h2></div>
#<div class="panel-body"><div class="content oneLine">27,144<span class="small"><span class="icon icon-arrow-up numberIncrease">+5.45%</span></span></div>
                 
    wait = WebDriverWait(driver,30)
    
    option = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='content oneLine']")))
    #option = int(option.text.replace(",", "", 1))
    option = option.text.replace(",", "", 1).replace(" +", "", 1)
    suffix = re.compile(r"[0-9]{1}\.[0-9]{2}%$")
    option = int(re.sub(suffix, "", option))
    return(option)
    
def lcapacity():
    driver.get("https://1ml.com/statistics")
#Our target <div class="col-md-3"><div class="panel panel-default"><div class="panel-heading"><h2 class="panel-title">Layer 1 Capacity Ratio</h2></div>
#<div class="panel-body"><div class="content oneLine large">0.013829%</div> #this div is the second (out of seven) occurrence of this this class in the entire page
                 
    wait = WebDriverWait(driver,30)
    option = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='col-md-3'][3]//div[@class='content oneLine large']")))#selenium.common.exceptions.TimeoutException: Message:
    option = option.text
    return(option)
   

def dnodes():
    driver.get("https://blockchair.com/dogecoin/nodes")
    #Our target is to get this element <h3 class="h4 mb-10">Total nodes: 1,581</h3>
    wait = WebDriverWait(driver,30)
    
    option = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='nodes_chain']/div[1]/h3")))
    option = int(option.text.replace("Total nodes: ", "", 1).replace(",", "", 1))
    return(option)
    


def lnodes():
    driver.get("https://blockchair.com/litecoin/nodes")
    #Our target is to get this element <h3 class="h4 mb-10">Total nodes: 1,581</h3>
    wait = WebDriverWait(driver,30)
    
    option = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='nodes_chain']/div[1]/h3")))
    option = int(option.text.replace("Total nodes: ", "", 1).replace(",", "", 1))
    return(option)
    
   
def bcnodes():
    driver.get("https://blockchair.com/bitcoin-cash/nodes")
    #Our target is to get this element <h3 class="h4 mb-10">Total nodes: 1,581</h3>
    wait = WebDriverWait(driver,30)
    
    option = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='nodes_chain']/div[1]/h3")))
    option = int(option.text.replace("Total nodes: ", "", 1).replace(",", "", 1))
    return(option)


def xmrnodes():
    driver.get("https://monerohash.com/nodes-distribution.html")
    try:
        nodes = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "total-nodes")))
        nodes = int(nodes.text)
        return(nodes)
        #return(nodes)

    finally: 
        driver.quit()#Closes the tab even when return is executed 
        
bn = bitnodes()
lightn = lighningnodes()
lightnbn = str('{0:.1f}'.format((lightn)/bn))

lncp = lcapacity()


dn = dnodes()
dnbnp = str('{0:.2f}'.format((dn*100)/bn))

liten = lnodes()
litenbnp = str('{0:.2f}'.format((liten*100)/bn))
bcn = bcnodes()
bcnbnp = str('{0:.2f}'.format((bcn*100)/bn))
xn = xmrnodes()
xnbnp = str('{0:.2f}'.format((xn*100)/bn))


result = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cdogecoin%2Cbitcoin-cash%2Clitecoin%2Cmonero&vs_currencies=btc&include_market_cap=true", headers = {"accept":"application/json"})

dtb = result.json()["dogecoin"]["btc_market_cap"] / result.json()["bitcoin"]["btc_market_cap"]
dtbp = str('{0:.2f}'.format(dtb * 100))


ltb = result.json()["litecoin"]["btc_market_cap"] / result.json()["bitcoin"]["btc_market_cap"]
ltbp = str('{0:.2f}'.format(ltb * 100))
bctb = result.json()["bitcoin-cash"]["btc_market_cap"] / result.json()["bitcoin"]["btc_market_cap"]
bctbp = str('{0:.2f}'.format(bctb * 100))
xtb = result.json()["monero"]["btc_market_cap"] / result.json()["bitcoin"]["btc_market_cap"]
xtbp = str('{0:.2f}'.format(xtb * 100))

print(f"Bitcoin Lightning's number of nodes is {lightn}, which is {lightnbn} times more than that of Bitcoin's {bn} nodes.")
print(f"Bitcoin Lightning's capacity is {lncp} of that of the total 21 mln of Bitcoin.")
print(f"Dogecoin's market cap is {dtbp}% of that of Bitcoin, whereas its number of nodes is {dn}, which is {dnbnp}% of that of Bitcoin's {bn} nodes.")
print(f"Litecoin's market cap is {ltbp}%% of that of Bitcoin, whereas its number of nodes is {liten}, which is {litenbnp}% of that of Bitcoin's {bn} nodes.")
print(f"Bitcoin Cash's market cap is {bctbp}%% of that of Bitcoin, whereas its number of nodes is {bcn}, which is {bcnbnp}% of that of Bitcoin's {bn} nodes.")
print(f"Monero's market cap is {xtbp}%% of that of Bitcoin, whereas its number of nodes is {xn}, which is {xnbnp}% of that of Bitcoin's {bn} nodes.")


#options = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='nodes_chain']//h3")))
# First option
#print(options[0].text)

# All the options
#for opt in options:
    #print(opt.text)



#https://www.youtube.com/watch?v=Xjv1sY630Uc
#https://selenium-python.readthedocs.io/getting-started.html
#https://selenium-python.readthedocs.io/navigating.html
#https://selenium-python.readthedocs.io/waits.html
#https://stackoverflow.com/questions/69320581/unable-to-locate-element-by-class-name-using-selenium-via-python-why-so



#time.sleep(10)#waiting for 10 seconds works just as well and requires less importing
#nodes = driver.find_element_by_id("total-nodes")#<p>Total nodes: <span id="total-nodes"></span> - Last updated: <span id="last-updated"></span></p>
#It gives me <selenium.webdriver.remote.webelement.WebElement (session="638cf52945970dcf44fb98faadad4916", element="d8a62805-f7c3-49d1-91cc-69244aed4468")> 
#if I don't wait log enough, e.g. 10 seconds
    
