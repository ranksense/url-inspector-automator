# url-inspector-automator
URL Inspection Tool Automator

This is a desktop client that automates the Google Search Console URL Inspection tool using the Chrome browser.

Steps to install:

1. Clone this repository
2. Install Python dependencies: pip install -r requirements.txt

Launch from command line using python3 url_inspector_automator.py

Copy and paste absolute URLs to inspect, and select any action you want to take for URLs that meet the not indexed criteria. Possible actions are test URL live or request indexing.

When you click to open Chrome the first time, input your user/pass for Search Console and let Chrome save it. It will be stored locally in the profile directory. Subsequent runs won’t prompt you to login again.

Make sure to completely exit the Chrome browser launched after you close the tool. If you leave it open, new runs won't be able to connect to Chrome. 

Feel free to review the screenshtots to see how the tool looks and works.

Please file bug reports as Github issues. Bug fixes and features are welcome as pull requests.

# For Windows users
Steps to install:

1-2. Same as above
3. Modify line 25 of url_inspector_automator.py to match your chrome.exe path. (C://{path-to-chrome-folder}/chrome.exe)
4. Close all Chrome windows before launching the script.
