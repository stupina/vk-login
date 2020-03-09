# vk-login

App that can log into VK and look for friends by name

## Bringing up

1. Clone this project and go to the directory
```bash
git clone https://github.com/stupina/vk-login.git && cd vk-login
```

2. Add file "env_file" to the our root directory. Add to params to file:
```bash
DB_NAME=db_name
DB_HOST=db_service_name_from_docker_compose_file
DB_PORT=db_external_port_from_docker_compose_file
APP_SECRET_KEY=app_secret_key
FLASK_APP=main.py
ID=app_id
SECRET=private_key
```

3. Bring up the app
```bash
docker-compose up -d
```

4. Browse to [link](http://0.0.0.0:5000) to see the app in action.
