from lib.Region import Region


def main():
    for region in [Region.EUROPE, Region.ASIA]:
        for retriever in region.retrievers:
            retriever.plot(region=region)


if __name__ == '__main__':
    main()
