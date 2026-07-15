def getpath():
    from pathlib import PurePath, Path
    import os
    pathp = PurePath(__file__)
    path = os.path.abspath(os.getcwd())
    return pathp


if __name__ == "__main__":
    print(getpath())
