Changelog
=========

1.0b2 - 2011-03-19
------------------

* Work around issue with traversing objects with slashes in their key.
  [davisagli]

* Handle case where objects providing interfaces not present in the Python
  environment can't be unpickled even into Broken objects.
  [davisagli]

* Cast non-string dict keys into strings for the sake of traversal.
  [davisagli]

* Handle case where inspect.getmembers hits an AttributeError.
  [davisagli]

* Handle case where ZODB state is not a mapping.
  [davisagli]

* Make it possible to browse ZODB BTrees (as long as they're not too big,
  anyway).
  [davisagli]

1.0b1 - 2011-03-19
------------------

* Initial release.
  [davisagli]
