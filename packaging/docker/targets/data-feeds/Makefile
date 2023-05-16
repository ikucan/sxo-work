TAG = 0.0.4
PFX = iztokkucan/sxo-data-feeds

build:
	docker build -t $(PFX):$(TAG) .

push: build
	docker push $(PFX):$(TAG)

run:
	docker run --rm $(PFX):$(TAG)
