action => {

	//XPath wrapper function
	function getElementByXPath(path) {
		return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
	}

	//Clicking actions from selectors
	

	if( action == 'test_live' ){
		e = getElementByXPath('//span[text()="Test live URL"]');
		e.click();	
	};

	

	if( action == 'request_indexing' ){
		e = getElementByXPath('//span[text()="Request indexing"]');
		e.click();	
	};

	


}