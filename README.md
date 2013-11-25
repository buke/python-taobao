python-taobao
==============

作者： wangbuke@gmail.com

python-taobao is a library to write taobao-open-platform api in a pythonic way.


Install::

    # pip install -e git+https://github.com/buke/python-taobao.git#egg=python-taobao

Uninstall::

    # pip uninstall python-taobao


Nutshell
--------

Import::

    >>> import taobao

Simple User::

    >>> top = taobao.ServerProxy(app_key = "xxx", app_secret="xxx", session="xxx")
    >>> seller = top.taobao.user.seller.get(fields=['nick','sex'])
    >>> dict(seller)
    {'nick': 'seller_nick', 'sex': 1}

    >>> seller.nick 
    'seller_nick'

    >>> seller.sex 
    1 


支持开源：
----------

如果您觉得好用，请进入下面的网址，付费支持作者 ~

http://me.alipay.com/wangbuke

谢谢！



