#!/usr/bin/python

#   Copyright 2017 John Bailey
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# Based on the encoding method described at
#  https://sqlite.org/src4/doc/trunk/www/varint.wiki

from ..varints import varint_storage
from ..varints import store_to_num

def encode( num ):
    ret_val = None
    if( num < 241 ):
        ret_val = varint_storage( num )
    elif( num < 2288 ):
        top = num-240
        ret_val = varint_storage( (top // 256)+241 ) + \
                  varint_storage( top % 256 )
    elif( num < 67824 ):
        top = num-2288
        ret_val = varint_storage( 249 ) + \
                  varint_storage( top // 256 ) + \
                  varint_storage( top % 256 )
    elif( num < 67824 ):
        top = num-2288
        ret_val = varint_storage( 249 ) + \
                  varint_storage( top // 256 ) + \
                  varint_storage( top % 256 )
    elif( num < 16777216 ):
        top = num % 65536
        ret_val = varint_storage( 250 ) + \
                  varint_storage( num // 65536 ) + \
                  varint_storage( top // 256 ) + \
                  varint_storage( top % 256 )
    return ret_val

def decode( num ):
    ret_val = None
    first = store_to_num( num[ 0 ] )
    if( first < 241 ):
        ret_val = first
    elif( first < 249 ):
        second = store_to_num( num[ 1 ] )
        ret_val = 240+(256*(first-241))+second
    elif( first == 249 ):
        second = store_to_num( num[ 1 ] )
        third = store_to_num( num[ 2 ] )
        ret_val = 2288+(256*second)+third
    elif( first == 250 ):
        second = store_to_num( num[ 1 ] )
        third = store_to_num( num[ 2 ] )
        fourth = store_to_num( num[ 3 ] )
        ret_val = (second*65536) + (third*256) + fourth
    return ret_val
