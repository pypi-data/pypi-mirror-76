Coronavirus (COVID-19) in the UK - API Service
==============================================

|PyPi_Version| |PyPi_Status| |Format| |Supported_versions_of_Python| |lgtm| |License|


Software Development Kit (SDK) for Python
-----------------------------------------

This is a Python SDK for the COVID-19 API, as published by Public Health England
on `Coronavirus (COVID-19) in the UK`_.

The API supplies the latest data for the COVID-19 outbreak in the United Kingdom. 

The endpoint for the data provided using this SDK is:

    https://api.coronavirus.data.gov.uk/v1/data

The SDK is also available for `JavaScript`_ and `R`_.

Pagination
..........

Using this SDK will bypass the pagination process. You will always download the entire
dataset unless the ``latest_by`` argument is defined.


Installation
............

Python 3.7+ is required to install and use this library.

To install, please run:

.. code-block:: bash

    python -m pip install uk-covid19

and import it in Python as follows:

.. code-block:: python

    from uk_covid19 import Cov19API


Note that you must use ``uk_covid19`` (with an underscore, not a hyphen) to import the
library in Python.

Example
.......

We would like to extract the number of new cases, cumulative cases, new deaths and
cumulative deaths for England using the API.

We start off by importing the library into our workspace:

.. code-block:: python

    from uk_covid19 import Cov19API


Next, we construct the value of the ``filters`` parameter:

.. code-block:: python

    england_only = [
        'areaType=nation',
        'areaName=England'
    ]

Next step is to construct the value of the ``structure`` parameter. To do so, we need to
find out the name of the metric in which we are interested. You can find this information
in the Developer's Guide on the Coronavirus Dashboard website.

In the case of this example, the metrics are as follows:

- ``newCasesByPublishDate``: New cases (by publish date)
- ``cumCasesByPublishDate``: Cumulative cases (by publish date)
- ``newDeathsByDeathDate``: New deaths (by death date)
- ``cumDeathsByDeathDate``: Cumulative deaths (by death date)

In its simplest form, we construct the structure as follows:

.. code-block:: python

    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeathsByDeathDate": "newDeathsByDeathDate",
        "cumDeathsByDeathDate": "cumDeathsByDeathDate"
    }


Now, we may use ``filters`` and ``structure`` to initialise the ``Covid19API`` object:

.. code-block:: python

    api = Cov19API(filters=england_only, structure=cases_and_deaths)
    data = api.get_json()  # Returns a dictionary
    print(data)


You may also use ``data.get_xml()`` or ``data.get_csv()`` to download the data in other
available formats.

::

    {
        'data': [
            {
                'date': '2020-07-28',
                'areaName': 'England',
                'areaCode': 'E92000001',
                'newCasesByPublishDate': 547,
                'cumCasesByPublishDate': 259022,
                'newDeathsByDeathDate': None,
                'cumDeathsByDeathDate': None
            },
            {
                'date': '2020-07-27',
                'areaName': 'England',
                'areaCode': 'E92000001',
                'newCasesByPublishDate': 616,
                'cumCasesByPublishDate': 258475,
                'newDeathsByDeathDate': 20,
                'cumDeathsByDeathDate': 41282
            },
            ...
        ],
        'lastUpdate': '2020-07-28T15:34:31.000000Z',
        'length': 162,
        'totalPages': 1
    }


To see the timestamp for the last update, run:

.. code-block:: python

    print(api.last_update)

::

    2020-07-28T15:34:31.000000Z


To get the latest data by a specific metric, run:

.. code-block:: python

    all_nations = [
        "areaType=nation"
    ]

    api = Cov19API(
        filters=all_nations,
        structure=cases_and_deaths,
        latest_by="newCasesByPublishDate"
    )

    data = api.get_json()

    print(data)

::

    {
        "data": [
            {
                "date": "2020-07-28",
                "areaName": "England",
                "areaCode": "E92000001",
                "newCasesByPublishDate": 547,
                "cumCasesByPublishDate": 259022,
                "newDeathsByDeathDate": None,
                "cumDeathsByDeathDate": None
            },
            {
                "date": "2020-07-28",
                "areaName": "Northern Ireland",
                "areaCode": "N92000002",
                "newCasesByPublishDate": 9,
                "cumCasesByPublishDate": 5921,
                "newDeathsByDeathDate": None,
                "cumDeathsByDeathDate": None
            },
            {
                "date": "2020-07-28",
                "areaName": "Scotland",
                "areaCode": "S92000003",
                "newCasesByPublishDate": 4,
                "cumCasesByPublishDate": 18558,
                "newDeathsByDeathDate": None,
                "cumDeathsByDeathDate": None
            },
            {
                "date": "2020-07-28",
                "areaName": "Wales",
                "areaCode": "W92000004",
                "newCasesByPublishDate": 21,
                "cumCasesByPublishDate": 17191,
                "newDeathsByDeathDate": None,
                "cumDeathsByDeathDate": None
            }
        ],
        "lastUpdate": "2020-07-28T15:34:31.000000Z",
        "length": 4,
        "totalPages": 1
    }


Set the ``save_as`` input argument to a path to save the data in a file. This
functionality is only available for ``.get_json()``, ``.get_xml()`` and ``.get_csv()``
methods.

Note that the ``save_as`` argument must be set to a file name with the correct extension;
that is, ``.json`` for JSON data, ``.xml`` for XML data, and ``.csv`` for CSV data. It is
assumed that the directory in which you wish to save the file already exists.

You may use relative or absolute paths.

.. code-block:: python

    path = "data.csv"

    api.get_csv(save_as="some_existing_directory/data.csv")


This will create a file entitled ``data.csv`` under ``some_existing_directory``. The
contents of the file would be as follows:

::

    date,areaName,areaCode,newCasesByPublishDate,cumCasesByPublishDate,newDeathsByDeathDate,cumDeathsByDeathDate
    2020-07-28,England,E92000001,547,259022,,
    2020-07-28,Northern Ireland,N92000002,9,5921,,
    2020-07-28,Scotland,S92000003,4,18558,,
    2020-07-28,Wales,W92000004,21,17191,,


Set the ``as_string`` input argument to ``True`` for the ``.get_json()`` method if you
wish to receive the result as a JSON string instead of a ``dict`` object:

.. code-block:: python

    data = api.get_json(as_string=True)
    print(data)

::

    {"data":[{"date":"2020-07-28","areaName":"England","areaCode":"E92000001","newCasesByPublishDate":547,"cumCasesByPublishDate":259022,"newDeathsByDeathDate":null,"cumDeathsByDeathDate":null},{"date":"2020-07-28","areaName":"Northern Ireland","areaCode":"N92000002","newCasesByPublishDate":9,"cumCasesByPublishDate":5921,"newDeathsByDeathDate":null,"cumDeathsByDeathDate":null},{"date":"2020-07-28","areaName":"Scotland","areaCode":"S92000003","newCasesByPublishDate":4,"cumCasesByPublishDate":18558,"newDeathsByDeathDate":null,"cumDeathsByDeathDate":null},{"date":"2020-07-28","areaName":"Wales","areaCode":"W92000004","newCasesByPublishDate":21,"cumCasesByPublishDate":17191,"newDeathsByDeathDate":null,"cumDeathsByDeathDate":null}],"lastUpdate":"2020-07-28T15:34:31.000000Z","length":4,"totalPages":1}



-----------

Developed and maintained by `Public Health England`_.

Copyright (c) 2020, Public Health England.

.. _`Coronavirus (COVID-19) in the UK`: http://coronavirus.data.gov.uk/
.. _`Public Health England`: https://www.gov.uk/government/organisations/public-health-england
.. _`JavaScript`: https://github.com/publichealthengland/coronavirus-dashboard-api-javascript-sdk
.. _`R`: https://github.com/publichealthengland/coronavirus-dashboard-api-R-sdk

.. |PyPi_Version| image:: https://img.shields.io/pypi/v/uk-covid19
.. |PyPi_Status| image:: https://img.shields.io/pypi/status/uk-covid19
.. |Format| image:: https://img.shields.io/pypi/format/uk-covid19
.. |Supported_versions_of_Python| image:: https://img.shields.io/pypi/pyversions/uk-covid19
.. |License| image:: https://img.shields.io/github/license/publichealthengland/coronavirus-dashboard-api-python-sdk
.. |lgtm| image:: https://img.shields.io/lgtm/grade/python/github/publichealthengland/coronavirus-dashboard-api-python-sdk