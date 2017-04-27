scribesclasses
==============

package providing support for classrooms with a particular layout on github, with documentation, etc.

* ``manage``: front end and user interface. The entry point just like manage.py in django.

highlevel modules
-----------------

Each module below contains a GitHubEngine that can be called from ``manage.py``

* ``scribesclasses.github``: define classrooms on github. Define the repository layout for a classroom.
* ``scribesclasses.onweb``: define the web insterface of a classrooms. In particular the sphinx generated documentation.
* ``scribesclasses.eval``: define how to evaluate case(s) studies for group(s)
* ``scribesclasses.changespec``: evaluate change specifications on student work.
* ``scribesclasses.commands``: generation of shell commands applying on all groups.
* ``scribesclasses.assignments``: creation, publication and tracking of assignments.
core modules
------------

* ``scribesclasses.classrooms``: define what is a classroom with all its components
* ``scribesclasses.casestudies``: define what is a case study (to be refined)
* ``scribesclasses.assignments``: define what is an assignement
* ``scribesclasses.groups``: define the notions of group and grouplist
* ``scribesclasses.infra.works``: define the notions of work, workDefinition and workItem

