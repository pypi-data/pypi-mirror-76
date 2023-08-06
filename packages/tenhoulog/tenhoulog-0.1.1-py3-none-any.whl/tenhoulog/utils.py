from collections import defaultdict
from datetime import datetime, tzinfo
from typing import TYPE_CHECKING, List
from decimal import Decimal, getcontext, ROUND_CEILING
import numpy as np
import pandas as pd
from beautifultable import BeautifulTable

if TYPE_CHECKING:
    from .models import GameResult # noqa


def start_of_today(tz: tzinfo) -> datetime:
    """指定したtimezoneにおける, 当日の00:00を表すdatetime"""
    now = datetime.now(tz=tz)
    return datetime(year=now.year, month=now.month, day=now.day, hour=0, second=0, tzinfo=tz)


def df2table(df: pd.DataFrame) -> BeautifulTable:
    """データフレームを可読性の高いテーブルに変換"""
    table = BeautifulTable()
    table.columns.header = df.columns
    for row in df.values:
        table.rows.append(row)
    return table


def calc_rate(results: List["GameResult"]):
    """レート計算

    - 初期値=R1500
    - 卓の平均Rが高いほど大きく上昇します

    (Rateの変動) = (試合数補正) x ( 対戦結果 + 補正値 ) x (スケーリング係数)
    試合数補正(400試合未満): 1 - 試合数 x 0.002
    試合数補正(400試合以上): 0.2
    対戦結果(段位戦4人打ち): 1位+30 2位+10 3位-10 4位-30
    対戦結果(段位戦3人打ち): 1位+30 2位0 3位-30
    対戦結果(雀荘戦): 得点 + 祝儀(得点換算)
    補正値: ( 卓の平均R - 自分のR ) / 40
    スケーリング係数(段位戦):1.0
    スケーリング係数(雀荘戦):(調整中)

    ※2009/09/09 Rate計算後小数第３位以下を切り上げ
    ※2010/02/01 卓の平均Rが1500未満の場合は1500に切り上げ
    ※2010/10/14 雀荘戦に収支制のRatingを導入
    """

    def times_correct(times: int) -> Decimal:
        if times < 400:
            Decimal(1 - times * 0.002)
        return Decimal(0.2)

    getcontext().prec = 7
    getcontext().rounding = ROUND_CEILING
    SCALLING_COEFF = Decimal(1.0)
    deltas = {3: (30, 0, -30), 4: (30, 10, -10, -30)}
    rates = defaultdict(lambda: {"rate": Decimal(1500), "times": 0})
    for result in results:
        avg_rate = max(Decimal(1500), np.mean([rates[name]["rate"] for name in result.player_names()]))
        for name, delta in zip(result.player_names(), deltas[result.playernum]):
            corr_val = (avg_rate - rates[name]["rate"]) / Decimal(40)
            rates[name]["rate"] += times_correct(rates[name]["times"]) * (delta + corr_val) * SCALLING_COEFF
            rates[name]["times"] += 1
    return rates
