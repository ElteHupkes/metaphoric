# PHP, MySQL and UTF-8

There's a lot of stuff written about this all over the internet: getting PHP to communicate with MySQL correctly 
using UTF-8. I ran into a couple of problems myself, and this is the story about how I got them fixed.

## Scrambled characters
MySQL, being quite old, uses latin1 as its default encoding (unless it is compiled/configured otherwise). 
This has bugged me forever, especially since it isn't all that clear how to correct it. 
UTF-8 is most definitely the standard for webpages these days, so bytes are being sent to and from all 
clients in this encoding.

Today, while browsing through my database using PhpMyAdmin though, I noticed that all special characters 
(such as é) were displayed as a set of weird scrambled characters we all know from encoding problems. 
The characters were displaying fine in my application. Although I'm pretty confident about my developing skills, 
I found it hard to believe that such an established product as PhpMyAdmin would get it wrong, so I started doing some 
research. Quite some time later I finally figured out what happened.
 
## What happened
MySQL converts characters between charsets if it thinks it's supposed to. This decision is made based on the 
encoding setting of the connection, so even if all your tables, data, etc are correctly set to UTF-8, MySQL 
will still convert characters if the connection isn't. Small example: suppose you send a chunk of UTF-8 data to 
be stored in a UTF-8 column in a UTF-8 table in a UTF-8 database (that's right). The connection, however, has latin1 
encoding (the MySQL default, hooray). Upon recieving the data, MySQL thus converts the characters it thinks are latin1 
characters to their corresponding UTF-8 characters, _saving the wrong bytes to the database_. 
When retrieving the data, however, the same conversion is done only the other way around, so you'll actually 
get the right bytes back from the database.

## Why you don't want it to happen
The part in bold is exactly why you don't want this to happen; incorrect data is saved to the database. 
Imagine you'd want to search through this data using a query, you'd have a really hard time matching characters, 
using MySQL string functions, etcetera.

## How to fix it
This is the tricky part. I've seen lots of people saying they simply set the connection encoding using 
the following query:

	SET NAMES utf8
	
The good thing about this solution is, it works, and it's simple. However, running an additional query-call for 
every request immediately struck me as odd and inefficient; maybe there's a better way? 

Obviously, there is; assuming you can alter your server config (get a VPS people, it's worth it). Now there's 
some ambiguity floating around the web about how to do it; eventually I solved it by adding three lines to my "my.cnf" 
file (if you're on Ubuntu like me, it's located in /etc/mysql/my.cnf (better yet, you can add a file to 
/etc/mysql/conf.d/ with these lines). They need to be placed in the `[mysqld]` section of my.cnf:

	[mysqld]
	..........
	collation-server = utf8_unicode_ci
	init-connect = 'SET NAMES utf8'
	character-set-server = utf8
	
Now check the results of the query `SHOW VARIABLES LIKE 'character_set%'`

Should show mostly "utf8", especially for the `character_set_results` and `character_set_server` settings!