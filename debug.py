# For looking for HTML class name of img tag

import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


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
			driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)  # https://pypi.org/project/webdriver-manager/
		elif browser == 'firefox':
			options = webdriver.FirefoxOptions()
			options.add_argument('--headless')
			options.add_argument('--no-sandbox')
			options.add_argument('--disable-dev-shm-usage')
			driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
		else:
			raise NameError('Command line argument invalid')
		
		driver.implicitly_wait(10)
	
		# HTML取得
		driver.get(url)  # ページ上のすべての画像が読み込まれた状態のHTMLを取得
		# すべての要素が読み込まれるまで待つ。タイムアウトは15秒。
		WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
		driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
		html = driver.page_source.encode("utf-8")
	
	# BeautifulSoupを使ってHTMLを解析
	soup = BeautifulSoup(html, "html.parser")

	# imgタグを検索
	img_tags = soup.find_all("img")
	print(img_tags)


if __name__ == '__main__':
	main('twice mina', 'firefox')
