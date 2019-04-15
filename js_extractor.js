() => {
	var data = {};

	//isHidden helper function
	// See https://stackoverflow.com/questions/19669786/check-if-element-is-visible-in-dom
	function isHidden(el) {
		//if(el == null) return true;
		//return (el.offsetParent === null)
		//Slower
		var style = window.getComputedStyle(el);
		return (style.display === 'none')
	}

	//XPath wrapper function
	function getElementByXPath(path) {
		return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
	}

	//XPath wrapper function returing an iterator
	function getElementsByXPath(path) {
		return document.evaluate(path, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
	}

	
		//coverage
		
			xpaths = getElementsByXPath('//div[text()="Coverage"]/following-sibling::div');  
			for (let i = 0, length = xpaths.snapshotLength; i < length; ++i) {

				if(isHidden(xpaths.snapshotItem(i)) == false){
					data["coverage"] = xpaths.snapshotItem(i);
				}
			}
		

	
		//sitemaps
			
			data["sitemaps"] = getElementByXPath('//div[text()="Sitemaps"]/parent::div/div[2]');  
		

	
		//referring_page
			
			data["referring_page"] = getElementByXPath('//div[text()="Referring page"]/parent::div/div[2]');  
		

	
		//crawled_date
			
			data["crawled_date"] = getElementByXPath('//div[text()="Last crawl"]/parent::div/div[2]');  
		

	
		//crawled_as
			
			data["crawled_as"] = getElementByXPath('//div[text()="Crawled as"]/parent::div/div[2]');  
		

	
		//crawled_allowed
			
			data["crawled_allowed"] = getElementByXPath('//div[text()="Crawl allowed?"]/parent::div/div[2]');  
		

	
		//page_fetch
			
			data["page_fetch"] = getElementByXPath('//div[text()="Page fetch"]/parent::div/div[2]');  
		

	
		//indexing_allowed
			
			data["indexing_allowed"] = getElementByXPath('//div[text()="Indexing allowed?"]/parent::div/div[2]');  
		

	
		//user_canonical
			
			data["user_canonical"] = getElementByXPath('//div[text()="User-declared canonical"]/parent::div/div[2]');  
		

	
		//alternative_user_canonical
			
			data["alternative_user_canonical"] = getElementByXPath('//div[text()="User-declared canonical"]/parent::div/div[3]');  
		

	
		//google_canonical
			
			data["google_canonical"] = getElementByXPath('//span[text()="Google-selected canonical"]/parent::div/parent::div/parent::div/div[2]/div');  
		

	

	//loop twice to avoid bug with url_index and url_not_index

	
		data["coverage"] = data["coverage"] && data["coverage"].textContent;
	
		data["sitemaps"] = data["sitemaps"] && data["sitemaps"].textContent;
	
		data["referring_page"] = data["referring_page"] && data["referring_page"].textContent;
	
		data["crawled_date"] = data["crawled_date"] && data["crawled_date"].textContent;
	
		data["crawled_as"] = data["crawled_as"] && data["crawled_as"].textContent;
	
		data["crawled_allowed"] = data["crawled_allowed"] && data["crawled_allowed"].textContent;
	
		data["page_fetch"] = data["page_fetch"] && data["page_fetch"].textContent;
	
		data["indexing_allowed"] = data["indexing_allowed"] && data["indexing_allowed"].textContent;
	
		data["user_canonical"] = data["user_canonical"] && data["user_canonical"].textContent;
	
		data["alternative_user_canonical"] = data["alternative_user_canonical"] && data["alternative_user_canonical"].textContent;
	
		data["google_canonical"] = data["google_canonical"] && data["google_canonical"].textContent;
	

	return data;
}