wikigeolinks
============

Adrià Mercader -http://amercader.net ([@amercader](https://twitter.com/amercader))

A [GeoJSON](http://geojson.org) REST service for georeferenced Wikipedia
articles, built with [MapFish](http://mapfish.org).

It was built around the georeferenced Wikipedia articles dataset that can 
be downloaded from this website:

http://amercader.net/dev/wikipedia

You will need to import the dataset to a [PostGIS](http://postgis.org) database
(or any other geodatabase engine supported by [GeoAlchemy](http://geoalchemy.org),
though this has not been tested).


Installation
------------

Create and activate a virtual environment:

    virtualenv --no-site-packages wikigeolinks
    cd wikigeolinks
    source bin/activate
    easy_install pip

Install the source (will also install the other requirements):

    pip install -e git+git://github.com/amercader/wikigeolinks.git#egg=wikigeolinks

Create a configuration file:

    cd src/wikigeolinks
    paster make-config wikigeolinks development.ini

Edit the database connection string to point to your database containing
the georeferenced articles:

    sqlalchemy.url = postgresql://<user_name>:<password>@<server>/<database>

Serve the application with the following command:

    paster serve --reload development.ini

You should get a GeoJSON response visiting the following URL:

http://localhost:5000/articles


API Overview
------------

Georeferenced articles are returned as GeoJSON [Features](http://geojson.org/geojson-spec.html#feature-objects):

    GET http://<server>/articles/<id>

E.g.:

    GET http://<server>/articles/1234

    {
        geometry: {
            type: "Point",
            coordinates: [
                -77.066946,
                38.921473
            ]
        },
        id: 1234,
        type: "Feature",
        bbox: [
            -77.066946,
            38.921473,
            -77.066946,
            38.921473
        ],
        properties: {
            links_count: 7,
            title: "United States Naval Observatory"
        }
    }

You can perform various queries using the [MapFish Protocol](http://trac.mapfish.org/trac/mapfish/wiki/MapFishProtocol)
on the main endpoint:

    GET http://<server>/articles?<query>

* Search by title:

        GET http://<server>/articles?title__ilike=%tarrag%&attrs=id,title,links_count&queryable=title&order_by=links_count&dir=desc&limit=30

* Search by location:

        GET http://<server>/articles?lon=-1.60&lat=54.98&tolerance=0.5&order_by=links_count&dir=desc&limit=30

* Search by bounding box:

        GET http://<server>/articles?bbox=5,50,7,60

All these queries return a [FeatureCollection](http://geojson.org/geojson-spec.html#feature-collection-objects)
of georeferenced articles.

    {
        type: "FeatureCollection",
        features: [
            {
                geometry: {
                    type: "Point",
                    coordinates: [
                        1.25,
                        41.13333333333333
                    ]
                },
                id: 47441,
                type: "Feature",
                bbox: [
                    1.25,
                    41.13333333333333,
                    1.25,
                    41.13333333333333
                ],
                properties: {
                    links_count: 13,
                    title: "Camp de Tarragona"
                }
            },
            {
                geometry: {
                    type: "Point",
                        coordinates: [
                            1.2740638888888889,
                            41.19218055555555
                        ]
                },
                id: 172375,
                type: "Feature",
                bbox: [
                    1.2740638888888889,
                    41.19218055555555,
                    1.2740638888888889,
                    41.19218055555555
                ],
                properties: {
                    links_count: 9,
                    title: "Camp de Tarragona railway station"
                }
            },
            ...
        }

