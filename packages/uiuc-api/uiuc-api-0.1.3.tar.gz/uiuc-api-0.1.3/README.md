About
=====
`uiuc-api` is a simple python package which wraps UIUC's official REST API for querying data about courses. In addition, it deals with some of the annoyances of using the official API by providing some convient structures. Data from the official API is available in XML form, however, it is in an inconvienent-to-parse format. For instance, take the XML data for CS 173:
```xml
<label>Discrete Structures</label>

<description>Discrete mathematical structures frequently encountered in the study of Computer Science. Sets, propositions, Boolean algebra, induction, recursion, relations, functions, and graphs. Credit is not given for both CS 173 and MATH 213. Prerequisite: One of CS 125, ECE 220; one of MATH 220, MATH 221.</description>

<creditHours>3 hours.</creditHours>

<courseSectionInformation>Credit is not given for both CS 173 and MATH 213. Prerequisite: One of CS 125, ECE 220; one of MATH 220, MATH 221.</courseSectionInformation>

<classScheduleInformation>Students must register for a lecture and discussion section.</classScheduleInformation>
```
It is tedious, for example, to accurately parse out the prerequisites in a easy-to-manipulate form. `uiuc-api` does this for the user:
```py
>>> import uiuc_api as ua
>>> ua.get_course("CS 173").serialize()
```
Output:
```yaml
CS 173:
  subject: CS
  number: '173'
  hours: 3
  label: Discrete Structures
  description: 'Discrete mathematical structures frequently encountered in the study
    of Computer Science. Sets, propositions, Boolean algebra, induction, recursion,
    relations, functions, and graphs. Credit is not given for both CS 173 and MATH
    213. Prerequisite: One of CS 125, ECE 220; one of MATH 220, MATH 221.'
  schedule_info: 'Credit is not given for both CS 173 and MATH 213. Prerequisite:
    One of CS 125, ECE 220; one of MATH 220, MATH 221.'
  prereqs:
  - !!python/object/apply:builtins.frozenset
    - - ECE 220
      - CS 125
  - !!python/object/apply:builtins.frozenset
    - - MATH 220
      - MATH 221
  coreqs: []
  constraints: []
```
Installation
=========
Install the `uiuc_api`  module via pip (`uiuc-api` also works):
```bash
pip install uiuc_api
```
Documentation
=========
See https://uiuc-api.readthedocs.io/en/main/.
