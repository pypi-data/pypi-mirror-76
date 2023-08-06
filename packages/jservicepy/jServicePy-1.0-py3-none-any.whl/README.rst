jServicePy
==========

API wrapper for jService (comes with a commmand-line game
implementation!)

|jService Logo|

A wrapper for `jService`_ and a small command-line based version of
Jeopardy using said wrapper with ANSI escape codes.

Examples
--------

API
~~~

.. code:: python

   from jservicepy import jService
   jeopardy = jService() # <- If you're running your own instance, put your base URL in here
   clues = jeopardy.clues()
   for clue in clues:
       print(clue.question + ':', clue.answer, '| $' + str(clue.value))

CLI
~~~

::

   python -m jservicepy -h
   usage: jServicePy [-h] [-c NUMBER] [-r NUMBER] [-v]

   Play Jeopardy in your terminal! Powered by @sottenad's jService
   [https://github.com/sottenad/jService] (v1.0)

   optional arguments:
     -h, --help            show this help message and exit
     -c NUMBER, --categories NUMBER
                           Answer questions from a NUMBER of random categories.
     -r NUMBER, --random NUMBER
                           Answer a NUMBER of random questions
     -v, --version         show program's version number and exit

Application Programming Interfacte Documentation
------------------------------------------------

class jService
~~~~~~~~~~~~~~

**init**
^^^^^^^^

Initialize jService.

Args:
     

-  baseURL (str, optional): Base URL to send requests to; use if you are
   making calls to your own instance of jService. Defaults to
   "`https://jservice.io"`_.

categories
^^^^^^^^^^

Get a list of categories.

.. _args-1:

Args:
     

-  count (int, optional): Amount of categories to return, limited to 100
   at a time. Defaults to 1. offset (int, optional): Offsets the
   starting ID of categories returned. Useful in pagination. Defaults to
   0.

Returns:
        

-  list: A list of Category dataclasses.

category
^^^^^^^^

Get a category.

.. _args-2:

Args:
     

-  id (int): The ID of the category to return.

.. _returns-1:

Returns:
        

-  Category: A dataclass containing the cateory ID, title, number of
   clues, and list of clues for the category.

clues
^^^^^

Get a list of clues.

.. _args-3:

Args:
     

-  value (int, optional): The value of the clue in dollars.
-  category (int, optional): The id of the category you want to return.
-  min_date (datetime, optional): Earliest date to show, based on
   original air date.
-  max_date (datetime, optional): Latest date to show, based on original
   air date.
-  offset (int, optional): Offsets the returned clues. Useful in
   pagination.

.. _returns-2:

Returns:
''''''''

-  list: A list of Clue dataclasses.

random
^^^^^^

Get random clues.

.. _args-4:

Args:
     

-  count (int, optional): Amount of clues to return, limited to 100 at a
   time. Defaults to 1.

.. _returns-3:

Returns:
        

-  list: A list of Clue dataclasses.

.. _jService: https://jservice.io
.. _`https://jservice.io"`: https://jservice.io"

.. |jService Logo| image:: https://jservice.io/assets/trebek-503ecf6eafde622b2c3e2dfebb13cc30.png