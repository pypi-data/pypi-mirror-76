from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
import wget
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import click


def scroll_down(browser):
	page=browser.find_element_by_tag_name('body')
	for i in range(10):
		page.send_keys(Keys.PAGE_DOWN)
		sleep(2)
	return browser
	


@click.group()
def cli():
	pass


@cli.command()
def hash(): 

	opts=Options()
	opts.set_headless()
	assert opts.headless
	browser=Firefox(options=opts)
	browser.get('https://twitter.com/explore/tabs/trending')
	click.secho("Browser opened", fg="white", bg="blue", blink=True, bold=True)

	search = WebDriverWait(browser, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//span[@class='r-18u37iz']//span[@class='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0']"))
    )

	print("found {} hashtags.".format(len(search)))
	for i in range(len(search)):
		click.secho(search[i].text, fg="green")

	browser.close()



@cli.command()
@click.option('--hash', default=1, help="position of hashtag in trending page")
@click.argument("num")
def imgs(hash, num):
	opts=Options()
	opts.set_headless()
	assert opts.headless
	browser=Firefox(options=opts)
	browser.get('https://twitter.com/explore/tabs/trending')
	click.secho("Browser opened", fg="white", bg="blue", blink=True, bold=True)
	sleep(10)
	search = WebDriverWait(browser, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//span[@class='r-18u37iz']//span[@class='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0']"))
    )
	search[hash].click()
	sleep(10)

	browser=scroll_down(browser)

	for i in range(int(num)):
		images1=browser.find_elements_by_xpath('//div[@class="r-1p0dtai r-1pi2tsx r-1d2f490 r-u8s1d r-ipm5af r-13qz1uu"]//img[@class="css-9pa8cd"]')
		for i in range(len(images1)):
			if (images1[i].get_attribute('src').find('media')!= -1):
				wget.download(images1[i].get_attribute('src'))
		browser=scroll_down(browser)

	browser.close()
















































