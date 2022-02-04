# marriage-orga
## organize your marriage
Webapplication to manage someones marriage. Features:
- selfregistration for participants with option to accept or decline participation
- management of presents including reservation of presents by participants
- management of party-contributions like something to eat, helping washing the dishes,...

Localized, you might use different languages.

## Requirements
- python 3.6+
- Database (postgreSQL, MariaDB,...)
- A reverse Proxy (apache2, nginx, ...)
- Access to E-Mail Account

## Tech
- [Django](https://djangoproject.com)
- [Bootstrap Modern Business](https://startbootstrap.com/template/modern-business)
- Fontawesome

## get started
> cp marriage-orga-db-env.sh.template marriage-orga-db-env.sh
> # edit to set the integration credentials
> . env.sh
> # call once to setup python env
> tools/build-pyenv.sh
> cd app && ./run.sh
