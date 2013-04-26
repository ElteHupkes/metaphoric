# Unsetting ID's when adding records in CakePHP

Say you are the regular Cake-guy and you're running a straightforward blog with a "Post" model with a linked "Comment"
model where your viewers can reply. Your code to save a comment probably looks something like this:

~~~~~~ php
if (!empty($this->data)) {
	// Some CAPTCHA / other security checks
	// A fieldList is always a good idea
	$fieldList = array('name', 'email', 'comment', 'post_id');

	$this->Comment->create();
	if (!$this->Comment->save($this->data, true, $fieldList)) {
		// Error handling
	} else {
		// Yay
	}
}
~~~~~~

Seems good right? Now say there's a little code chimpansee looking to mess with your site.
He looks in the source code, sees the structure, and figures "hey, let's just add an id field, see what happens".
He adds the `data[Comment][id]` field to the form and submits the comment the regular way. Now what happens is that,
_even though "id" is not in the fieldList_, it is gonna overwrite the comment with the supplied ID instead of generating
a new one. That could be nasty if a spammer decided to overwrite all your legitimate comments with his viagra ones.

If you are using [SecurityComponent](http://api.cakephp.org/2.3/class-SecurityComponent.html)
this most likely won't be a problem since the request will get blackholed.
Most simple blogs, I reckon, don't have this though (oh, I do, by the way) so it's something worth keeping in mind.
Especially since it's so easy to solve, just add:

```unset($this->data['Comment']['id']);```{:.language-php}

Above the `save()` call and the problem goes away. Another option is passing the data to `create()` and using
`true` as the second argument; this will filter any primary key present. Hope it helps somebody out there!