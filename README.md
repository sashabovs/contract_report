https://github.com/docker-library/docs/blob/master/postgres/README.md
docker run -p 80:80 -e 'PGADMIN_DEFAULT_EMAIL=user@domain.com' -e 'PGADMIN_DEFAULT_PASSWORD=mysecretpassword' -d dpage/pgadmin4