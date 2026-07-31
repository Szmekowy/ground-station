RULES = {
    "temperature": {"types": (int, float), "min": -90, "max": 60},
    "pressure": {"types": (int, float), "min": 0},
    "position": {
        "x": {"types": (int, float)},
        "y": {"types": (int, float)},
        "z": {"types": (int, float), "min": 0}
    }
}
