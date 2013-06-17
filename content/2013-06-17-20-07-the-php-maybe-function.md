# The PHP `maybe` function
Sometimes you just have a revelation, something that has bothered you for years that is actually quite easy to solve. For
me, one of those things was the common PHP-scenario in which you check if a certain array key exists, if so return it,
and otherwise return some default value. This is relatively easy with a ternary operator:

~~~~ php
$var = array_key_exists($someHash, 'key') ? $someArray['key'] : 'default';
~~~~

What bugs me about this though is the repetition: You have to type both `$someHash` and `key` twice. It's a small
thing, but it's been bothering me for ages. Actually I think it started actively bothering me when I started using
JavaScript on a daily basis, where you can simply use:

~~~~ javascript
var v = someHash['key'] || 'default';
~~~~

A similar construct in PHP would not only return the wrong value - it would also raise a `Notice` if the key wasn't
present. So last week, when I wrote this function:

~~~~ php
/**
 * Returns the key $k on array $arr if it exists,
 * the default otherwise.
 * @param array $arr The array to check 
 * @param string $k The key to return
 * @param mixed $default The default value if the key doesn't exist.
 * @return string
 */
function maybe($arr, $k, $default = '') {
	return array_key_exists($k, $arr) ? $arr[$k] : $default;
}
~~~~

And now I can simply use:

~~~~ php
$var = maybe($someHash, 'key', 'default');
~~~~

Why I haven't thought this before is beyond me. I'm very happy about it though.