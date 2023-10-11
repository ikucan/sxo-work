TAG = 0.1.0
PFX = iztokkucan/sxo-token-grabber

build:
	docker build -t $(PFX):$(TAG) .

push: build
	docker push $(PFX):$(TAG)

run:
	docker run --rm $(PFX):$(TAG)
