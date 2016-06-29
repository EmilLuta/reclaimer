### Getting your hands dirty ###

* cd to a comfy location
* git clone git@github.com:EmilLuta/reclaimer.git
* sudo npm install -g less
* sudo ln -s /usr/bin/nodejs /usr/bin/node  # in case you get "node: command not found" in bash
* cd reclaimer/
* virtualenv -p $(which python3) venv
* source venv/bin/activate
* pip install -r requirements.txt
* cp config_example.py config.py
* update the config.py file to suit your needs
* ./manage.py db_create
* ./manage.py runserver
* point your browser to [http://localhost:5000/](http://localhost:5000/)
