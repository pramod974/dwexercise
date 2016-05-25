__author__ = 'pramodkumar'
from time import time
from random import randint,random,getrandbits
import uuid
import sys
if len(sys.argv)>1:
    long_url=sys.argv[1]
#Constants for encoding the string
BASE_ALPH = tuple("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
#Enumerating the Constants
BASE_DICT = dict((c, v) for v, c in enumerate(BASE_ALPH))
BASE_LEN = len(BASE_ALPH)

#Method to Decode the string
def base_decode(string):
   num = 0
   for char in string:
       num = num * BASE_LEN + BASE_DICT[char]
   return num
#Method to encode the number
def base_encode(num):
   if not num:
       return BASE_ALPH[0]

   encoding = ""
   while num:
       num, rem = divmod(num, BASE_LEN)
       encoding = BASE_ALPH[rem] + encoding
   return encoding
#Method takes a long string URL as input returns Short URL
def shorten(long_url):
    #Logic 1 to get rand bits for encoding we can mask the UUID generated
    # id=uuid.uuid1().int>>64
    #Using Logic 2 to get rand bits for encoding
    id=getrandbits(40)
    short_url=base_encode(id)
    return short_url
#Method to covert URLs in text file and return the list of short URLs
def shortenfile(absoluteFileName):
    with open(absoluteFileName,"r") as f:
        line=f.readline().strip()
        shortlines=[]
        originalURL=[]
        while(line):
            shortlines.append(shorten(line))
            originalURL.append(line)
            line=f.readline().strip()
        return originalURL,shortlines