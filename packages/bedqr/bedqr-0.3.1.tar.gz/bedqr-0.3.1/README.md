bedqr
=====

BED Quick Reader


Quick Start
-----------

Load data from disk:

```python
from bedqr.reader import QuickReader
bed = QuickReader(open('/path/to/demo.bed', 'r')).data
```
Access row data:

```python
for row in bed.body:
    print bed.get_cells_from_row(row)
```

TODO
----

- implement parsing logic for header fields
- add config for PyLint, Flask8
- add unittest

License
-------

This software is licensed under Apache License Version 2.0.

You should have received a copy of the Apache License along with this program.  If not, see [here](http://www.apache.org/licenses/LICENSE-2.0).
