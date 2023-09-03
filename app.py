from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.kalibrr.id/id-ID/job-board/te/data/1')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div',attrs={'class':'k-border-b k-border-t k-border-tertiary-ghost-color md:k-border md:k-overflow-hidden md:k-rounded-lg'})


row = table.find_all('div', attrs={'class':'k-grid k-border-tertiary-ghost-color k-text-sm k-p-4 md:k-p-6 css-1b4vug6'})
row_length = len(row)

temp = [] #initiating a 
#loop pages until pages 15
URL='https://www.kalibrr.id/id-ID/job-board/te/data/'
for data in range(1,16):
    url = requests.get(URL + str(data) + '/')
    soup = BeautifulSoup(url_get.content,"html.parser")
    table = soup.find('div',attrs={'class':'k-border-b k-border-t k-border-tertiary-ghost-color md:k-border md:k-overflow-hidden md:k-rounded-lg'})
    for i in range(0, row_length):
        
        #begin scrapping process

        #get job_title
        job_title = table.find_all('a',href=True, attrs={'class':'k-text-primary-color'})[i].text

        #get job_location
        job_location = table.find_all('a',href=True, attrs={'class':'k-text-subdued k-block'})[i].text
    
        #get job_postdate
        job_postdate = table.find_all('span', attrs={'class':'k-block k-mb-1'})[i].text.split('•')[0]

        #get job_deadline
        job_deadline = table.find_all('span', attrs={'class':'k-block k-mb-1'})[i].text.split('• ')[1]

        #get company
        job_company = table.find_all('span', attrs={'class':'k-inline-flex k-items-center k-mb-1'})[i].text
        
        temp.append((job_title,job_location,job_postdate,job_deadline,job_company))
#change into dataframe
jobs = pd.DataFrame(temp,columns=('job_title', 'job_location','job_postdate','job_deadline','job_company'))
jobs
#insert data wrangling here
jobs['job_location',] = jobs['job_location'].astype('category') 
jobs_locgrouped = jobs.groupby('job_location').count()[['job_title']].sort_values(by='job_title',ascending=True)
jobs_locgrouped['frequency'] = jobs.groupby('job_location').count()[['job_title']].sort_values(by='job_title',ascending=True)
jobs_locgroupedfreq = jobs_locgrouped[['frequency']]


#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{jobs_locgroupedfreq["frequency"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = jobs_locgroupedfreq.plot.barh(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)