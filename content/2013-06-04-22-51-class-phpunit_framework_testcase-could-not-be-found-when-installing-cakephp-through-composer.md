# `Class PHPUnit_Framework_TestCase could not be found` when installing CakePHP through Composer
Recently Mark Story (one of CakePHP's main guys)
[wrote a great article](http://mark-story.com/posts/view/installing-cakephp-with-composer) about how to install CakePHP
with Composer. I ran into an issue with today that might or might not suddenly occur when you do this and are also using
`CakeEmail`, so I figured I'd share it.

Composer adds a class loader to your application, if you choose include it (and you should, otherwise it doesn't
really make sense to use Composer). Using Mark's trick you can make sure
that this class loader doesn't override Cake's default class loader, however this still leaves one potential problem.
This problem lies with the class you're supposed to create for email configuration: `EmailConfig`. The file this class
is in is included directly by `CakeEmail` rather then loaded through `App`. Before it is included though, `CakeEmail`
checks whether the class already exists using [`class_exists()`](http://www.php.net/class_exists). Since Cake's
autoloader `App::load()` is not configured to find it, the task is automatically delegated to Composer's class loader,
which pretty much knows about every class in your entire project. This would be fine, had it not been for the fact that
the test cases in the Cake core also include an `EmailConfig` class. At this point it is basically a gamble which one
it is going to include: it included the right file on my PC, but crashed with the error in the title on another.

Since you can't be sure this will go well if you, say, deploy your code to production on another server, you'll have
to somehow force the right `EmailConfig` class. There's no easy way to do this using `App::uses()` unfortunately (the
config file doesn't fit in the convention), but for now I solved it by simply including the `email.php` file in
`bootstrap.php` below Mark's autoloader fix:

~~~~~ php
require APP.'/Config/email.php';
~~~~~