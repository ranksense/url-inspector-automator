() => {

	//XPath wrapper function
	function getElementByXPath(path) {
		return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
	}

	{% if key == "test_live" %}

		e = getElementByXPath('{{xpath}}');
		e.click();

	{% endif %}

	{% if key == "submit_url" %}

		e = getElementByXPath('{{xpath}}');
		e.click();

	{% endif %}

}