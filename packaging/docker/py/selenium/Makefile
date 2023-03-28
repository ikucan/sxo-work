TAG = 0.0.1
PFX = iztokkucan/selenium

build:
	docker build -t $(PFX):$(TAG) .

push: build
	docker push $(PFX):$(TAG)

run:
	docker run --rm $(PFX):$(TAG)
