# coding: utf-8
import sys
import urllib
import urllib2
import re
import cookielib
import requests
import chardet
import os
import thread,threading
from requests.adapters import HTTPAdapter

reload(sys)
sys.setdefaultencoding("utf-8")

class MaiZiVideo(object):
	@staticmethod
	def download_video(all_course_url, file_dir):
		MAIN_PAGE = 'http://www.maiziedu.com/'
		response = requests.get(all_course_url)
		response.encoding = 'utf-8'
		html_source = response.text
		course_name = re.search(r'<h1 class="color33 font24 marginB10">(.*?)</h1>', html_source, re.S).group(1)
		os.mkdir(file_dir + course_name)
		all_course_url_and_name = re.findall(r'<li><a href="(.*?)" target="_blank" class="font14 color66"><span class="fl">(.*?)</span>', html_source, re.S)

		for each_course in all_course_url_and_name:
			each_course_url = MAIN_PAGE + each_course[0]
			response = requests.get(each_course_url)
			html_source = response.text
			mp4_url = re.search(r'<source src="(.*?)" type=', html_source, re.S).group(1)
			print mp4_url + ":" + each_course[1]
			urllib.urlretrieve(mp4_url, file_dir + course_name + "/" + each_course[1] + ".mp4", Schedule)
			#urllib.urlretrieve(mp4_url, file_dir + each_course[1], Schedule)

def Schedule(downloadSize, dataSize, remotelyFileSize):
	'''
	downloadSize:已经下载的数据块
	dataSize:数据块的大小
	remotelyFileSize:远程文件的大小
	'''
	per = 100.0 * downloadSize * dataSize / remotelyFileSize
	if per > 100:
		per = 100

	print u'当前下载进度:%.2f%%\r' % per

if __name__ == '__main__':

	file_dir = u'D:/personal/video/program/python/'
	
	list_course = [
	'http://www.maiziedu.com/course/751/',
	]
	for course in list_course:
		MaiZiVideo.download_video(course, file_dir)
