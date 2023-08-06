AWS Triggers
============

Some classes to get information from AWS triggers easily.

Some examples
-------------

Here's some of the stuff you can do:

.. code:: python

    # import all
    from awstriggers import *

    def lambda_handler(event, context):

        for record in event['Records']:

            trigger = SQSTrigger(record)

            print(trigger.body)
            print(trigger.attributes)

Installation
------------

.. code:: bash

    pip install awstriggers
