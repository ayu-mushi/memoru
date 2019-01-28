Memoru
=======

* CLI memo command
* Memoru enable to generate memos, and to manipulate memos.
* Each memo has its own unique and random index.
* Suitable for twitter draft
* use the memo stack system

How to install
-------
```sh
git clone https://github.com/ayu-mushi/memoru
cd memoru
python setup.py install
```

Tutorial
--------

###Initialize
Type `memoru init` to initialize a directory for using memoru.

###memoru & tw
https://github.com/shokai/tw

```
vim `memoru gen 'txt'`
memoru pop | tw --pipe
```

Related tools
-----


License
--------
This software is licensed under the MIT license.

See LICENSE file.
