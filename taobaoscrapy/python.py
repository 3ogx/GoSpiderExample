# -*- coding:utf-8 -*-
import urllib.request, urllib.parse, http.cookiejar
import os, time,re
import http.cookies
import xlsxwriter as wx
from PIL import Image
import pymysql
import socket
__author__ = 'hunterhug'
# http://python.jobbole.com/81344/
# ���JSON
import xml.dom.minidom
import json
from openpyxl import Workbook
from openpyxl import load_workbook

def password():
	print('����������˺ź�����')
	user=input('�˺ţ�')
	pwd=input('���룺')
	if user=='jinhan' and pwd=='6833066':
		print('��ӭ�㣺'+user)
		return
	try:
		mysql = pymysql.connect(host="192.168.1.177", user="dataman", passwd="123456",db='qingmu', charset="utf8")
		cur = mysql.cursor()
		isuser="SELECT * FROM mtaobao where user='{0}' and pwd='{1}'".format(user,pwd)
		cur.execute(isuser)
		mysql.commit()
		if cur.fetchall():
			print('��ӭ�㣺'+user)
			localIP = socket.gethostbyname(socket.gethostname())#����õ�����ip
			ipList = socket.gethostbyname_ex(socket.gethostname())
			s=''
			for i in ipList:
				if i != localIP and i!=[]:
					s=s+(str)(i)
			timesss=time.strftime('%Y%m%d-%H%M%S', time.localtime())
			update="UPDATE mtaobao SET `times` = `times`+1,`dates`='{0}',`ip` ='{1}' where user='{2}'".format(timesss,s.replace("'",''),user)
			#print(update)
			cur.execute(update)
			mysql.commit()
			cur.close()
			mysql.close()
			return
		else:
			raise
	except Exception as e:
		#print(e)
		mysql.rollback()
		cur.close()
		mysql.close()
		print('�������')
		password()

# �ҳ��ļ���������html��׺���ļ�
def listfiles(rootdir, prefix='.xml'):
	file = []
	for parent, dirnames, filenames in os.walk(rootdir):
		if parent == rootdir:
			for filename in filenames:
				if filename.endswith(prefix):
					file.append(rootdir + '/' + filename)
			return file
		else:
			pass

def writeexcel(path,dealcontent):
	workbook = wx.Workbook(path)
	top = workbook.add_format({'border':1,'align':'center','bg_color':'white','font_size':11,'font_name': '΢���ź�'})
	red = workbook.add_format({'font_color':'white','border':1,'align':'center','bg_color':'800000','font_size':11,'font_name': '΢���ź�','bold':True})
	image = workbook.add_format({'border':1,'align':'center','bg_color':'white','font_size':11,'font_name': '΢���ź�'})
	formatt=top
	formatt.set_align('vcenter') #���õ�Ԫ��ֱ����
	worksheet = workbook.add_worksheet()        #����һ�����������
	width=len(dealcontent[0])
	worksheet.set_column(0,width,38.5)            #�趨�еĿ��Ϊ22����
	for i in range(0,len(dealcontent)):
		if i==0:
			formatt=red
		else:
			formatt=top
		for j in range(0,len(dealcontent[i])):
			if i!=0 and j==len(dealcontent[i])-1:
				if dealcontent[i][j]=='':
					worksheet.write(i,j,' ',formatt)
				else:
					try:
						worksheet.insert_image(i,j,dealcontent[i][j])
					except:
						worksheet.write(i,j,' ',formatt)
			else:
				if dealcontent[i][j]:
					worksheet.write(i,j,dealcontent[i][j].replace(' ',''),formatt)
				else:
					worksheet.write(i,j,'��',formatt)
	workbook.close()
	

def getHtml(url,daili='',postdata={}):
	"""
    ץȡ��ҳ��֧��cookie
    ��һ������Ϊ��ַ���ڶ���ΪPOST������
    """
	# COOKIE�ļ�����·��
	filename = 'cookie.txt'

	# ����һ��MozillaCookieJar����ʵ���������ļ���
	cj = http.cookiejar.MozillaCookieJar(filename)
	# cj =http.cookiejar.LWPCookieJar(filename)

	# ���ļ��ж�ȡcookie���ݵ�����
	# ignore_discard����˼�Ǽ�ʹcookies��������Ҳ������������
	# ignore_expires����˼������ڸ��ļ��� cookies�Ѿ����ڣ��򸲸�ԭ�ļ�д
	# ������ڣ����ȡ��ҪCOOKIE
	if os.path.exists(filename):
		cj.load(filename, ignore_discard=True, ignore_expires=True)
	# ��ȡ����COOKIE
	if os.path.exists('../subcookie.txt'):
		cookie = open('../subcookie.txt', 'r').read()
	else:
		cookie='ddd'
	# �������COOKIE�������Ĵ�ר��
	proxy_support = urllib.request.ProxyHandler({'http':'http://'+daili})
	# ��������֧��
	if daili:
		print('����:'+daili+'����')
		opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPHandler)
	else:
		opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

	# ��ר�Ҽ�ͷ��
	opener.addheaders = [('User-Agent',
						  'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'),
						 ('Referer',
						  'http://s.m.taobao.com'),
						 ('Host', 'h5.m.taobao.com'),
						 ('Cookie',cookie)]

	# ����ר��
	urllib.request.install_opener(opener)
	# ��������ҪPOST
	if postdata:
		# ����URL����
		postdata = urllib.parse.urlencode(postdata)

		# ץȡ��ҳ
		html_bytes = urllib.request.urlopen(url, postdata.encode()).read()
	else:
		html_bytes = urllib.request.urlopen(url).read()

	# ����COOKIE���ļ���
	cj.save(ignore_discard=True, ignore_expires=True)
	return html_bytes

# ȥ�������еķǷ��ַ� (Windows)
def validateTitle(title):
	rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
	new_title = re.sub(rstr, "", title)
	return new_title

# �ݹ鴴���ļ���
def createjia(path):
	try:
		os.makedirs(path)
	except:
		print('Ŀ¼�Ѿ����ڣ�'+path)

def timetochina(longtime,formats='{}��{}Сʱ{}����{}��'):
	day=0
	hour=0
	minutue=0
	second=0
	try:
		if longtime>60:
			second=longtime%60
			minutue=longtime//60
		else:
			second=longtime
		if minutue>60:
			hour=minutue//60
			minutue=minutue%60
		if hour>24:
			day=hour//24
			hour=hour%24
		return formats.format(day,hour,minutue,second)
	except:
		raise Exception('ʱ��Ƿ�')

def begin():
    sangjin = '''
		-----------------------------------------
		| ��ӭʹ���Զ�ץȡ�ֻ��Ա��ؼ��ֳ���   	|
		| ʱ�䣺2015��12��23��                  |
		| ����΢����һֻ����                    |
		| ΢��/QQ��569929309                    |
		-----------------------------------------
	'''
    print(sangjin)


if __name__ == '__main__':
	begin()
	# password()
	today=time.strftime('%Y%m%d', time.localtime())
	a=time.clock()
	keyword = input('������ؼ��֣�')
	sort = input('�����������밴1�����۸�͵���ץȡ�밴2���۸�ߵ��Ͱ�3����������4���ۺ�����5��')
	try:
		pages =int(input('��Ҫץȡ��ҳ����Ĭ��100ҳ����'))
		if pages>100 or pages<=0:
			print('ҳ��Ӧ����1-100֮��')
			pages=100
	except:
		pages=100
	try:
		man=int(input('������ץȡ��ͣʱ�䣺Ĭ��4�루4����'))
		if man<=0:
			man=4
	except:
		man=4
	zp=input('ץȡͼƬ��1����ץȡ��2��')
	if sort == '1':
		sortss = '_sale'
	elif sort == '2':
		sortss = 'bid'
	elif sort=='3':
		sortss='_bid'
	elif sort=='4':
		sortss='_ratesum'
	elif sort=='5':
		sortss=''
	else:
		sortss = '_sale'
	namess=time.strftime('%Y%m%d%H%S', time.localtime())
	root = '../data/'+today+'/'+namess+keyword
	roota='../excel/'+today
	mulu='../image/'+today+'/'+namess+keyword
	createjia(root)
	createjia(roota)
	for page in range(0, pages):
		time.sleep(man)
		print('��ͣ'+str(man)+'��')
		if sortss=='':
			postdata = {
				'event_submit_do_new_search_auction': 1,
				'search': '�ύ��ѯ',
				'_input_charset': 'utf-8',
				'topSearch': 1,
				'atype': 'b',
				'searchfrom': 1,
				'action': 'home:redirect_app_action',
				'from': 1,
				'q': keyword,
				'sst': 1,
				'n': 20,
				'buying': 'buyitnow',
				'm': 'api4h5',
				'abtest': 16,
				'wlsort': 16,
				'style': 'list',
				'closeModues': 'nav,selecthot,onesearch',
				'page': page
			}
		else:
			postdata = {
				'event_submit_do_new_search_auction': 1,
				'search': '�ύ��ѯ',
				'_input_charset': 'utf-8',
				'topSearch': 1,
				'atype': 'b',
				'searchfrom': 1,
				'action': 'home:redirect_app_action',
				'from': 1,
				'q': keyword,
				'sst': 1,
				'n': 20,
				'buying': 'buyitnow',
				'm': 'api4h5',
				'abtest': 16,
				'wlsort': 16,
				'style': 'list',
				'closeModues': 'nav,selecthot,onesearch',
				'sort': sortss,
				'page': page
			}
		postdata = urllib.parse.urlencode(postdata)
		taobao = "http://s.m.taobao.com/search?" + postdata
		print(taobao)
		try:
			content1 = getHtml(taobao)
			file = open(root + '/' + str(page) + '.json', 'wb')
			file.write(content1)
		except Exception as e:
				if hasattr(e, 'code'):
					print('ҳ�治���ڻ�ʱ��̫��.')
					print('Error code:', e.code)
				elif hasattr(e, 'reason'):
						print("�޷���������.")
						print('Reason:  ', e.reason)
				else:
					print(e)

	# files=listfiles('201512171959','.json')
	files = listfiles(root, '.json')
	total = []
	# total.append(['ҳ��', '����', '��Ʒ����', '��Ʒ���ۼ�', '������ַ', '������', 'ԭ��', '�ֻ��ۿ�', '�۳�����', '��������', '��������', '����ۿ�','URL��ַ','ͼ��URL','ͼ��'])
	total.append(['ҳ��', '����', '��Ʒ����', '��Ʒ���ۼ�', '������ַ', '������', 'ԭ��', '�۳�����', '��������', '��������', '����ۿ�','URL��ַ','ͼ��URL','ͼ��'])
	for filename in files:
		try:
			doc = open(filename, 'rb')
			doccontent = doc.read().decode('utf-8', 'ignore')
			product = doccontent.replace(' ', '').replace('\n', '')
			product = json.loads(product)
			onefile = product['listItem']
		except:
			print('ץ����' + filename)
			continue
		for item in onefile:
			itemlist = [filename, item['nick'], item['title'], item['price'], item['location'], item['commentCount']]
			itemlist.append(item['originalPrice'])
			# itemlist.append(item['mobileDiscount'])
			itemlist.append(item['sold'])
			itemlist.append(item['zkType'])
			itemlist.append(item['act'])
			itemlist.append(item['coinLimit'])
			itemlist.append('http:'+item['url'])
			picpath=item['pic_path'].replace('60x60','720x720')
			itemlist.append(picpath)
			#http://g.search2.alicdn.com/img/bao/uploaded/i4/i4/TB13O7bJVXXXXbJXpXXXXXXXXXX_%21%210-item_pic.jpg_180x180.jpg
			if zp=='1':
				if os.path.exists(mulu):
					pass
				else:
					createjia(mulu)
				url=urllib.parse.quote(picpath).replace('%3A',':')
				urllib.request.urlcleanup()
				try:
					pic=urllib.request.urlopen(url)
					picno=time.strftime('%H%M%S', time.localtime())
					filenamep=mulu+'/'+picno+validateTitle(item['nick']+'-'+item['title'])
					filenamepp=filenamep+'.jpeg'
					sfilename=filenamep+'s.jpeg'
					filess=open(filenamepp,'wb')
					filess.write(pic.read())
					filess.close()
					img = Image.open(filenamepp)
					w, h = img.size
					size=w/6,h/6
					img.thumbnail(size, Image.ANTIALIAS)
					img.save(sfilename,'jpeg')
					itemlist.append(sfilename)
					print('ץ��ͼƬ��'+sfilename)
				except Exception as e:
					if hasattr(e, 'code'):
						print('ҳ�治���ڻ�ʱ��̫��.')
						print('Error code:', e.code)
					elif hasattr(e, 'reason'):
							print("�޷���������.")
							print('Reason:  ', e.reason)
					else:
						print(e)
					itemlist.append('')
			else:
				itemlist.append('')
			# print(itemlist)
			total.append(itemlist)
	if len(total) > 1:
		writeexcel(roota +'/'+namess+keyword+ '�Ա��ֻ���Ʒ.xlsx', total)
	else:
		print('ʲô��ץ����')
	b=time.clock()
	print('����ʱ�䣺'+timetochina(b-a))
input('��رմ���')