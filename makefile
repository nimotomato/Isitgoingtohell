

build_dev:
	docker compose down -v --remove-orphans
	docker compose up -d --build

enter_dev:
	docker exec -ti isitgoingtohell-dev /bin/bash