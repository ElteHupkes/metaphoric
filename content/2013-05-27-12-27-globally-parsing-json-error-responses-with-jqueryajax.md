# Globally parsing JSON error responses with `jQuery.ajax()`
Proper RESTfull API use status codes to indicate the result of requests. This means that for `PUT`/`PATCH` 
requests a `400 Bad Request` or a `409 Conflict` will be returned if the data in the request is invalid. Since this
is a solvable error for the end user, the API will return error codes, perhaps something like this:

~~~~~~~ json
{
	"errors": {
		"email": "invalid_email"
	}
}
~~~~~~~

Awesome, but if you want to actually _show_ these errors to the end user you'll need access to
the request data. If you're using jQuery, accessing data for requests with a 2xx (success) status code is easy;
if the request's `Content-Type` is `application/json`, jQuery will parse it for you. For 4xx and 5xx requests not
so much though; you need to do something like this:

~~~~~ javascript
$.post('/whatever', '{}').fail(function(xhr) {
	try {
		var validationErrors = JSON.parse(xhr.responseText);
		displayErrors(validationErrors.errors);
	} catch(e) {
		// Invalid JSON error handling
	}
});
~~~~~

If you're a bit lazy like me though, you don't want to do this manually for every scenario in which you'll be handling
errors like this. Preferably, the JSON data is automatically available in every XHR's fail callback.
Unfortunately, `$.ajaxError` and `$.ajaxComplete` are worthless in this scenario, since they fire _after_ user defined
callbacks. The solution is overriding `$.ajax` so you can always assign the first callback. A solution like this
can be found [on this page](http://wingkaiwan.com/2012/10/21/deserialize-error-in-json-for-jquery-ajax/), but it is
incomplete, as any "error" callback assigned through in `$.ajax`'s options will still run before the manual callback. 
I therefore rewrote this code to work in that scenario as well:

~~~~~ javascript
(function($) {
	var old = $.ajax;
	$.ajax = function(url, options) {
		if (!options) {
			options = url || {};
		}
		
		var fail;
		if (options.error) {
			// Remove the error callback and add it
			// as a fail callback on the XHR later on.
			fail = options.error;
			delete options.error;
		}
		
		var xhr = old.call(this, url, options).fail(function(xhr) {
			if (xhr.getResponseHeader('content-type').indexOf('application/json') > -1) {
				try {
					xhr.JSONdata = JSON.parse(xhr.responseText);
				} catch(e) {}
			}
		});
		
		if (fail) {
			// Assign the error callback
			xhr.fail(fail);
		}
		
		return xhr;
	}
})(jQuery);
~~~~~

There you go! Now in your fail callback you can simply use:

~~~~~ javascript
$.post('/whatever', '{}').fail(function(xhr) {
	if (xhr.JSONdata) {
		displayErrors(xhr.JSONdata.errors);
	}
});
~~~~~