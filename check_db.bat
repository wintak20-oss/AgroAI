@echo off
docker exec -it agro-postgres psql -U postgres -d agro_health
