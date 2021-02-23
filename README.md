# Hello!
##This is my test project.

Load config data:
`python manage.py loaddata settings.json `

Documentation for API available:
`http://127.0.0.1:8000/swagger/`

Registration:
`http://127.0.0.1:8000/api/v1/auth/users/`

Get token:
`http://127.0.0.1:8000/api/v1/auth/jwt/create`

Get list photos:
`http://127.0.0.1:8000/api/v1/list/`

Upload photo:
`http://127.0.0.1:8000/api/v1/photo/`

Get the photo:
`http://127.0.0.1:8000/api/v1/photo/<photo id>/`

Update name photo:
`http://127.0.0.1:8000/api/v1/photo/<photo id>/`

##Celery
Start worker:
`celery -A photobook worker -l INFO`

##Sending e-mail
For sending email every day add to cron next task:
`0 9 * * * python /path/to/wor/dir/manage.py send_email_daily`

For sending email every month add to cron next task:
`0 9 1 * * python /path/to/wor/dir/manage.py send_email_daily`