
game_rule = {
    "Mankara Basic": "".join(
        [
            "自分のポケットの石が先に無くなったほうが勝ち。",
            "自分、相手のゴールにも石を配る。",
            "自分、相手のゴールで石を配り終えた場合には、",
            "もう一度石を配ることができる。",
        ]
    ),
    "Mankara Easy": "".join(
        [
            "自分か相手のどちらかのポケットの石が無くなったらゲーム終了。",
            "ゲーム終了時点でゴールにある石の数が多いほうが勝ち。",
            "ゲーム終了時点でポケットに残された石はカウントしない。",
            "相手のゴールには石を配らない。",
            "自分のゴールで石を配り終えた場合には、",
            "もう一度石を配ることができる。",
        ]
    ),
    "Karaha": "".join(
        [
            "自分か相手のどちらかのポケットの石が無くなったらゲーム終了。",
            "ゲーム終了時点でポケットに残された石は、それぞれゴールに移動させる。",
            "ゲーム終了時点でゴールにある石の数が多いほうが勝ち。",
            "相手のゴールには石を配らない。",
            "自分のゴールで石を配り終えた場合には、",
            "もう一度石を配ることができる。",
        ]
    ),
    "Sunka": "".join(
        [
            "自分か相手のどちらかのポケットの石が無くなったらゲーム終了。",
            "ゲーム終了時点でポケットに残された石は、それぞれゴールに移動させる。",
            "ゲーム終了時点でゴールにある石の数が多いほうが勝ち。",
            "相手のゴールには石を配らない。",
            "自分のゴールで石を配り終えた場合には、",
            "もう一度石を配ることができる。",
            "自分の空の状態だったポケットで石を配り終えた場合、",
            "そのポケットおよび向かい側のポケットの双方に石があるときに、",
            "その双方の石を自分のゴールに移動させる。",
        ]
    ),
    "Owari": "".join(
        [
            "自分、相手のゴールには石を配らない。",
            "相手のポケットで石を配り終えたとき、そのポケットに石が2か3個だった場合、",
            "自分のゴールにそのポケットの石を移動。",
            "さらにその向かいの自分のポケットに石が2か3個だった場合、",
            "自分のゴールにそのポケットの石を移動。",
            "ゲーム終了時点でゴールにある石の数が多いほうが勝ち。",
            "相手のターンで石が配れない状態を作ってはいけない。",
            "どうやっても相手ターンで石が配れない状態になってしまったらゲーム終了。",
            "ゲーム終了時点でのゴールにある石の数が多いほうが勝ち",
        ]
    ),
}

POCKET_NUMBER = 7

PEACE_SIZE = 32
