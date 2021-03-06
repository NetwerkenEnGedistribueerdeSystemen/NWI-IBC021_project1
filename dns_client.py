#!/usr/bin/env python3

""" Simple DNS client

A simple example of a client using the DNS resolver.
"""


from argparse import ArgumentParser

from dns.cache import RecordCache
from dns.resolver import Resolver


def resolve():
    """Resolve a hostname using the resolver """
    parser = ArgumentParser(description="DNS Client")
    parser.add_argument("hostname", help="hostname to resolve")
    parser.add_argument("--timeout", metavar="time", type=int, default=5,
                        help="resolver timeout")
    parser.add_argument("-c", "--caching", action="store_true",
                        help="Enable caching")
    parser.add_argument("-t", "--ttl", metavar="time", type=int, default=0,
                        help="TTL value of cached entries (if > 0)")
    args = parser.parse_args()

    cache = RecordCache(args.ttl)
    if args.caching:
        cache.read_cache_file()
        resolver = Resolver(args.timeout, cache)
    else:
        resolver = Resolver(args.timeout)
    hostname, aliaslist, ipaddrlist = resolver.gethostbyname(args.hostname)
    if args.caching:
        cache.write_cache_file()

    print(hostname)
    print(aliaslist)
    print(ipaddrlist)


if __name__ == "__main__":
    resolve()
