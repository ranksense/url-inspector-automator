from PyQt5 import QtCore, uic, QtWidgets

import sys, subprocess
import threading
import asyncio

from chrome_automator import ChromeAutomator

from urllib.parse import urljoin
import configparser
from jinja2 import Template
import pandas as pd
from time import sleep
#import pickle as pkl
from urllib.parse import urlparse

UIClass, QtBaseClass = uic.loadUiType("url_inspector_automator.ui")

class URLInspector(UIClass, QtBaseClass):
	def __init__(self):
		UIClass.__init__(self)
		QtBaseClass.__init__(self)
		self.setupUi(self)

		self.chrome = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", 
			"--remote-debugging-port=9222", "--no-first-run", "--user-data-dir={userFolder}"]

		#connecting action buttons to corresponding methods/slots
		self.commandLinkButton.clicked.connect(self.launchChrome)

		self.pushButton.clicked.connect(self.inspectURLs)

		self.pushButton_2.clicked.connect(self.exportResults)

		#regenerate JS extractor
		self.actionBox.currentTextChanged.connect(self.actionSelected)

		self.auto = None # Chrome Automator placeholder

		#load default selectors
		selectors_ini = self.selectorsConf.text()
		#print(selectors_ini)

		self.config = configparser.ConfigParser()

		self.config.read(selectors_ini)

		print("Selectors loaded")

		#convert config to JS files to inject into Chrome
		self.generate_javascript_files()

		self.headers = self.add_headers() #do once

		self.results = list() 



	def add_headers(self):

		#read columns from configuration file
		data = list(self.config["EXTRACTION"])

		data.append("url")

		self.resultsWidget.setColumnCount(len(data))

		self.resultsWidget.setHorizontalHeaderLabels(data);

		return data


	def add_result(self, data):
		#see https://stackoverflow.com/questions/24044421/how-to-add-a-row-in-a-tablewidget-pyqt
		#and https://pythonspot.com/pyqt5-table/

		rowPosition = self.resultsWidget.rowCount()

		#insert empty row
		self.resultsWidget.insertRow(rowPosition)

		for i, column in enumerate(data.values()):
			item =  QtWidgets.QTableWidgetItem(column)
			self.resultsWidget.setItem(rowPosition, i, item)
			#print(column)

		#resize table
		self.resultsWidget.resizeColumnsToContents()


	def add_no_indexed_urls(self):
		
		#create pandas data frame with results
		df = pd.DataFrame(self.results)

		#print(df.head())

		criteria = self.notIndexCriteria.text()

		query = 'coverage=="{criteria}"'.format(criteria=criteria)
		#print(query)

		for url in df.query(query)["url"]:
			print("This url: {url} is not indexed".format(url=url))
			
			self.urlsNotIndexed.insertPlainText(url+"\n")


	def generate_javascript_files(self):

		#Javascript arrow function jinja2 template
		with open("js_extractor.jinja2") as f:
			template_text=f.read()

		template=Template(template_text)

		#combine template with relevant section in configuration file
		self.extraction_fn = template.render(settings=self.config["EXTRACTION"])

		#Javascript arrow function jinja2 template
		with open("js_clicker.jinja2") as f:
			template_text=f.read()

		template=Template(template_text)

		self.clicking_fn = template.render(settings=self.config["CLICKS"])


	# named slot
	# (doesn't require a previously built connection for form widgets)
	@QtCore.pyqtSlot()
	def launchChrome(self):

		#this prevents locking up the UI
		threading.Thread(target=self.launchChromeThread, name="_chrome").start()

		import time

		#wait 5 seconds for Chrome
		time.sleep(5)

		print("Output saved ... reading WS URI")

		with open("chrome.txt", "r") as chrome_output:
		#with open(FIFO) as chrome_output:
			lines = chrome_output.readlines()
			
			if len(lines) > 0:
				#Example DevTools listening on ws://127.0.0.1:9222/devtools/browser/1ad33a5f-4dfa-4763-8726-45d12c60574c
				ws=lines[1].split()[3] #get WS URI

				#print(ws) 

				#update URI
				self.wsURI.setText(ws)
				self.wsURI.setEnabled(False)

				#enable inspectURLs
				self.pushButton.setEnabled(True)
				#disable launching Chrome
				self.commandLinkButton.setEnabled(False)


				#print(self.delay.text())

				delay = int(self.delay.text())

				self.auto = ChromeAutomator() 

				asyncio.get_event_loop().run_until_complete(self.auto.connect(ws, self.extraction_fn, self.clicking_fn))
				

	def launchChromeThread(self):
		# do something
		print("Launching Chrome Thread")  #
		args = self.chrome
		args[3] = args[3].format(userFolder=self.userFolder.text())

		print(args)

		with open("chrome.txt", "w+") as chrome_output: #save Chrome output to file
		#with open(FIFO, "w") as chrome_output: #save Chrome output to file
 
			#works
			#proc=subprocess.Popen(args, stdout=subprocess.PIPE) #stderr=subprocess.DEVNULL)#, , stderr=subprocess.PIPE)
			proc=subprocess.Popen(args, stderr=chrome_output)


		#self.waitforChrome = False

	# named slot
	@QtCore.pyqtSlot()
	def inspectURLs(self):
		# do something
		print("Launched InspectURLs")  #

		urls = self.urls2Check.toPlainText().split()

		if len(urls) == 0:
			QtWidgets.QMessageBox.about(self, "Inspect URLs", "Please provide absolute URLs. For example: https://www.ranksense.com/")
			return

		for url in urls:
			if urlparse(url).netloc == "":
				QtWidgets.QMessageBox.about(self, "Inspect URLs", "Please provide absolute URLs. For example: https://www.ranksense.com/")
				return

		#print(absolute_urls) #there is no text() in QTextEdit
		criteria = self.notIndexCriteria.text()  
		action = self.actionBox.currentText()

		#inspect URL delay
		delay = self.delay.text()
		delay = int(delay)

		#action delay
		action_delay = self.delay_2.text()
		action_delay = int(action_delay)

		#comment below to debug without live Chrome 
		self.results = asyncio.get_event_loop().run_until_complete(self.auto.inspect_urls(urls, criteria, action, delay, action_delay))

		#TO DEBUG

		#pkl.dump( self.results, open( "results.pkl", "wb" ) )

		#self.results = pkl.load(open("results.pkl", "rb"))

		print("Done!")

		for data in self.results:
			self.add_result(data)

		#update not indexed
		self.add_no_indexed_urls()

		#enable exportResults
		self.pushButton_2.setEnabled(True)

		#enable submit URLs
		self.urlsNotIndexed.setEnabled(True)

	# named slot
	@QtCore.pyqtSlot()
	def actionSelected(self):

		#update headers
		self.add_headers()

		#update generated js files
		self.generate_javascript_files()


	# named slot
	@QtCore.pyqtSlot()
	def exportResults(self):

		#create pandas data frame with results
		df = pd.DataFrame(self.results)

		print(df[["url", "coverage"]].groupby("coverage").count())

		df.to_csv(self.csvFile.text())

		QtWidgets.QMessageBox.about(self, "Export Results", "Successfully exported {count} URLs".format(count=df.shape[0]))


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = URLInspector()
	window.show()
	sys.exit(app.exec_())

