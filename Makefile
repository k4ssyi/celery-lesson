# 開発環境用コマンド
ALL: run
build:
	docker-compose build
up:
	docker-compose up
stop:
	docker-compose stop
down:
	docker-compose down
shell:
	docker-compose exec app /bin/bash
