import requests

'''
#download images
for page in range(1,20):
	URL = "https://cec.com.vn/book/kg3/sb3/files/mobile/{}.jpg?201224182246".format(page)
	print(URL)
	response = requests.get(URL)
	open("/home/minhthienk/Desktop/Phonics books/Book 3/Pages/page_{}.jpg".format(page), "wb").write(response.content)
'''

#download audio
for page in range(1,91):
	for part in ['.1','-1','_1','.2','-2','_2','']:
		URL = "https://cec.com.vn/book/kg2/files/pageConfig/Page {}{}.mp3?210318180607".format(page, part)
		print(URL)
		response = requests.get(URL)
		open("/home/minhthienk/Desktop/Phonics books/Book 2/Audio/page_{}{}.mp3".format(page,part), "wb").write(response.content)

		URL = "https://cec.com.vn/book/kg2/files/pageConfig/Page-{}{}.mp3?210318180607".format(page, part)
		print(URL)
		response = requests.get(URL)
		open("/home/minhthienk/Desktop/Phonics books/Book 2/Audio/page_-{}{}.mp3".format(page,part), "wb").write(response.content)


'''
book 2
https://cec.com.vn/book/kg2/files/pageConfig/Page-1.mp3?210318180607
https://cec.com.vn/book/kg2/files/pageConfig/Page {}{}.mp3?210318180607
book 3
https://cec.com.vn/book/kg3/sb3/files/pageConfig/Page 61.m4a?201224182246
https://cec.com.vn/book/kg3/sb3/files/pageConfig/Page 7_1.m4a?201224182246


'''