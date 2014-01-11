Lifts
=====

Query-able lifting log with Flask interface.

I want to be able to track my workouts for each day with relative ease
and have them hosted so that when at the gym I can look for what I
previously did for sets/reps/weight if I can't remember.

Notes
-----

Originally I planned on using SQL, but switched to Redis for simple
prototyping. Before I even got far with that I felt a flat-file might
be more appropriate.

CLI doesn't provide much utility as editting with the flat file is just as easy.

Data storage format
-------------------

A single file with entries (most recent at top) like:
::

   01/09/14 hangsnatchhighpull 95x3 95x3 135x3 155x2 195x2 195x2 195x2 "didn't pull high enough at 195"
   0
   12/30/14 descsnatch kg 40x3 40x3 40x3 50x2 60x2 65x2- 65x1- 65x1- ...
   date exercise [kg/lbs] weightxrep weightxrep ... "notes notes notes"

To set units to kg, kg has to be included, but lbs assumed by default. Output currently set to lbs.

A failed set is indicated by a dash: e.g. 65x1-.

TODO
----

- CLI remove
- Group lifts by date
- Reorder input by date
- Flask exact search
- Flask query date
