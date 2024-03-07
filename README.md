https://github.com/docker-library/docs/blob/master/postgres/README.md
docker run -p 80:80 -e 'PGADMIN_DEFAULT_EMAIL=user@domain.com' -e 'PGADMIN_DEFAULT_PASSWORD=mysecretpassword' -d dpage/pgadmin4

use ssl:
https://stackoverflow.com/questions/29458548/can-you-add-https-functionality-to-a-python-flask-web-server
https://kracekumar.com/post/54437887454/ssl-for-flask-local-development/

pip install sqlacodegen_v2
sqlacodegen_v2 --schemas contract_report --outfile contract_report_model.py postgresql+psycopg://postgres:mysecretpassword@localhost:5432/contract_report
