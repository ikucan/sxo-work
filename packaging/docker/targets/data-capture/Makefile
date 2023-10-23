TAG = 0.2.1
PFX = iztokkucan/sxo-data-capture

build:
	docker build -t $(PFX):$(TAG) .

push: build
	docker push $(PFX):$(TAG)

run:
	docker run --rm $(PFX):$(TAG)
