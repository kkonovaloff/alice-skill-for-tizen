class TVApp:
    def __init__(self, names_: list[str], id_: int) -> None:
        self.names = names_
        self.id = id_


tv_apps = [
    TVApp(["youtube", "ютуб", "ютьуб"], 111299001912),
    TVApp(["twitch", "твич", "твитч", "twich", "tvich", "tvitch"], 3202203026841),
    TVApp(["кинопоиск", "kinopoisk"], 111399000037),
]
