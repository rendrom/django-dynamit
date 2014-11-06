run:
	python manage.py runserver 0.0.0.0:8000

shell:
	python manage.py shell

create_database:
	./manage.py syncdb --noinput
	./manage.py migrate --noinput
	./manage.py createsuperuser --username=admin --email=admin@example.com

superuser:
	./manage.py createsuperuser --username=admin --email=admin@example.com


syncdb:
	python manage.py syncdb

mailserver:
	python -m smtpd -n -c DebuggingServer 0.0.0.0:1025

collect:
	python manage.py collectstatic

manage:
	python manage.py $(CMD)

graphviz:
	python manage.py graph_models -a -o logic_models.png -e -g

