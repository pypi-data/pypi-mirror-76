from typing import List

import httpx

from .models import APIResponse, GameResult


def fetch_lobby_log(lobby_id: str) -> List[GameResult]:
    """nodocchi.moeから指定したロビーの対戦成績を取得"""
    API_URL = "https://nodocchi.moe/api/lobby.php"
    resp = httpx.post(API_URL, data={"lobby": lobby_id})
    return APIResponse.parse_raw(resp.text).list


def fetch_player_log(player_name: str) -> List[GameResult]:
    """nodocchi.moeから指定したプレイヤーの対戦成績を取得"""
    API_URL = "https://nodocchi.moe/api/listuser.php"
    resp = httpx.post(API_URL, data={"name": player_name})
    return APIResponse.parse_raw(resp.text).list
