import re
from dataclasses import dataclass
from datetime import datetime, tzinfo, date
from typing import Any, Dict, List, Set, Tuple, Optional

import japanize_matplotlib  # noqa
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from pydantic import BaseModel


class GameResult(BaseModel):
    """1試合の結果

    nodocchi.moeのAPI形式に準拠
    """

    lobby: str  # 個室ID
    playernum: int  # 対戦人数(3 or 4)
    player1: str  # 1位のプレイヤーの名前
    player1ptr: float  # 1位のプレイヤーの得点
    player1shuugi: Optional[int]  # 1位のプレイヤーの祝儀
    player2: str
    player2ptr: float
    player2shuugi: Optional[int]
    player3: str
    player3ptr: float
    player3shuugi: Optional[int]
    player4: Optional[str]
    player4ptr: Optional[float]
    player4shuugi: Optional[int]
    starttime: datetime  # 開始時刻

    def to_records(self) -> List["Record"]:
        rank_to_attrs = [(rank, f"player{rank}") for rank in range(1, self.playernum + 1)]
        return [
            Record(
                player_name=getattr(self, attr),
                point=getattr(self, attr + "ptr"),
                tip=getattr(self, attr + "shuugi"),
                rank=rank,
            )
            for (rank, attr) in rank_to_attrs
        ]

    @classmethod
    def from_str(cls, log_oneline: str, date: date) -> "GameResult":
        """天鳳公式の文字列形式の1行分をパース

        文字列形式の例:
            L1000 | 00:30 | 四般南喰赤－ | A(+45.0) B(+9.0) C(-20.0) D(-34.0)
            C1000 | 00:50 | 三般南喰赤祝 | A(+64.0,+3枚) B(-8.0,-1枚) C(-56.0,-2枚)
        """
        data: Dict[str, Any] = {}
        lobby_id, starttime, rule, records_str = log_oneline.split("|")
        data["lobby"] = lobby_id.strip()
        h, m = starttime.split(":")
        data["starttime"] = datetime(date.year, date.month, date.day, int(h), int(m))
        if rule.strip().startswith("四"):
            data["playernum"] = 4
        else:
            data["playernum"] = 3
        records = Record.parse_str(records_str.strip())
        for record in records:
            data[f"player{record.rank}"] = record.player_name
            data[f"player{record.rank}ptr"] = record.point
            data[f"player{record.rank}shuugi"] = record.tip
        return cls(**data)

    @classmethod
    def parse_str(cls, log_str: str, date: date) -> List["GameResult"]:
        """天鳳公式の文字列形式の複数行をパース"""
        return [cls.from_str(log_oneline, date) for log_oneline in log_str.split("\n") if log_oneline]

    def player_names(self) -> List[str]:
        return [getattr(self, f"player{i}") for i in range(1, self.playernum + 1)]


class APIResponse(BaseModel):
    """nodocchi.moeのAPIレスポンス"""

    earliest: datetime  # 最も古い対戦の開戦時刻(UTC)
    lobby: str  # 個室ID
    list: List[GameResult]


class Record(BaseModel):
    """プレイヤーの1試合分の成績"""

    player_name: str  # 名前
    point: float  # 得点
    tip: Optional[int]  # 祝儀
    rank: int  # 順位

    @staticmethod
    def _parse_record_str(record_str: str) -> Dict[str, Any]:
        """
        Examples:
            >>> parse_record_str("A(+45.0)")
            {"name": "A", "point": 45.0, "tip": None}
            >>> parse_record_str("A(+45.0,+3枚)")
            {"name": "A", "point": 45.0, "tip": 3}
        """
        regex = re.compile(r"(?P<name>[^\s\(\)]+)\((?P<scores>[\d\+\-\.,]+).*\)")
        m = regex.match(record_str)
        if m is None:
            raise ValueError(f"Invalid record_str format: {record_str}")
        score, *tail = m["scores"].split(",")
        tip = int(tail[0]) if tail else None
        return {"name": m["name"], "point": float(score), "tip": tip}

    @classmethod
    def parse_str(cls, records_str: str) -> List["Record"]:
        """天鳳公式の文字列形式をパース
        Examples:
            >>> from_str("A(+45.0) B(+9.0) C(-20.0) D(-34.0)")
            [
                Record("A", 45.0, None, 1),
                Record("B", 9.0, None, 2),
                Record("C", -20.0, None, 3),
                Record("D", -40.0, None, 4)
            ]
            >>> from_str("A(+64.0,+3枚) B(-8.0,-1枚) C(-56.0,-2枚)")
            [Record("A", 64.0, 3, 1), Record("B", -8.0, -1, 2), Record("C", -56.0, -2, 3)]
        """
        ds = sorted(
            [cls._parse_record_str(record_str) for record_str in records_str.split(" ")], key=lambda x: -x["point"]
        )
        return [Record(player_name=d["name"], point=d["point"], tip=d["tip"], rank=i + 1) for (i, d) in enumerate(ds)]


@dataclass
class ResultBook:
    """複数試合の結果をまとめた帳簿"""

    scores: pd.DataFrame  # 得点
    ranks: pd.DataFrame  # 順位
    tips: pd.DataFrame  # 祝儀

    @property
    def player_names(self) -> Set[str]:
        return set(self.scores.columns) - {"starttime"}

    def __add__(self, other: "ResultBook") -> "ResultBook":
        """他のBookとの結合"""
        columns = self.player_names.union(other.player_names).union({"starttime"})
        base_df = pd.DataFrame([], columns=columns)
        return ResultBook(
            pd.concat([base_df, self.scores, other.scores]),
            pd.concat([base_df, self.ranks, other.ranks]),
            pd.concat([base_df, self.tips, other.tips]),
        )

    @classmethod
    def _filter_df_by_period(cls, df: pd.DataFrame, time_period: Tuple[datetime, datetime]) -> pd.DataFrame:
        return df[(time_period[0] <= df["starttime"]) & (df["starttime"] < time_period[1])]

    def filter_by_period(self, time_period: Tuple[datetime, datetime]) -> "ResultBook":
        """指定した期間内の結果にフィルタする"""
        return ResultBook(
            self._filter_df_by_period(self.scores, time_period),
            self._filter_df_by_period(self.ranks, time_period),
            self._filter_df_by_period(self.tips, time_period),
        )

    def aggregate(self, player_num: int) -> pd.DataFrame:
        """集計を行う"""
        rows = []
        for player in self.player_names:
            score_sum = self.scores[player].sum()
            times = self.scores[player].notnull().sum()
            rank_counts = self.ranks[player].value_counts().to_dict()
            ranks = [rank_counts.get(rank, 0) for rank in range(1, player_num + 1)]
            rank_avg = self.ranks[player].mean()
            tip = int(self.tips[player].sum())
            rows.append([player, times, score_sum, "-".join(map(str, ranks)), rank_avg, tip])
        return pd.DataFrame(rows, columns=["名前", "回数", "得点", "順位分布", "平均順位", "祝儀"])

    def plot_cumsum(self, attr: str = "scores") -> Figure:
        """得点または祝儀の推移を可視化

        Args:
            - attr (str): ``scores`` or ``tips``を選択. Default to ``scores``.
        """
        target_df: pd.DataFrame = getattr(self, attr)
        fig, ax = plt.subplots()
        shifted_cumsum = target_df[self.player_names].apply(lambda x: pd.Series(x.dropna().values)).cumsum()
        shifted_cumsum.plot(ax=ax)
        ax.set_title("得点推移")
        ax.legend(loc="upper left")
        return fig

    @classmethod
    def from_results(cls, results: List["GameResult"], player_names: List[str], tz: tzinfo) -> "ResultBook":
        """試合結果をDataFrameに変換

        player_namesで指定したプレイヤーの結果だけが対象
        (scoreを表すdf, rankを表すdf)を返す
        """
        scores = []
        ranks = []
        tips = []
        columns = player_names + ["starttime"]
        for result in results:
            starttime = result.starttime.astimezone(tz)
            records = result.to_records()
            score = dict({record.player_name: record.point for record in records}, starttime=starttime)
            rank = dict({record.player_name: record.rank for record in records}, starttime=starttime)
            tip = dict({record.player_name: record.tip for record in records}, starttime=starttime)
            scores.append(score)
            ranks.append(rank)
            tips.append(tip)
        return ResultBook(
            pd.DataFrame(scores, columns=columns),
            pd.DataFrame(ranks, columns=columns),
            pd.DataFrame(tips, columns=columns),
        )
