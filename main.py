import sys, os, re, requests, base64
from time import altzone, sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


# ============================== Constants ==============================
HTML_CLASS = 'rg_i Q4LuWd'
# ============================== Constants ==============================


# Selemnium
# options = webdriver.ChromeOptions()
# options = webdriver.FirefoxOptions()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)  # https://pypi.org/project/webdriver-manager/
# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
# driver.implicitly_wait(10)


def download_image(url, file_path):
	""" 画像をダウンロードする関数 """
	r = requests.get(url, stream=True)

	if r.status_code == 200:
		with open(file_path, "wb") as f:
			f.write(r.content)


def save_base64_image(data, file_path):
	""" Base64をデコードして画像に戻す関数 """
	# base64の読み込みは4文字ごとに行う。4文字で区切れない部分は「=」で補う
	data = data + '=' * (-len(data) % 4)
	img = base64.b64decode(data.encode())
	with open(file_path, "wb") as f:
			f.write(img)


def main(query: str, browser: str = None, save_dir: str = "./images"):
	url = "https://www.google.com/search?q={}&tbm=isch".format(query)  # tbm=isch does image search

	if browser == None:
		html = requests.get(url).content
		sleep(5)
	else:
		print(browser)
		# Launch Selemnium driver
		if browser == 'chrome':
			options = webdriver.ChromeOptions()
			options.add_argument('--headless')
			options.add_argument('--no-sandbox')
			options.add_argument('--disable-dev-shm-usage')
			driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)  # https://pypi.org/project/webdriver-manager/
		elif browser == 'firefox':
			options = webdriver.FirefoxOptions()
			options.add_argument('--headless')
			options.add_argument('--no-sandbox')
			options.add_argument('--disable-dev-shm-usage')
			driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
		else:
			raise NameError('Command line argument invalid')
		
		driver.implicitly_wait(10)
	
		# HTML取得
		driver.get(url)  # ページ上のすべての画像が読み込まれた状態のHTMLを取得
		# すべての要素が読み込まれるまで待つ。タイムアウトは15秒
		WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
		driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
		html = driver.page_source.encode("utf-8")
	
	# BeautifulSoupを使ってHTMLを解析
	soup = BeautifulSoup(html, "html.parser")

	# imgタグを検索
	img_tags = soup.find_all("img", class_=HTML_CLASS)
	print('\nImages found: {}\n'.format(len(img_tags)))

	img_urls = []

	for img_tag in img_tags:
		print('img_tag:', img_tag)
		url = img_tag.get("src")

		if url is None:
			url = img_tag.get("data-src")

		if url is not None:
			img_urls.append(url)
			print('url', url)


	os.makedirs(save_dir, exist_ok=True)

	base64_string = "data:image/jpeg;base64,"

	# png画像も対象にする
	png_base64_string = "data:image/png;base64,"


	for index, url in enumerate(img_urls):
		name = query.replace(" ", "_")
		file_name = "{}-{}.jpg".format(name, index)
		# print(file_name)
		# print(url)

		image_path = os.path.join(save_dir, file_name)

		if len(re.findall(base64_string, url)) > 0 or len(re.findall(png_base64_string, url)) > 0:
			url = url.replace(base64_string, "")
			save_base64_image(data=url, file_path=image_path)
		else:
			download_image(url=url, file_path=image_path)


if __name__ == '__main__':
	# args = sys.argv
	query, browser, save_dir = 'twice mina', 'firefox', None
	main(query, browser)
