# Understanding `required` and `allowEmpty` in CakePHP validation rules
One of the most confusing things about CakePHP's validation rules is the meaning of the `required` and (especially)
`allowEmpty` flags. Therefore I figured I'd give them both a quick walkthrough that you can reference whenever
you get confused.

So here are some important facts about Cake validation rules, in bullet points:

- Validation rules for ields that are not specified in the `fieldList` for a `Model::validates()` or `Model::save()`
  call are never executed; these fields will not be saved so they are completely ignored. The
  `allowEmpty`/`required` flags will not change this behavior.
- `required` and `allowEmpty` only affect whether a validation rule is executed or not. 
  They do not affect the rule itself, they are merely meant as an easy way to break out of common scenarios without
  having to add extra rules.
- Now that we've established that; `required` only checks whether a field is present on the input array using
  [`array_key_exists`](http://www.php.net/array_key_exists). If the field is not present, the validation
  rules for this field are not executed, because you cannot use the value of a field that doesn't exist. 
  With `required = true` in this scenario the validation rule will fail
  with the message of the rule the `required` flag was set on, while `required = false` would lead to the field's
  validation succeeding without any rule being executed. The default value of `required` is `false`, meaning a field
  doesn't have to be present with the save.
- The `allowEmpty` flag lets you skip all validation rules for a field or fail immediately if the field is left empty.
  This empty check is defined `true` for any value for which [`empty`](http://www.php.net/empty) returns `true`,
  except for `"0"`, which is considered non-empty. Now comes the confusing part: **`allowEmpty` has three possible
  values, not two**. Specifying `true` would cause validation to be skipped if the field is empty, specifying `false`
  causes it to fail in that case. You might already see the missing third case here: the one that skips the empty
  check and just executes the validation rule. This is actually the default behavior - it happens when you don't
  specify `allowEmpty` at all. The explicit equivalent of this would be `allowEmpty = null`.

I hope this settles some of the confusion.

One more thing though: sometimes you want a different validation error for when a field has not been specified
but should have been - this is impossible when adding `required = true` to an existing rule (because that rule
has its own validation error). The solution is adding a validation rule that always succeeds to your model:

~~~~ php
// 
public $validate = array(
	'fieldName' => array(
		'required' => array(
			'rule' => 'present',
			'message' => 'This field is required',
			'required' => true
		),
		'some_other_rule' => array(
			'rule' => 'whatever',
			'message' => 'Some other condition is not met'
		)
	)
);


// The rule
public function present() {
	return true;
}
~~~~

This way validation will fail with a "This field is required" error if it is left out, and another appropriate
error if a different condition fails.