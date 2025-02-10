class DataNotFound(Exception):
    def __init__(self, asset: str, url: str) -> None:
        self.msg = f"No data found for ticker '{asset}' [URL: {url}]"
