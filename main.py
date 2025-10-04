from lib.Region import Region


def all():
    regions = [Region.EUROPE, Region.ASIA]
    for region in regions:
        for retriever in region.retrievers:
            retriever.plot(region=region)


if __name__ == '__main__':
    all()
