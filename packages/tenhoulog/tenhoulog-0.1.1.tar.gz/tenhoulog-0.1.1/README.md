# tenhoulog

## インストール

```sh
pip install tenhoulog
```

## GameResult object

GameResultオブジェクトは1試合の結果を保持します。

### 文字列から生成

```py
>>> log_str = """
>>> L1000 | 00:30 | 四般南喰赤－ | A(+45.0) B(+9.0) C(-20.0) D(-34.0)
>>> L1000 | 00:30 | 四般南喰赤－ | D(+85.0) B(+1.0) C(-10.0) E(-74.0)
>>> """
>>> from datetime import date
>>> print(GameResult.parse_str(log_str, date(2020, 8, 15)))
[
  GameResult(
      lobby='L1000',
      playernum=4,
      player1='A', player1ptr=45.0, player1shuugi=None, player2='B', player2ptr=9.0, player2shuugi=None,
      player3='C', player3ptr=-20.0, player3shuugi=None,
      player4='D', player4ptr=-34.0, player4shuugi=None,
      starttime=datetime.datetime(2020, 8, 15, 0, 30)),
  GameResult(
      lobby='L1000',
      playernum=4,
      player1='D', player1ptr=85.0, player1shuugi=None,
      player2='B', player2ptr=1.0, player2shuugi=None,
      player3='C', player3ptr=-10.0, player3shuugi=None,
      player4='E', player4ptr=-74.0, player4shuugi=None,
      starttime=datetime.datetime(2020, 8, 15, 0, 30))
]
```

### nodocchi.moeのAPIからfetch

```py
>>> results = fetch_player_log("ASAPIN")
>>> results[:2]
[
  GameResult(
      lobby=None,
      playernum=4,
      player1='KAZ2000', player1ptr=50.0, player1shuugi=None, 
      player2='ASAPIN', player2ptr=7.0, player2shuugi=None,
      player3='くに＠けん', player3ptr=-18.0, player3shuugi=None,
      player4='NoName', player4ptr=-39.0, player4shuugi=None,
      starttime=datetime.datetime(2009, 6, 16, 19, 46, tzinfo=datetime.timezone.utc)),
   GameResult(
       lobby=None,
       playernum=4,
       player1='ダイナマイト四国', player1ptr=58.0, player1shuugi=None,
       player2='ASAPIN', player2ptr=20.0, player2shuugi=None,
       player3='Del９', player3ptr=-34.0, player3shuugi=None,
       player4='M*Do', player4ptr=-44.0, player4shuugi=None, 
       starttime=datetime.datetime(2009, 6, 16, 20, 14, tzinfo=datetime.timezone.utc))
]

>>> results = fetch_lobby_log("C0000")
>>> results[:2]
...
```

## ResultBook object

ResultBookは複数試合の結果を保持している集計用クラスです。

### 例

[第９期天鳳名人戦](https://tenhou.net/cs/2019/08tm/)の結果集計

```py
from tenhoulog import *
from tenhoulog.utils import df2table

results = fetch_lobby_log("C0011")
players = [
    "タケオしゃん",
    "Ⓟ醍醐大",
    "就活生@川村軍団",
    "Ⓟ木原浩一",
    "おかもと",
    "Ⓢ福地誠",
    "Ⓟ渋川難波",
    "Ⓟ小林剛",
    "独歩",
    "Ⓟ松ヶ瀬隆弥",
    "Ⓟ中嶋隼也",
    "お知らせ",
]
book = ResultBook.from_results(results, players)
JST = timezone(timedelta(hours=+9), "JST")
meijin_book = book.filter_by_period((datetime(2019, 8, 6, tzinfo=JST), datetime(2020, 6, 11, tzinfo=JST)))
print(meijin_book.aggregate(4).sort_values("得点", ascending=False))
```

```sh
名前  回数     得点         順位分布      平均順位  祝儀
1       Ⓢ福地誠  40  336.2    12-9-12-7  2.350000   0
2       Ⓟ醍醐大  40  226.7    11-9-12-8  2.425000   0
5   就活生@川村軍団  40  195.5   10-11-10-9  2.450000   0
8       おかもと  40  187.4    11-9-12-8  2.425000   0
4      Ⓟ木原浩一  36  143.9     11-8-9-8  2.388889   0
0     Ⓟ松ヶ瀬隆弥  36   97.6     7-13-9-7  2.444444   0
9       お知らせ  70   91.6  20-17-17-16  2.414286   0
3     タケオしゃん  39   53.2   10-13-5-11  2.435897   0
6         独歩  36    2.3     8-14-6-8  2.388889   0
7      Ⓟ中嶋隼也  24  -45.9      5-6-7-6  2.583333   0
11     Ⓟ渋川難波  24  -50.6      8-3-5-8  2.541667   0
10      Ⓟ小林剛  43 -755.9   10-5-11-17  2.813953   0
```
