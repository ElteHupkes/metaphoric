# Getting MAX or MIN values in CakePHP

This is something that always bugs me because I always have to look it up, and it isn't really documented somewhere.
Building an aggregate query isn't all that difficult:

~~~php
$result = $this->find('first',
	array(
		'fields' => array('MAX(some_field) AS name')
	)
);
~~~

But even though it's simple I keep forgetting how to actually get that value from the array.
Well, here it is (and now that I posted it here, I'm probably not going to forget it anymore..):

`$maxValue = $result[0]['name']`{:.language-php}