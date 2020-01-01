import requests
from bs4 import BeautifulSoup as bs
import pymysql

db = pymysql.connect("localhost","root","a123456",charset="utf8")
cursor = db.cursor()
page = 1
back_flag = True
url = "https://www.ptt.cc/bbs/index.html"
baseurl = "https://www.ptt.cc/"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
payload = {
'from':'/bbs/Gossiping/index.html',
'yes':'yes'}
cookies = {'over18':'1'}
params = {'q':None,
'page':str(page)}
soup_list = []
tp_set = set()
rs = requests.session()
res = rs.post(baseurl + '/ask/over18', verify=False, data=payload)

tp_dict = {}
result = {}

# 探訪首頁
def fresh_list():
	page = 1
	res = rs.get(baseurl + 'bbs/index.html', headers=headers, verify=False)
	res.encoding = "utf-8"
	html = res.text
	soup = bs(html,'lxml')
	# print(soup)
	url_list = []
	url_li = soup.find_all('a')
	url_li = url_li[5:]
	for url in url_li[:51]:
		url_list.append(url['href'])
	# print(url_list)
	name_list = soup.find_all('div', attrs={'class':'board-name'})
	class_list = soup.find_all('div', attrs={'class':'board-class'})
	title_list = soup.find_all('div', attrs={'class':'board-title'})
	
	for num, (n, c, t) in enumerate(zip(name_list[:30], class_list[:30], title_list[:30])):
		num += 1
		n = n.text
		c = c.text
		t = t.text
		tp_dict[num] = n
		print('%2d %15s %5s %s' %(num,n,c,t))
	# try:
	tp = input('請輸入想搜索的看板:')
	if tp == 'q':
		print('q')
		back_flag = False
	elif tp == '0':
		print('0')
		fresh_list()
	elif not tp.isdigit():
		print('not digit')
		fresh_list()	
	else:
		tp = int(tp)
		# result, soup, url= fresh_list()

# 進入看板，搜尋關鍵字
# def show_allmenu():
	# tp_dict = fresh_list()
	if tp in tp_dict.keys():
		print('進入', tp_dict[int(tp)],'版')
		xx = tp_dict[int(tp)]
		tp_set.add(xx)
		key = input("請輸入想搜尋的關鍵字:")
		params['q'] = key
		global urls
		urls = baseurl + 'bbs/' + tp_dict[tp] + '/search?'
		res = rs.get(urls, headers=headers, verify=False, cookies=cookies, params=params)
		res.encoding = "utf-8"
		html = res.text
		soup = bs(html,'lxml')
		soup_list.append(soup)
		titles = soup.find_all('div',attrs={'class':'title'})
		authors = soup.find_all('div',attrs={'class':'author'})
		dates = soup.find_all('div',attrs={'class':'date'})
		# all_con = []
		empty = []
		for num, title in enumerate(titles):
			title = title.text.strip('\n').split()
			# all_con.append([num, (titles[num], authors[num], dates[num])])
			a = '(本文已被刪除)' in title
			if a:
				empty.insert(0, num)
		for emp in empty:
			del titles[emp], authors[emp], dates[emp]
		for num, (title, author, date) in enumerate(zip(titles, authors, dates)):
			num = num + 1
			title = title.text.strip('\n')
			author = author.text.strip('\n')
			date = date.text.strip('\n')
			result[num] = [title,author,date]
			print('%2d %-20s %-10s %-5s' %(num, title, author, date))
		# return soup, url

def do_page():
	res = rs.get(urls, headers=headers, verify=False, cookies=cookies, params=params)
	res.encoding = "utf-8"
	html = res.text
	soup = bs(html,'lxml')
	soup_list.append(soup)
	titles = soup.find_all('div',attrs={'class':'title'})
	authors = soup.find_all('div',attrs={'class':'author'})
	dates = soup.find_all('div',attrs={'class':'date'})
	for num, title in enumerate(titles):
		title = title.text.strip('\n').split()
		a = '(本文已被刪除)' in title
		if a:
			del titles[num], authors[num], dates[num]
	for num, (title, author, date) in enumerate(zip(titles, authors, dates)):
		num = num + 1
		title = title.text.strip('\n')
		author = author.text.strip('\n')
		date = date.text.strip('\n')
		result[num] = [title,author,date]
		print('%2d %-20s %-10s %-5s' %(num, title, author, date))
	print('正在瀏覽第%2s頁' %params['page'])
	# print(url, page)
	# return soup


fresh_list()
# tp_board = list(tp_set)[-1]
# c_tab = "create table if not exists " + tp_board + "(title varchar(255), url varchar(50))charset=utf8"
# ins = "insert into " + tp_board + "(title,url) values(%s,%s)"

while back_flag:
	numbers = len(result)
	url_list = []
	soup = soup_list[-1]
	search = soup.select('.r-ent')
	for s in search:
		s = s.find_all('a')
		for r in s:
			href = r['href']
			if 'search' in href:
				continue
			if 'author' in href:
				continue
			url_list.append(href)
	# print(url_list)
	nums = result.keys()
	datas = result.values()
	# print(datas)
	for num, data, i_url in zip(nums, datas, url_list):
		result[num] = [data, i_url]

	input_test = input('請輸入要查看的文章(1~%d)?下一頁(n)上一頁(l) quit(q) research(r) 回首頁(h)' %numbers)
	tp_board = list(tp_set)[-1]
	c_tab = "create table if not exists " + tp_board + "(title varchar(255), url varchar(255))charset=utf8"
	ins = "insert into " + tp_board + "(title,url) values(%s,%s)"

	if input_test.isdigit():
		input_test = int(input_test)
	if input_test in result.keys():
		# for url in url_list:
		urll = baseurl + url_list[input_test - 1]
		res = rs.get(urll,headers=headers, verify=False, cookies=cookies)
		res.encoding = "utf-8"
		html = res.text
		soup = bs(html,'lxml')
		search = soup.find_all('div',attrs={'id':'main-content'})
		print(search[0].text)
		que = input('是否存入數據庫(y/n)?')
		if que == 'y':
			L = [result[input_test][0][0], "https://www.ptt.cc/" + url_list[input_test - 1]]
			cursor.execute("create database if not exists pttdb")
			cursor.execute("use pttdb")
			cursor.execute(c_tab)
			cursor.execute(ins,L)
			db.commit()
		input("按輸入鍵繼續:")
		do_page()
	elif input_test == 'q':
		print('爬取結束!!感謝使用')
		cursor.close()
		db.close()
		back_flag = False

	elif input_test == 'n':
		print('')
		if len(result) < 15:
			print('已經是最後一頁了!')
			print('')
		page += 1
		params['page'] = str(page)
		do_page()

	elif input_test == 'h':
		params['page'] = 1
		fresh_list()

	elif input_test == 'l':
		page -= 1
		print('')
		if page < 1:
			print('已經是第一頁了!!')
			print('')
			page = 1
		params['page'] = str(page)
		do_page()


	elif input_test == 'r':
		global key 
		key = input('請輸入想搜索的關鍵字:')
		params['q'] = key
		do_page()

	else:
		print('輸入有誤!!請重新輸入!!')
