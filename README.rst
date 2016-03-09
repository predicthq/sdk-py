###############################
PredictHQ API Client for Python
###############################

.. image:: https://badge.fury.io/py/predicthq.svg
    :target: https://badge.fury.io/py/predicthq
.. image:: https://travis-ci.org/predicthq/sdk-py.svg?branch=master
    :target: https://travis-ci.org/predicthq/sdk-py
.. image:: https://coveralls.io/repos/github/predicthq/sdk-py/badge.svg?branch=master
    :target: https://coveralls.io/github/predicthq/sdk-py?branch=master


`PredictHQ <https://www.predicthq.com/>`_ is a global events intelligence platform that aggregates, enriches and connects scheduled and real-time event data happening both locally and globally, then predicts which ones could impact your business.


Installation
############

.. code-block:: shell

    pip install predicthq

Usage
#####

.. code-block:: python

    from predicthq import Client

    phq = Client(access_token="$ACCESS_TOKEN")

    for event in phq.events.search(q="Foo Fighters", rank_level=[4, 5], country='US'):
        print("{} - {} - {} - {}".format(event.rank, event.category, event.title, event.start.strftime('%Y-%m-%d')))

    81 - concerts - Foo Fighters - 2015-11-17
    99 - concerts - Foo Fighters - 2015-11-16

Endpoints
#########

* ``Client.oauth2``
* ``Client.accounts``
* ``Client.events``
* ``Client.signals``

For a description of all available endpoints, refer to our `API Documentation <https://developer.predicthq.com/>`_.

Running Tests
#############

.. code-block:: shell

    pip install tox
    tox

Changelog
#########

0.0.1
*****

* Initial release
