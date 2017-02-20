#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
IPv4 Address

This is a class to help with the manipulation of IP addresses in python modules.

Example Usage:
IPv4 = reload(IPv4)
addr = IPv4.Address('10.1.2.1')
mask = IPv4.SubnetMask('255.255.0.0')
ntwk = IPv4.Network(addr,mask)

addr in ntwk



"""


class Address:

    value = None

    def __init__(self, address=None):
        if address.__class__ is Address:
            self.value = address.value
        if type(address) == str:
            self.value = self.string_to_int(address)
        if type(address) == int:
            self.value = address

    def string_to_int(self, string):
        try:
            binary = 0
            for (offset, segment) in enumerate(string.split('.')):
                binary += 256 ** (3 - offset) * int(segment)
            return binary
        except Exception:
            raise ValueError('Not Decimal Dotted: {}'.format(string))

    def int_to_string(self, integer):
        segments = [str((integer >> 8 * offset) % 256) for offset in
                    range(3, -1, -1)]
        return '.'.join(segments)

    def __repr__(self):
        return '{0:b}'.format(self.value)

    def __str__(self):
        return self.int_to_string(self.value)


class SubnetMask(Address):

    def __init__(self, address=None):
        if type(address) == str:
            self.value = self.string_to_int(address)
        if type(address) == int:
            self.value = address

        # Check that this is a valid mask

        if not ''.join(sorted('{0:b}'.format(self.value),
                       reverse=True)) == '{0:b}'.format(self.value):
            raise ValueError('Not a valid IPv4 Subnet Mask: {}'.format(address))

    def __str__(self):
        return str(bin(self.value).count('1'))


class Network:

    network_address = None
    subnet_mask = None

    def __init__(self, address, subnet_mask):
        if address.__class__ is not Address:
            raise TypeError()
        if subnet_mask.__class__ is not SubnetMask:
            raise TypeError()
        self.subnet_mask = subnet_mask

        self.network_address = Address(self.subnet_mask.value
                & address.value)

    def __contains__(self, address):
        if address.__class__ is not Address:
            raise TypeError()
        return address.value & self.subnet_mask.value \
            == self.network_address.value

    def __str__(self):
        return '{}/{}'.format(str(self.network_address),
                              str(self.subnet_mask))


class NetworkCollection:

    address_list = []


