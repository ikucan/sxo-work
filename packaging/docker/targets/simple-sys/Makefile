TAG = 0.2.0
DATA_FEED_PFX = iztokkucan/simple-strat-data-feed
STRATEGY_PFX = iztokkucan/simple-strat-impl

build-df:
	echo -----
	echo building $(DATA_FEED_PFX):$(TAG)
	echo -----
	docker build -t $(DATA_FEED_PFX):$(TAG) -f Dockerfile-DataFeed.df .

build-strat:
	echo -----
	echo building $(STRATEGY_PFX):$(TAG)
	echo -----
	docker build -t $(STRATEGY_PFX):$(TAG) -f Dockerfile-StratImpl.df .


push-df: build-df
	echo -----
	echo pushing $(DATA_FEED_PFX):$(TAG)
	echo -----
	docker push $(DATA_FEED_PFX):$(TAG)

run-df:
	echo -----
	echo running $(DATA_FEED_PFX):$(TAG)
	echo -----
	docker run --rm $(DATA_FEED_PFX):$(TAG)


build: build-df build-strat
	echo -----
	echo done building
	echo -----
