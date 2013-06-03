# Understanding `required` and `allowEmpty` in CakePHP validation rules
One of the most confusing things about CakePHP's validation rules is the meaning of the `required` and (especially)
`allowEmpty` flags. Therefore I figured I'd give them both a quick walkthrough that you can reference whenever
you get confused.

So here are some important facts about Cake validation rules, in bullet points:

- Validation rules for ields that are not specified in the `fieldList` for a `Model::validates()` or `Model::save()`
  call are never executed; these fields will not be saved so they are completely ignored. The
  `allowEmpty`/`required` flags will not change this behavior.
- `required` and `allowEmpty` apply to a _field_, not to a rule. It doesn't matter on which rule you specify them,
   they influence the field - not that rule. The rule you specify them on only affects the validation error message
   should one of these flags cause field validation to fail.
   You should really only ever add these flags to one validation rule per field (if at all).
- Now that we've established that; `required` only checks whether a field is present on the input array using
  [`array_key_exists`](http://www.php.net/array_key_exists). If the field is not present, *none* of the validation
  rules for this field are executed: With `required = true` in this scenario the validation rule will fail
  with the message of the rule the `required` flag was set on, while `required = false` would lead to the field's
  validation succeeding without any rule being executed.  The default value of `required` is `false`, meaning a field
  doesn't have to be present with the save.
- The `allowEmpty` flag lets you skip all validation rules for a field or fail immediately if the field is left empty.
  This empty check is defined `true` for any value for which [`empty`](http://www.php.net/empty) returns `true`,
  except for `"0"`, which is considered non-empty. Now comes the confusing part: **`allowEmpty` has three possible
  values, not two**. Specifying `true` would cause validation to be skipped if the field is empty, specifying `false`
  causes it to fail in that case. You might already see the missing third case here: the one that skips the empty
  check and just executes the validation rule. This is actually the default behavior - it happens when you don't
  specify `allowEmpty` at all. The explicit equivalent of this would be `allowEmpty = null`.

I hope this settles the confusion once and for all.
