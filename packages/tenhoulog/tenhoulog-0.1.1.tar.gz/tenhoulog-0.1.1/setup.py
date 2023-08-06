# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tenhoulog']

package_data = \
{'': ['*']}

install_requires = \
['beautifultable>=1.0.0,<2.0.0',
 'httpx>=0.13.3,<0.14.0',
 'japanize-matplotlib>=1.1.2,<2.0.0',
 'matplotlib>=3.3.0,<4.0.0',
 'pandas>=1.1.0,<2.0.0',
 'pydantic>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'tenhoulog',
    'version': '0.1.1',
    'description': 'utils for tenhou log',
    'long_description': '# tenhoulog\n\n## インストール\n\n```sh\npip install tenhoulog\n```\n\n## GameResult object\n\nGameResultオブジェクトは1試合の結果を保持します。\n\n### 文字列から生成\n\n```py\n>>> log_str = """\n>>> L1000 | 00:30 | 四般南喰赤－ | A(+45.0) B(+9.0) C(-20.0) D(-34.0)\n>>> L1000 | 00:30 | 四般南喰赤－ | D(+85.0) B(+1.0) C(-10.0) E(-74.0)\n>>> """\n>>> from datetime import date\n>>> print(GameResult.parse_str(log_str, date(2020, 8, 15)))\n[\n  GameResult(\n      lobby=\'L1000\',\n      playernum=4,\n      player1=\'A\', player1ptr=45.0, player1shuugi=None, player2=\'B\', player2ptr=9.0, player2shuugi=None,\n      player3=\'C\', player3ptr=-20.0, player3shuugi=None,\n      player4=\'D\', player4ptr=-34.0, player4shuugi=None,\n      starttime=datetime.datetime(2020, 8, 15, 0, 30)),\n  GameResult(\n      lobby=\'L1000\',\n      playernum=4,\n      player1=\'D\', player1ptr=85.0, player1shuugi=None,\n      player2=\'B\', player2ptr=1.0, player2shuugi=None,\n      player3=\'C\', player3ptr=-10.0, player3shuugi=None,\n      player4=\'E\', player4ptr=-74.0, player4shuugi=None,\n      starttime=datetime.datetime(2020, 8, 15, 0, 30))\n]\n```\n\n### nodocchi.moeのAPIからfetch\n\n```py\n>>> results = fetch_player_log("ASAPIN")\n>>> results[:2]\n[\n  GameResult(\n      lobby=None,\n      playernum=4,\n      player1=\'KAZ2000\', player1ptr=50.0, player1shuugi=None, \n      player2=\'ASAPIN\', player2ptr=7.0, player2shuugi=None,\n      player3=\'くに＠けん\', player3ptr=-18.0, player3shuugi=None,\n      player4=\'NoName\', player4ptr=-39.0, player4shuugi=None,\n      starttime=datetime.datetime(2009, 6, 16, 19, 46, tzinfo=datetime.timezone.utc)),\n   GameResult(\n       lobby=None,\n       playernum=4,\n       player1=\'ダイナマイト四国\', player1ptr=58.0, player1shuugi=None,\n       player2=\'ASAPIN\', player2ptr=20.0, player2shuugi=None,\n       player3=\'Del９\', player3ptr=-34.0, player3shuugi=None,\n       player4=\'M*Do\', player4ptr=-44.0, player4shuugi=None, \n       starttime=datetime.datetime(2009, 6, 16, 20, 14, tzinfo=datetime.timezone.utc))\n]\n\n>>> results = fetch_lobby_log("C0000")\n>>> results[:2]\n...\n```\n\n## ResultBook object\n\nResultBookは複数試合の結果を保持している集計用クラスです。\n\n### 例\n\n[第９期天鳳名人戦](https://tenhou.net/cs/2019/08tm/)の結果集計\n\n```py\nfrom tenhoulog import *\nfrom tenhoulog.utils import df2table\n\nresults = fetch_lobby_log("C0011")\nplayers = [\n    "タケオしゃん",\n    "Ⓟ醍醐大",\n    "就活生@川村軍団",\n    "Ⓟ木原浩一",\n    "おかもと",\n    "Ⓢ福地誠",\n    "Ⓟ渋川難波",\n    "Ⓟ小林剛",\n    "独歩",\n    "Ⓟ松ヶ瀬隆弥",\n    "Ⓟ中嶋隼也",\n    "お知らせ",\n]\nbook = ResultBook.from_results(results, players)\nJST = timezone(timedelta(hours=+9), "JST")\nmeijin_book = book.filter_by_period((datetime(2019, 8, 6, tzinfo=JST), datetime(2020, 6, 11, tzinfo=JST)))\nprint(meijin_book.aggregate(4).sort_values("得点", ascending=False))\n```\n\n```sh\n名前  回数     得点         順位分布      平均順位  祝儀\n1       Ⓢ福地誠  40  336.2    12-9-12-7  2.350000   0\n2       Ⓟ醍醐大  40  226.7    11-9-12-8  2.425000   0\n5   就活生@川村軍団  40  195.5   10-11-10-9  2.450000   0\n8       おかもと  40  187.4    11-9-12-8  2.425000   0\n4      Ⓟ木原浩一  36  143.9     11-8-9-8  2.388889   0\n0     Ⓟ松ヶ瀬隆弥  36   97.6     7-13-9-7  2.444444   0\n9       お知らせ  70   91.6  20-17-17-16  2.414286   0\n3     タケオしゃん  39   53.2   10-13-5-11  2.435897   0\n6         独歩  36    2.3     8-14-6-8  2.388889   0\n7      Ⓟ中嶋隼也  24  -45.9      5-6-7-6  2.583333   0\n11     Ⓟ渋川難波  24  -50.6      8-3-5-8  2.541667   0\n10      Ⓟ小林剛  43 -755.9   10-5-11-17  2.813953   0\n```\n',
    'author': 'kitagawa-hr',
    'author_email': 'kitagawahr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kitagawa-hr/tenhoulog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
