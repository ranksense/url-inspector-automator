import asyncio
from pyppeteer import connect

from time import sleep

from urllib.parse import urlparse

class ChromeAutomator():
	#def __init__(self, submit_sel, test_live_sel, delay=5, width=1024, height=768):
	def __init__(self, width=1024, height=768):
		self.width = width
		self.height = height
		#self.delay = delay
		#self.submit_sel = submit_sel
		#self.test_live_sel = test_live_sel

	async def connect(self, ws, js_extractor):

		self.browser = await connect({"browserWSEndpoint": ws})
		self.page = await self.browser.newPage()

		self.js_extractor = js_extractor

		#optional viewport resize
		await self.page.setViewport({"width": self.width, "height": self.height})

		print("Connected to Chrome at {ws}".format(ws=ws))

		await self.page.goto("https://search.google.com/search-console")

		print("Opened Google Search Console".format(ws=ws))


	async def inspect_urls(self, absolute_urls, website, criteria, action, delay):

		results = list()

		#iterate over URLs to check
		for url in absolute_urls:

			print("Inspecting {url}".format(url=url))

			#print("Reset Google Search Console Home to {home}".format(home=website))
			#asyncio.get_event_loop().run_until_complete(self.auto.visit_site(website))
			#await self.visit_site(website)

			#data = asyncio.get_event_loop().run_until_complete(self.auto.inspect_url(url, submit, criteria))
			#delay = self.delay.text()
			#delay = int(delay)

			#data = asyncio.get_event_loop().run_until_complete(self.auto.inspect_url(url, delay)) #, submit, criteria))
			data = await self.inspect_url(url, delay) #, submit, criteria))
			print(data)

			results.append(data)

			#wait for action
			if data["coverage"] == criteria:
				if action == "Test Live Not Indexed URLs":
					#print("waiting for action {delay} seconds".format(delay=delay*10))
					#sleep(delay*10)
					await self.test_live_url()
				
				if action == "Submit Not Indexed URLs":
					#print("waiting for action {delay} seconds".format(delay=delay*10))
					#sleep(delay*10)
					await self.submit_url()

			
			#self.add_result(data)

			#print(data)
		
		return results


	async def visit_site(self, website):

		parsed_url = urlparse(website)

		page_request = 'https://search.google.com/search-console?resource_id={scheme}%3A%2F%2F{website}%2F'.format(scheme=parsed_url.scheme, website=parsed_url.netloc)

		print(page_request)

		self.website = website

		await self.page.goto(page_request, {"waitUntil": "networkidle0"})


	async def test_live_url(self, delay=120):

		#print("Executing Click")

		test_live_js="""
			//XPath wrapper function
	function getElementByXPath(path) {
		return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
	}

						e = getElementByXPath('//span[text()="Test live URL"]');
					e.click();
		"""

		await self.page.evaluate(test_live_js)

		sleep(delay)

	async def submit_url(self, delay=120):

		#print("Executing Click")

		submit_js="""
			//XPath wrapper function
	function getElementByXPath(path) {
		return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
	}

						e = getElementByXPath('//span[text()="Request indexing"]');
					e.click();
		"""

		await self.page.evaluate(submit_js)

		sleep(delay)


	#async def inspect_url(self, url, submit, criteria):
	async def inspect_url(self, url, delay=5):#, submit, criteria):

		#sel= "#gb > div.gb_gd.gb_Md.gb_Zb > div.gb_lc.gb_wd.gb_Fd.gb_rd.gb_vd.gb_Cd > div.gb_td > form > div > div > div > div > div > div.d1dlne > input.Ax4B8.ZAGvjd"
		#TODO: remove trailing slash
		sel="input[value='Inspect any URL in \"{website}/\"']".format(website=self.website)

		#print(sel)
		#await self.page.waitForSelector(sel)
		sleep(delay) # temporary fix as waitForSelector breaks after a live check
		await self.page.click(sel)

		#await page.querySelectorEval(sel, "el => el.value = 'Testing 123'") #doen't work
		await self.page.keyboard.type(url) #input url
		await self.page.keyboard.press("Enter")

		#wait for retrieval
		print("waiting {delay}".format(delay=delay))
		sleep(delay)

		results = await self.page.evaluate(self.js_extractor)

		results["url"] = url

		#if submit and results["coverage"] == criteria:
		#	print("Submitting URL: {url}".format(url=url))
			
		#	print(self.test_live_sel)

			#click to test live
			#await self.page.waitForSelector(self.test_live_sel)
			#await self.page.click(self.test_live_sel)

		return results








