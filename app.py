from flask import Flask,request,Response
import telegram
from bs4 import BeautifulSoup
import lxml
import requests
from urllib.request import Request, urlopen
from datetime import datetime

TOKEN = '#TOKEN PLACE'
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

def mysoup(myurl):
	url = myurl
	req = Request(url, headers={'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'})
	w = urlopen(req)
	myhtml = w.read()
	soup = BeautifulSoup(myhtml,"lxml")
	mydivs = soup.findAll('ul',class_='job_listings list')
	mylist=[]
	for ul in mydivs:
		for li in ul.findAll('li'):
			mylist.append(li)
	i =0
	mydict = {}
	kalo = []

	joblink = []
	title = []
	company = []
	country = []
	days = []
	perm = []

	for jal in mylist:
		for link in jal.findAll('a'):
			joblink.append(link.get('href'))
			arey = link.get_text()
			arey = arey.split('\n')
			title.append(arey[0])
			company.append(arey[1])
			country.append(arey[2])
			temp = arey[4]
			days.append(int(temp[9]))
			perm.append(temp[:9])

	mydict['link'] = joblink
	mydict['title'] = title
	mydict['company'] = company
	mydict['country'] = country
	mydict['days'] = days
	mydict['perm'] = perm
	return mydict

@app.route('/{}'.format(TOKEN),methods=['POST'])
def respond():
	if request.method == 'POST':
		msg = request.get_json()
		up = telegram.Update.de_json(msg,bot)
		try:
			c_id = up.message.chat.id
			m_id = up.message.message_id
		except:
			return Response('ok')
		text = up.message.text.encode('utf-8').decode()
		text = text.lower()
		f_name = up.message.chat.first_name
		url = 'https://workire.com/jobs'
		dic = mysoup(url)
		joblink = dic['link']
		title = dic['title']
		company = dic['company']
		country = dic['country']
		days = dic['days']
		perm = dic['perm']
		sp = text.split(' ')
		if(text=='/start'):
			to_send = """Hi {}, 
			This is gulf job posting bot. 
			Here is command List:

			command 'recent':
			recent -> gives list of jobs on main jobs page.
			
			recent n -> post the nth job from above list to group.

			recent n m l -> To post multiple jobs. n,m and l are job no in list

			command 'page':
			page n -> to pull jobs from nth page
			like page 2 to pull https://workire.com/jobs/page/2/

			page n k -> to post kth job on page n


			command 'cat':
			cat link header-> post titles of all jobs in link.
			To get the link use the filter on website
			the header of post will be header provided

			command 'mulcat':
			The format of the mul cat is:
				mulcat N link header
				where N is no of pages category occupies and link is link for that category. """.format(f_name)
			bot.sendMessage(chat_id=c_id, text=to_send)
			return Response('ok',status=200)
		elif sp[0]=='recent':
			temp = len(sp)
			if temp == 1:
				msg_t= "Following is list of  Jobs on recent page:\n"
				count = 0
				for i in title:
					count=count+1
					t = str(count)
					msg_t = msg_t + t
					msg_t = msg_t + '- '
					msg_t = msg_t + i
					msg_t = msg_t + '\nCountry: '
					msg_t = msg_t + country[count-1]
					msg_t = msg_t + '\n\n'
				msg_t= msg_t + "\nTo post a job send\nrecent n\nwhere n is number of job in above list.\nmultiple jobs cam be posted as\nrecent n m l\nwhere m,n,l are job number"
				bot.sendMessage(chat_id=c_id,text=msg_t)
				return Response('ok',status=200)
			else:
				for i in sp:
					if i=='recent':
						print("in recent")
					else:
						m_s = "Position: "
						try:
							te = int(i)-1
							m_s = m_s + '<b>'
							m_s = m_s + title[te]
							m_s = m_s + '</b>'
						except:
							bot.sendMessage(chat_id=c_id,text='Please follow command format')
							return Response('ok',status=200)
						m_s = m_s + "\nCompany: "
						m_s = m_s + company[te]
						m_s = m_s + "\nLocation: "
						m_s = m_s + country[te]
						m_s = m_s + "\n\nFor further information, and to apply, please visit our website: "
						m_s = m_s + joblink[te]
						m_s = m_s + "\n"
						m_s = m_s + "\nPost Date: "
						now = datetime.now()
						m_s = m_s + now.strftime("%d %b %Y")
						m_s = m_s + """\n\n#hiring #qatarjobs #middleeastjobs #uaejobs #saudijobs #omanjobs #kuwaitjobs #gulfjobs #engineeringjobs #ITjobs #accountingjobs #Teachingjobs #bahrainjobs #oilandgasjobs #Financejobs

Are you looking for a job in Gulf? 
Join our telegram channel and get verified job alerts.
https://t.me/gulfjobnews"""
						bot.sendMessage(chat_id=c_id,text="Posted")
						bot.sendMessage(chat_id='@gulfjobnews',text=m_s,parse_mode='HTML')
				return Response('ok',status=200)
		elif sp[0]=='page':
			temp = len(sp)
			if temp==1:
				t = "Please follow the format. \npage n"
				bot.sendMessage(chat_id=c_id,text=t)
				return Response('ok',status=200)
			elif temp==2:
				t = 'https://workire.com/jobs/page/{}/'.format(sp[1])
				try:
					dic = mysoup(t)
				except:
					bot.sendMessage(chat_id=c_id,text="Invalid page number. try again.")
					return Response('ok',status=200)
				title = dic['title']
				country = dic['country']
				msg_t= "Following is list of  Jobs on page {}:\n".format(sp[1])
				count = 0
				for i in title:
					count=count+1
					t = str(count)
					msg_t = msg_t + t
					msg_t = msg_t + '- '
					msg_t = msg_t + i
					msg_t = msg_t + '\nCountry :'
					msg_t = msg_t + country[count-1]
					msg_t = msg_t + '\n\n'
				msg_t= msg_t + "\nTo post a job send\npage n m\nwhere n is page number and m is job number\nmultiple jobs cam be posted as\nrecent n m l\nwhere n is page number and n,l are job number"
				bot.sendMessage(chat_id=c_id,text=msg_t)
				return Response('ok',status=200)
			elif temp>2:
				t = 'https://workire.com/jobs/page/{}/'.format(sp[1])
				dic = mysoup(t)
				title = dic['title']
				joblink = dic['link']
				company = dic['company']
				country = dic['country']
				days = dic['days']
				perm = dic['perm']
				count = 0
				print("\nHow you doing\n")
				for i in range(2,temp):
					print("\nI am there\n")
					m_s = "Position: "
					try:
						te = int(sp[i])-1
						m_s = m_s + '<b>'
						m_s = m_s + title[te]
						m_s = m_s + '</b>'
					except:
						bot.sendMessage(chat_id=c_id,text="Please choose valid job number.")
						return Response('ok',status=200)
					m_s = m_s + "\nCompany: "
					m_s = m_s + company[te]
					m_s = m_s + "\nLocation: "
					m_s = m_s + country[te]
					m_s = m_s + "\n\nFor further information, and to apply, please visit our website: "
					m_s = m_s + joblink[te]
					m_s = m_s + "\n"
					m_s = m_s + "\nPost Date: "
					now = datetime.now()
					m_s = m_s + now.strftime("%d %b %Y")
					m_s = m_s + """\n\n#hiring #qatarjobs #middleeastjobs #uaejobs #saudijobs #omanjobs #kuwaitjobs #gulfjobs #engineeringjobs #ITjobs #accountingjobs #Teachingjobs #bahrainjobs #oilandgasjobs #Financejobs

Are you looking for a job in Gulf? 
Join our telegram channel and get verified job alerts.
https://t.me/gulfjobnews"""
					bot.sendMessage(chat_id=c_id,text="Posted")
					bot.sendMessage(chat_id='@gulfjobnews',text=m_s,parse_mode='HTML')
				return Response('ok',status=200)
		elif sp[0]=='cat':
			temp = len(sp)
			if temp==1:
				bot.sendMessage(chat_id=c_id,text="Please use format \ncat link header")
				return Response('ok',status=200)
			elif temp>2:
				try:
					dic = mysoup(sp[1])
				except:
					t1 = "Invalid link. try again!"
					bot.sendMessage(chat_id=c_id,text=t1)
					return Response('ok',status=200)
				title = dic['title']
				msg_t = '<b>'
				for i in range(2,temp):
					msg_t = msg_t + sp[i].capitalize()
					msg_t = msg_t + " "
				msg_t = msg_t + '</b>'
				msg_t = msg_t + '\n\n'
				count = 0
				for i in title:
					count = count + 1
					msg_t = msg_t + str(count)
					msg_t = msg_t + '. '
					msg_t = msg_t + i
					msg_t = msg_t + '\n'
				msg_t = msg_t + "\nFor further information, and to apply, please visit our website: \n"
				msg_t = msg_t + sp[1]
				msg_t = msg_t + "\n"
				msg_t = msg_t + "\nPost Date: "
				now = datetime.now()
				msg_t = msg_t + now.strftime("%d %b %Y")
				msg_t = msg_t + """\n\n#hiring #qatarjobs #middleeastjobs #uaejobs #saudijobs #omanjobs #kuwaitjobs #gulfjobs #engineeringjobs #ITjobs #accountingjobs #Teachingjobs #bahrainjobs #oilandgasjobs #Financejobs

Are you looking for a job in Gulf? 
Join our telegram channel and get verified job alerts.
https://t.me/gulfjobnews"""
				bot.sendMessage(chat_id=c_id,text="Posted")
				bot.sendMessage(chat_id='@gulfjobnews',text=msg_t,parse_mode='HTML')
				return Response('ok',status=200)
			else:
				bot.sendMessage(chat_id=c_id,text="Please Follow the cat format!")
				return Response('ok',status=200)
		elif sp[0]=='mulcat':
			temp = len(sp)
			if temp==1:
				mystr = """" The format of the mul cat is:
				mulcat N link header
				where N is no of pages category occupies and link is link of category"""
				bot.sendMessage(chat_id=c_id,text=mystr)
			elif temp>1:
				try:
					page = int(sp[1])
				except:
					mystr = "N should be a number. type mulcat for more info"
					bot.sendMessage(chat_id=c_id,text=mystr)
					return Response('ok',status=200)
				temp = sp[2].replace('\n','').split('/')
				print(temp[4])
				muldic = {}
				titles = []
				for i in range(2,page+2):
					try:
						if i==2:
							url = 'https://workire.com/job-category/{}/'.format(temp[4])
						else:
							url = 'https://workire.com/job-category/{}/page/{}/'.format(temp[4],i-1)
						muldic[i-2] = mysoup(url)
					except:
						mystr = "Error detected. Wheter the page number is wrong or link.please check and try again"
						bot.sendMessage(chat_id=c_id,text=mystr)
						return Response('ok',status=200)
				msg = '<b>'
				count = 0
				for i in sp:
					if count >2:
						msg = msg + i.capitalize()
						msg = msg + ' '
					count = count+1
				msg = msg + '</b>'
				msg = msg + '\n\n'
				c = 0;
				for i in muldic:
					for j in muldic[i]['title']:
						c = c +1
						msg = msg + str(c)
						msg = msg + ". "
						msg = msg + j
						msg = msg + '\n'
				msg = msg + "\nFor further information, and to apply, please visit our website: \n"
				msg = msg + sp[2]
				msg = msg + "\n"
				msg = msg + "\nPost Date: "
				now = datetime.now()
				msg = msg + now.strftime("%d %b %Y")
				msg = msg + """\n\n#hiring #qatarjobs #middleeastjobs #uaejobs #saudijobs #omanjobs #kuwaitjobs #gulfjobs #engineeringjobs #ITjobs #accountingjobs #Teachingjobs #bahrainjobs #oilandgasjobs #Financejobs

Are you looking for a job in Gulf? 
Join our telegram channel and get verified job alerts.
https://t.me/gulfjobnews"""
				bot.sendMessage(chat_id='@gulfjobnews',text=msg,parse_mode='HTML')
				bot.sendMessage(chat_id=c_id,text='Posted')
				return Response('ok',status=200)
		else:
			temp="Unrecongnized command. Please /start again. and send right command!"
			bot.sendMessage(chat_id=c_id, text=temp)
			return Response('ok',status=200)
		return Response('ok',status=200)

@app.route('/',methods=['GET'])
def index():
	return '<h1>Gulf Job Bot</h1><h2>A telegram bot</h2><p>This bot is for posting jobs to a telegram channel.</p>'

if __name__ == '__main__':
	app.run(debug=True)
