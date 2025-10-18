from lib.Map import Map


def main():
    # for region in [Map.EUROPE, Map.ASIA]:
    #       region.to_reddit()

    # Map.EUROPE.to_reddit()
    # Map.ASIA.to_reddit()
    # Map.AMERICAS.to_reddit()
    # Map.OCEANIA.to_reddit()
    # Map.AFRICA.to_reddit()
    for region in [Map.EUROPE, Map.ASIA, Map.AMERICAS, Map.OCEANIA, Map.AFRICA]:
        region.to_reddit()


if __name__ == '__main__':
    main()
