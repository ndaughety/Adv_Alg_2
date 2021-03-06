#!/usr/bin/python3

import hashlib



class Base58():

    def __init__(alphabet = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'):
        self.alphabet = alphabet
        self.base_count = len(self.alphabet)


    def encode(self, num):
        """ Returns num (int) in a base58-encoded string """
        encode =''
        assert(type(num) == int)

        if (num < 0):
            return ''

        while (num >= self.base_count):
            mod = num % self.base_count
            assert(type(mod) == int and mod < 58)
            encode = self.alphabet[mod] + encode
            num = num // self.base_count

        if (num):
            encode = self.alphabet[num] + encode

        return encode


    def decode(self, s):
        """ Decodes the base58-encoded string s into an integer """
        decoded = 0
        multi = 1
        s = s[::-1]

        for char in s:
            decoded += multi * self.alphabet.index(char)
            multi = multi * self.base_count

        return decoded


    # get 20 byte address -- TODO: this does not necessarily
    # fit with this class and should probably be moved to a
    # Blockchain class
    def getHashedAddress(self, publicKey):
        return hashlib.ripemd160(hashlib.sha256(publicKey))
