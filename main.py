from lib.Map import Map


def main():
    for region in [Map.EUROPE, Map.ASIA]:
        region.to_reddit()


if __name__ == '__main__':
    main()
