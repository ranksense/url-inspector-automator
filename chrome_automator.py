import asyncio
from pyppeteer import connect

from time import sleep

from urllib.parse import urlparse, urlunparse, urlencode

class ChromeAutomator():
	#def __init__(self, submit_sel, test_live_sel, delay=5, width=1024, height=768):
	def __init__(self, width=1024, height=768):
		self.width = width
		self.height = height

		self.website = None

	async def connect(self, ws, js_extractor, js_clicker):

		self.browser = await connect({"browserWSEndpoint": ws})
		self.page = await self.browser.newPage()

		self.js_extractor = js_extractor
		self.js_clicker = js_clicker

		#optional viewport resize
		await self.page.setViewport({"width": self.width, "height": self.height})

		print("Connected to Chrome at {ws}".format(ws=ws))

		await self.page.goto("https://search.google.com/search-console")

		print("Opened Google Search Console".format(ws=ws))


	async def inspect_urls(self, absolute_urls, criteria, action, delay, action_delay):

		results = list()

		#iterate over URLs to check
		for url in absolute_urls:

			print("Inspecting {url}".format(url=url))

			# Compute website from URL
			u = urlparse(url)
			website = urlunparse((u.scheme, u.netloc, "", "", "", "")) # no trailing slash or path

			#allows to check URLs from different sites
			if self.website == None or website != self.website:
				self.website = website
				await self.visit_site() # reset GSC Home to new site

				print("Resetting GSC Home to new site: {website}".format(website=website))

			data = await self.inspect_url(url, delay) #, submit, criteria))
			print(data)

			results.append(data)

			#wait for action
			if data["coverage"] == criteria:
				await self.click_action(action, action_delay)
		
		return results


	async def visit_site(self):

		#add trailing slash to website
		u = urlparse(self.website)
		website = urlunparse((u.scheme, u.netloc, "/", "", "", "")) # add trailing slash

		params = {"resource_id": website}

		#url encode
		website_qs = urlencode(params)

		#GSC URL
		page_request = urlunparse(("https", "search.google.com", "/search-console", "", website_qs, ""))

		print(page_request)

		await self.page.goto(page_request, {"waitUntil": "networkidle0"})


	async def click_action(self, action, delay=80):

		action_name= {"Do Nothing": "", "Test Live Not Indexed URLs": "test_live", "Submit Not Indexed URLs": "request_indexing"}

		#print("Executing Click")

		if action in action_name.keys() and action_name[action] != "":
			print(action)
			#pass short action name to JS function
			await self.page.evaluate(self.js_clicker, action_name[action])
			
			#wait for action
			print("waiting {delay}".format(delay=delay))
			sleep(delay)


	#async def inspect_url(self, url, submit, criteria):
	async def inspect_url(self, url, delay=8):#, submit, criteria):

		sel="input[value='Inspect any URL in \"{website}/\"']".format(website=self.website)

		#print(sel)
		#await self.page.waitForSelector(sel)
		sleep(delay) # temporary fix as waitForSelector breaks after a live check
		await self.page.click(sel)

		#await page.querySelectorEval(sel, "el => el.value = 'Testing 123'") #doen't work
		await self.page.keyboard.type(url) #input url
		await self.page.keyboard.press("Enter")

		#wait for retrieval
		("waiting {delay}".format(delay=delay))
		sleep(delay)

		results = await self.page.evaluate(self.js_extractor)

		results["url"] = url

		return results








