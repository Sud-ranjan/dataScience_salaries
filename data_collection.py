import scraper_glassdoor as sc
import pandas as pd


path = "/usr/local/bin/chromedriver"
df = sc.get_jobs('data scientist',5,False,path,5)

