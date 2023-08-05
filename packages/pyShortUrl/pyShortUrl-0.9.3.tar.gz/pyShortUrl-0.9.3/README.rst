
===========
pyshorturl
===========

A python library to shorten urls using various url shortening serices. Republished from the previously released library by `Parth Bhatt`_.

Following table lists details for each of the supported services:

  +--------------+----------------------+-----------+
  | Domain       |  Shorten/Expand URLs |  QR code  |
  +--------------+----------------------+-----------+
  | bit.ly       |        YES           |   NO      |
  +--------------+----------------------+-----------+
  | bitly.com    |        YES           |   NO      |
  +--------------+----------------------+-----------+
  | gimme.bar    |        YES           |   NO      |
  +--------------+----------------------+-----------+
  | git.io       |        YES           |   NO      |
  +--------------+----------------------+-----------+
  | goo.gl       |        YES           |   YES     |
  +--------------+----------------------+-----------+
  | is.gd        |        YES           |   NO      |
  +--------------+----------------------+-----------+
  | j.mp         |        YES           |   NO      |
  +--------------+----------------------+-----------+
  | tinyurl.com  |        YES           |   NO      |
  +--------------+----------------------+-----------+
  | v.gd         |        YES           |   NO      |
  +--------------+----------------------+-----------+


Install
=======

To install pyshorturl:

::

  python setup.py install


Using pyshorturl
================

pyshorturl provides simple APIs that your python applications can use. Following
are some examples that show how you can use pyShortUrl with goo.gl.

Using pyshorturl for URL shortening with *goo.gl*
-------------------------------------------------

Shorten a URL using goo.gl:

::

    from pyshorturl import Googl, GooglError

    long_url = 'http://www.parthbhatt.com/blog/'
    service = Googl(api_key=<your_api_key>)
    try:
        short_url = service.shorten_url(long_url)
        print short_url
    except GooglError, e:
        print 'Error: %s' %e


Expand a goo.gl short url back to the original long url:

::

    from pyshorturl import Googl, GooglError

    short_url = 'http://goo.gl/RwsEG'
    service = Googl(api_key=<your_api_key>)
    try:
        long_url = service.expand_url(short_url)
        print long_url
    except GooglError, e:
        print 'Error: %s' %e



Get QR code for a goo.gl short url:

::

    from pyshorturl import Googl, GooglError

    short_url = 'http://goo.gl/RwsEG'
    qr_img_path = '/path/to/qr_code.png'
    service = Googl()
    try:
        service.write_qr_image(short_url, qr_img_path)
    except GooglError, e:
        print 'Error: %s' %e


Using pyshorturl for URL shortening with *bit.ly*, *j.mp* and *bitly.com*
-------------------------------------------------------------------------

You can use bit.ly exactly like you'd use goo.gl. Just initialize the *service*
object in the snippets above using *Bitly* instead of *Googl*.

::

    from pyshorturl import Bitly, BitlyError

    service = Bitly(<your_bit.ly_login>, <your_bit.ly_api_key>)


Note that it is mandatory to associate every call to bit.ly with a valid
account and an API Key. Hence, to use URL shortening with bit.ly you will need
to provide an account name and API key.

To shorten a url using *j.mp* or *bitly.com*, specify the domain as an argument
to the `shorten` function call as shown below:

::

    from pyshorturl import Bitly, BitlyError

    long_url = 'http://www.parthbhatt.com/blog/'
    service = Bitly(<your_bit.ly_login>, <your_bit.ly_api_key>)
    try:
        short_url = service.shorten_url(long_url, domain='j.mp')
        print short_url
    except BitlyError, e:
        print '%s' %e

Using pyshorturl for URL shortening with *tinyurl.com*
------------------------------------------------------

::

    from pyshorturl import TinyUrlcom
    
    service = TinyUrlcom()

You dont need any account name or api key to use TinyUrl.


Using the pyshorturl-cli.py utility
===================================

pyshorturl ships with a command-line utility called `pyshorturl-cli.py` that
allows you to use all the features of the library from the command line.

::

    $ python pyshorturl-cli.py -h
    Options:
      -h, --help            show this help message and exit
      -r SERVICE, --service=SERVICE
                            One of the shortening services
                            goo.gl,bit.ly,tinyurl.com,v.gd,is.gd. Defaults to
                            goo.gl
      -d DOMAIN, --domain=DOMAIN
                            Domain bit.ly, j.mp or bitly.com to use while
                            shortening with bit.ly. Defaults to bit.ly
      -u LOGIN, --login=LOGIN
                            The user account to use with the url shortening
                            service.
      -l LONG_URL, --long-url=LONG_URL
                            Shorten the specified URL.
      -k SVC_API_KEY, --api-key=SVC_API_KEY
                            Use API Key while communicating with the url
                            shortening service.
      -s SHORT_URL, --short-url=SHORT_URL
                            Expand the specified Short URL.
      -q QR_IMG_PATH, --qr-code-file=QR_IMG_PATH
                            Used with -s. Writes the QR code for the corresponding
                            short url.


Some examples of using the pyshorturl-cli.py utility:

Shorten a long url using goo.gl:

::

    $ python pyshorturl-cli.py --service goo.gl --long-url http://www.parthbhatt.com/blog/2011/geolocation-with-google-maps-javascript-api/ --api-key <your-api-key>
    http://goo.gl/NMdyG

Obtain the original long url for a goo.gl short url:

::

    $ python pyshorturl-cli.py --short-url http://goo.gl/NMdyG --api-key <your_goo.gl_api_key>
    http://www.parthbhatt.com/blog/2011/geolocation-with-google-maps-javascript-api/

Get the QR code for a goo.gl short url:

::

    $ python pyshorturl-cli.py --short-url http://goo.gl/NMdyG --qr-code-file qr_code.png
    Wrote the qr code for http://goo.gl/NMdyG to qr_code.png

Shorten a long url using bit.ly:

::

    $ python pyshorturl-cli.py --service bit.ly --login <your_bit.ly_account> --api-key <your_bit.ly_api_key> -l http://www.parthbhatt.com/blog/
    http://bit.ly/xJHGkJ

Shorten a long url using j.mp:

::

    $ python pyshorturl-cli.py --service bit.ly --login <your_bit.ly_account> --api-key <your_bit.ly_api_key> --domain j.mp -l http://www.parthbhatt.com/blog/
    http://j.mp/xJHGkJ

Obtain the original long url for a bit.ly short url:

::

    $ python pyshorturl-cli.py --service bit.ly --login <your_bit.ly_account> --api-key <your_bit.ly_api_key> -s http://bit.ly/xJHGkJ
    http://www.parthbhatt.com/blog/

Get the QR code for a bit.ly short url:

::

    $ python pyshorturl-cli.py --service bit.ly --login <your_bit.ly_account> --api-key <your_bit.ly_api_key> --short-url http://bit.ly/xJHGkJ --qr-code-file qr_code.png
    Wrote the qr code for http://bit.ly/xJHGkJ to qr_code.png


Shorten a long url using tinyurl.com:

::

    $ python pyshorturl-cli.py --service tinyurl.com --long-url http://www.parthbhatt.com/blog/
    http://tinyurl.com/8yuvzl5

Obtain the original long url for a tinyurl.com short url:

::

    $ python pyshorturl-cli.py --service tinyurl.com --short-url http://tinyurl.com/8yuvzl5
    http://www.parthbhatt.com/blog/


Shorten a long url using git.io:

::

    $ python pyshorturl-cli.py --service git.io --long-url https://github.com/parthrbhatt/pyShortUrl
    https://git.io/sUX2IQ

Retrieve the original long url with git.io:

::

    $ python pyshorturl-cli.py --service git.io --short-url https://git.io/sUX2IQ
    https://github.com/parthrbhatt/pyShortUrl


.. _Parth Bhatt: https://github.com/parthrbhatt
