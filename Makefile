dev:
	python main.py --config_file config.dev.json
dev_server:
	cd test && python3 -m http.server --bind 127.0.0.1 10086

logs:
	docker-compose exec app tail -f logs/debug.txt