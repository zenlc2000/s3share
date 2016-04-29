# -*- coding: utf-8 -*-
#!/anaconda/envs/python3/bin/python

# s3share v 0.01
# Copyright (c) 2016 Mike Busch

# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to 
# deal in the Software without restriction, including without limitation the 
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
# IN THE SOFTWARE.

"""
Usage: python s3share.py [-h | --help] | [-l | --list] | [-u <file> | -- upload <file>] | [-d <file> | --download <file>] | [-x <file> | --delete <file>]

Options:
    -h, --help                     show this help text
    -l, --list                     list files in s3 bucket
    -u <file> --upload <file>      local file name to upload to S3
    -d <file> --download <file>    s3 file to download to local file system
    -x <file> --delete <file>      s3 file to delete from bucket
"""

from boto.s3.connection import S3Connection
from boto.s3.key import Key
import os
import sys
from docopt import docopt

AWS_KEY = 'MY_KEY'
AWS_SECRET = 'MY_SECRET'

AWS_ACCESSKEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_ACCESSKEY_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")

aws_connection = S3Connection(AWS_ACCESSKEY_ID, AWS_ACCESSKEY_SECRET)
bucket = aws_connection.get_bucket('<public-folder-name')


def list_files():
    '''
    bucket.list() returns a BucketListResultSet that can be iterated 
    to obtain a list of keys contained in a bucket. A key represents 
    some object (e.g., a file) inside of a bucket.
    '''
    for file_key in bucket.list():
        print (file_key.name)

def get_key_from_name(fname):
    for file_key in bucket.list():
        if file_key.name == fname:
            return file_key
    

def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

def delete_file(fname):
    key = get_key_from_name(fname)
    bucket.delete_key(key)
    print('\n\nFile List:')
    list_files()

def upload_file(fpath):
    fname = os.path.split(fpath)[1]
    k = Key(bucket)
    k.key = fname
    print('\nBeginning upload. Progress: ')
    k.set_contents_from_filename(fname, cb=percent_cb, num_cb=10)
    print('\n\nFile List:')
    list_files()
    print('\nDownload URL is: ')
    print(make_https_url(k))
 
 
def make_https_url(k):
    url = 'https://{host}/{bucket}/{key}'.format(host = 's3-us-west-1.amazonaws.com', 
        bucket = 'zens-shared-files', key = k.name)
    return url
    
def make_http_url(k):
    url = 'http://{host}/{bucket}/{key}'.format(host = 's3-us-west-1.amazonaws.com', 
        bucket = 'zens-shared-files', key = k.name)
    return url
    
def download_file(fname):
    key = get_key_from_name(fname)
    key.get_contents_to_filename(fname)
    
if __name__=='__main__':
    args = docopt(__doc__)
#    print(args)

    if args['--list']:
        list_files()
    if args['--upload']:
        upload_file(args['--upload'])
    if args['--delete']:
        delete_file(args['--delete'])        
    
    '''
    print('List before upload: ')
    list_files()
    delete_file('s3share.py')
    print('\nList after delete: ')
    list_files()
    '''