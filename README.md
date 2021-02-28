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
`http://127.0.0.1:8000/api/v1/photos/`

Upload photo:
`http://127.0.0.1:8000/api/v1/photos/photo/create`

Get the photo:
`http://127.0.0.1:8000/api/v1/photos/photo/<photo id>/`

Update name photo:
`http://127.0.0.1:8000/api/v1/photos/photo/<photo id>/`

Delete photo:
`http://127.0.0.1:8000/api/v1/photos/photo/<photo id>/`

##Celery
Start worker:
`celery -A photobook worker -l INFO`

##Flower
Start worker:
`flower -A photobook --port=5555`

##Sending e-mail
For sending email every day add to cron next task:
`0 9 * * * python /path/to/wor/dir/manage.py send_email_daily`

For sending email every month add to cron next task:
`0 9 1 * * python /path/to/wor/dir/manage.py send_email_daily`