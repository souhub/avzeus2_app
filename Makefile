docker-compose-prod:
	docker build -f services/dmm/Dockerfile -t hryk-production-dmm . && \
	docker compose -f docker-compose.prod.yml up
