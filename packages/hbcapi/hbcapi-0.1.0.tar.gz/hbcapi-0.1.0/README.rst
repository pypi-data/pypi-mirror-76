hbcapi
======

Description
-----------

This is the official api wrapper for hydrogenbots.club

importing and defining
======================

import
------

``pip install hbcapi``

define the library in your code
-------------------------------

.. code:: py

   import hbcapi

   HBC = hbcapi.access("auth_token")

Methods
=======

poststats
---------

post the servercount for your bot

.. code:: py

   print(HBC.poststats(guildcount)) #guildcount is type of numbers, print the response

voters
------

get an array of all of the voters that have voted for your bot

.. code:: py

   print(HBC.poststats()) #print the response