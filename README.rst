LIFTS
=====

Query-able lifting log with Flask interface.

I want to be able to track my workouts for each day with relative ease
and have them hosted so that when at the gym I can look for what I
previously did for sets/reps/weight if I can't remember.

Originally I planned on using SQL, but switched to Redis for simple
prototyping. Before I even got far with that I felt a flat-file might
be more appropriate.

Data storage format
-------------------

A single file with entries (most recent at top) like:
::

   01/09/14 hangsnatchhighpull 95x3 95x3 135x3 155x2 195x2 195x2 195x2 "didn't pull high enough at 195"
   date exercise weightxrep weightxrep ... "notes notes notes"

TODO
----

- CLI remove
- Group lifts by date
- Reorder input by date
- Flask exact search
- Flask query date
- Specify kg vs lbs
