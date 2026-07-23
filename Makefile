.PHONY: up down logs seed shell

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

seed:
	curl "http://localhost:8000/api/logs/generate?n=100&anomaly_ratio=0.15"

shell:
	docker compose exec backend bash