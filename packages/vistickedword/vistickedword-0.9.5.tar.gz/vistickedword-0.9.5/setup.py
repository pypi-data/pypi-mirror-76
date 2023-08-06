# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['vistickedword']
install_requires = \
['single-version>=1.1,<2.0']

setup_kwargs = {
    'name': 'vistickedword',
    'version': '0.9.5',
    'description': 'Library to split sticked Vietnamese words',
    'long_description': '=============\nViStickedWord\n=============\n\n.. image:: https://badgen.net/pypi/v/vistickedword\n   :target: https://pypi.org/project/vistickedword\n\n\nA library to split a string of many Vietnamese words sticked together to single words. It, for example, split "khuckhuyu" to "khuc" and "khuyu".\nThis library is not supposed to split Vietnamese by semantics, so it won\'t differentiate single or compound words. It will not, for example, split "bacsitrongbenhvien" to "bac si" + "trong" + "benh vien".\nIf you want such a feature, please use underthesea_.\nDue to my personal need, this library currently doesn\'t process fully marked words, like "họamikhônghótnữa". However, it is trivial for library user to strip those marks before passing to ``ViStickedWord`` (using Unidecode_).\n\nTo make convenient for programming, some terminologies are not used accurately like it should be in linguistic. Please don\'t use my code as a source for learning Vietnamese grammar.\n\n----------\n\nThư viện để tách một chùm từ tiếng Việt viết dính liền thành các từ đơn riêng lẻ, ví dụ tách "khuckhuyu" thành "khuc", "khuyu".\nThư viện này không có ý định tách từ dựa theo ngữ nghĩa, nên nó sẽ không phân biệt từ đơn, từ ghép của tiếng Việt. Ví dụ, nó sẽ ko tách cụm "bacsitrongbenhvien" thành "bac si" + "trong" + "benh vien".\nNếu bạn cần tính năng đó, nên sử dụng underthesea_.\n\nDo nhu cầu cá nhân nên hiện tại thư viện không xử lý từ có đầy đủ dấu, ví dụ "họamikhônghótnữa". Tuy nhiên, người dùng thư viện có thể loại bỏ dấu trước khi truyền vào ``ViStickedWord``. Việc đó không khó (dùng Unidecode_).\n\nĐể thuận tiện cho việc lập trình, một số thuật ngữ không được dùng chính xác như cách dùng bên ngôn ngữ học. Vui lòng đừng xem code của tôi là nguồn tài liệu học ngữ pháp tiếng Việt.\n\nInstall\n-------\n\n.. code-block:: sh\n\n    pip install vistickedword\n\n\nUsage\n-----\n\n.. code-block:: python\n\n    from vistickedword import split_words\n\n    split_words(\'ngoanngoeo\')\n\n    # Returns (\'ngoan\', \'ngoeo\')\n\n\nCredit\n------\n\nDeveloped by by `Nguyễn Hồng Quân <author_>`_.\n\n\n.. _underthesea: https://github.com/undertheseanlp/underthesea\n.. _Unidecode: https://pypi.org/project/Unidecode/\n.. _author: https://quan.hoabinh.vn\n',
    'author': 'Nguyễn Hồng Quân',
    'author_email': 'ng.hong.quan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hongquan/ViStickedWord',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
