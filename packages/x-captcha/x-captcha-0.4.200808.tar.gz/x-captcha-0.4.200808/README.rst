x-captcha
=========

A simple and powerful captcha generation library.

Features
--------

1. Easy to use.
2. Parameterization.
3. Powerful.
4. Continuous updating.

Installation
------------

Install x-captcha with pip::

    $ pip install x-captcha

Usage
-----

Image captcha:

.. code:: python

    from xcaptcha.image import Captcha

    # default
    generator = Captcha()
    captcha, image = generator.generate()

    # parameter
    size = (200, 100)
    characters = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    number = 6
    font = 'data/msyhbd.ttf'
    generator = Captcha(size, characters, number, font)
    captcha, image = generator.generate()

    # config
    generator = Captcha()
    size = (200, 100)
    characters = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    number = 6
    font = 'data/msyhbd.ttf'
    generator.config(size, characters, number, font)
    captcha, image = generator.generate()

    # save
    generator = Captcha()
    generator.save()
    generator.save('captcha/captcha.png')

This is the APIs for your daily works.

Contribution
------------


