d = {
    "stream": "footballusdt@kline_1m",
    "data": {
        "e": "kline",
        "E": 1665585162179,
        "s": "FOOTBALLUSDT",
        "k": {
            "t": 1665585120000,
            "T": 1665585179999,
            "s": "FOOTBALLUSDT",
            "i": "1m",
            "f": 6426372,
            "L": 6426383,
            "o": "865.92000",
            "c": "865.67000",
            "h": "865.92000",
            "l": "865.56000",
            "v": "4.26",
            "n": 12,
            "x": False,
            "q": "3688.3413000",
            "V": "1.73",
            "Q": "1497.9851000",
            "B": "0",
        },
    },
}

data = d["data"]
kline = data["k"]
symbol = kline["s"]

print(symbol)