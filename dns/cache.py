#!/usr/bin/env python3

"""A cache for resource records

This module contains a class which implements a cache for DNS resource records,
you still have to do most of the implementation. The module also provides a
class and a function for converting ResourceRecords from and to JSON strings.
It is highly recommended to use these.
"""


import json
import time

from dns.resource import ResourceRecord, CacheRecord


class RecordCache:
    """Cache for ResourceRecords"""

    def __init__(self, ttl):
        """Initialize the RecordCache

        Args:
            ttl (int): TTL of cached entries (if > 0)
        """
        assert ttl >= 0, "TTL must be >= 0"
        self.records = set()
        self.ttl = ttl

    def lookup(self, dname, type_, class_):
        """Lookup resource records in cache

        Lookup for the resource records for a domain name with a specific type
        and class.

        Args:
            dname (Name): domain name
            type_ (Type): type
            class_ (Class): class
        """
        for record in self.records:
            if (
                    record.name == dname and
                    record.type_ is type_ and
                    record.class_ is class_
            ):
                if time.time() - record.added <= record.ttl:
                    return record
                else:
                    self.records.remove(record)
                    return

    def add_record(self, record):
        """Add a new Record to the cache

        Args:
            record (ResourceRecord): the record added to the cache
        """
        self.records.add(CacheRecord(record, time.time()))

    def add_records(self, records):
        """ Add new Records to the cache

        Args:
            records ([ResourceRecord]): the records added to the cache
        """
        self.records.update(set(
            CacheRecord(record, time.time()) for record in records
        ))

    def read_cache_file(self):
        """Read the cache file from disk"""
        records = []
        try:
            with open("cache", "r") as file_:
                records = json.load(file_)
        except:
            print("could not read cache")
        self.records = {CacheRecord.from_dict(dct) for dct in records}

    def write_cache_file(self):
        """Write the cache file to disk"""
        dcts = [record.to_dict() for record in self.records]
        try:
            with open("cache", "w") as file_:
                json.dump(dcts, file_, indent=2)
        except:
            print("could not write cache")
