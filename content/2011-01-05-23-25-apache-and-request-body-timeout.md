# Apache and Request Body Timeout

Today, while working on the REST API for [SR//Expenses](http://www.srxp.com), we ran into a weird problem. 
Somehow our app succeeded in sending a request over WiFi, while slower connections such as 3G and GPRS wouldn't work. 
Some of the older BlackBerry phones however did succeed. On all occasions the request did reach the API backend, 
but with an empty POST buffer, even though we were sure some data was sent. It took hours of debugging to get to 
the issue, which included finding out why Apache's mod_dumpio wouldn't work (for the ones out there wondering: 
you have to make sure that LogLevel is set to "debug" for not one but all of your VirtualHost entries. 
They might not be fully done developing that module.).

The problem turned out to be the 3G connection speed in combination with the rate at which chunks were sent. 
Apache, by default, waits 10 to 20 seconds for the request header, and after that another 10 seconds for the first 
bytes of the request body. The timeout increases with one second after every 1000 bytes received, but a 
minimum throughput of 500 bytes per second is required. It turned out that our 3G connection at the 
Amsterdam Science Park was so lousy that it took more than 10 seconds to send the first chunk of request body data, 
and so the request failed altogether.
 
What's interesting though is that this doesn't result in a server error: apparently Apache still invokes the 
CGI handler and just processes the requested URL without a request body, which struck me as rather disturbing. 
I would have liked to see a 500 response when something like this happened, at least that would give us a 
clear IO-error indication.
 
For those of you who are having the same problems, you can use Apache's 
[`mod_reqtimeout`](http://httpd.apache.org/docs/trunk/mod/mod_reqtimeout.html) to alter the request 
timeout settings. It's actually really well documented and easy to solve once you figure it out.
 
I'm still not sure why the older BlackBerry OS versions did manage to send the request quite often, 
since the problem was clearly in the network connection and not in any of our applications. This put us off when 
trying to look for the problem, but I guess it once again shows that 
[correlation doesn't imply causation](http://xkcd.com/552/). 