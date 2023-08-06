"""MongoDB Apache Beam IO utilities.
Tested with google-cloud-dataflow package version 2.19.0
"""

__all__ = ['ReadFromMongo']

import datetime
import logging
import re
from pymongo import MongoClient
from apache_beam.transforms import PTransform
from apache_beam.io import iobase, range_trackers

logger = logging.getLogger(__name__)


def mongo_connection_string(url):
    """Extract the MongoDB connection string given MongoDB url.
    If the string contains a Cloud Storage url, the url is assumed to be the
    first line of a text file at that location.
    """
    if 'gs://' in url:
        from google.cloud import storage
        logging.info('Fetching connection string from Cloud Storage {}'.format(url))

        # Split gs://my-bucket/my-file.txt into my-bucket and my-file.txt separately.
        _, path = url.split('gs://')
        path = path.split('/')
        bucket = path[0]
        path = '/'.join(path[1:])

        # Fetch the file
        client = storage.Client()
        blob = client.get_bucket(bucket).get_blob(path).download_as_string()

        # Assume the connection string is on the first line.
        connection_string = blob.splitlines()[0]
        return connection_string.decode("utf-8")
    logger.info('Using connection string from CLI options')
    return url


iso_match = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}')


def clean_query(query):
    new_query = {}
    for key, val in query.items():
        if isinstance(val, str):
            val = str(val) # Because unicode and 2.7 :-(

        # If the string is an ISO date, turn it into a real datetime object so pymongo can understand it.
        if isinstance(val, str) and iso_match.match(val):
            val = datetime.datetime.strptime(val[0:19], '%Y-%m-%dT%H:%M:%S')
        elif isinstance(val, dict):
            val = clean_query(val)
        new_query[str(key)] = val
    return new_query


class _MongoSource(iobase.BoundedSource):
    """A :class:`~apache_beam.io.iobase.BoundedSource` for reading from MongoDB."""

    def __init__(self, connection_string, db, collection, query=None, fields=None):
        """Initializes :class:`_MongoSource`"""
        self._connection_string = connection_string
        self._db = db
        self._collection = collection
        self._fields = fields
        self._client = None

        # Prepare query
        self._query = query
        if not self._query:
            self._query = {}
        logger.info('Raw query: {}'.format(query))
        self._query = clean_query(self._query)
        logger.info('Cleaned query: {}'.format(self._query))

    @property
    def client(self):
        """Returns a PyMongo client. The client is not pickable so it cannot
        be part of the main object.
        """
        if self._client:
            logger.info('Reusing existing PyMongo client')
            return self._client

        # Prepare client, assumes a full connection string.
        logger.info('Preparing new PyMongo client')
        real_connection_string = mongo_connection_string(self._connection_string)
        self._client = MongoClient(real_connection_string)
        return self._client

    def estimate_size(self):
        """Implements :class:`~apache_beam.io.iobase.BoundedSource.estimate_size`"""
        return None

    def get_range_tracker(self, start_position, stop_position):
        """Implements :class:`~apache_beam.io.iobase.BoundedSource.get_range_tracker`"""
        if start_position is None:
            start_position = 0
        if stop_position is None:
            stop_position = range_trackers.OffsetRangeTracker.OFFSET_INFINITY

        # Use an unsplittable range tracker. This means that a collection can
        # only be read sequentially for now.
        range_tracker = range_trackers.OffsetRangeTracker(start_position, stop_position)
        range_tracker = range_trackers.UnsplittableRangeTracker(range_tracker)

        return range_tracker

    def read(self, range_tracker):
        """Implements :class:`~apache_beam.io.iobase.BoundedSource.read`"""
        coll = self.client[self._db][self._collection]
        for doc in coll.find(self._query, projection=self._fields):
            yield doc

    def split(self, desired_bundle_size, start_position=None, stop_position=None):
        """Implements :class:`~apache_beam.io.iobase.BoundedSource.split`
        This function will currently not be called, because the range tracker
        is unsplittable
        """
        if start_position is None:
            start_position = 0
        if stop_position is None:
            stop_position = range_trackers.OffsetRangeTracker.OFFSET_INFINITY

        # Because the source is unsplittable (for now), only a single source is
        # returned.
        yield iobase.SourceBundle(
            weight=1,
            source=self,
            start_position=start_position,
            stop_position=stop_position)


class ReadFromMongo(PTransform):
    """A :class:`~apache_beam.transforms.ptransform.PTransform` for reading
    from MongoDB.
    """
    def __init__(self, connection_string, db, collection, query=None, fields=None):
        """Initializes :class:`ReadFromMongo`
        Uses source :class:`_MongoSource`
        """
        super(ReadFromMongo, self).__init__()
        self._connection_string = connection_string
        self._db = db
        self._collection = collection
        self._query = query
        self._fields = fields
        self._source = _MongoSource(
            self._connection_string,
            self._db,
            self._collection,
            query=self._query,
            fields=self._fields)

    def expand(self, pcoll):
        """Implements :class:`~apache_beam.transforms.ptransform.PTransform.expand`"""
        logger.info('Starting MongoDB read from {}.{} with query {}'
                    .format(self._db, self._collection, self._query))
        return pcoll | iobase.Read(self._source)

    def display_data(self):
        return {'source_dd': self._source}