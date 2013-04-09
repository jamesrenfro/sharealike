Poochable
=========

Share pictures of your dog!

## Quick start

	This will start the app using a sqlite database under the top-level project directory, and store
	uploaded files under a local directory called 'public/media/originals'.

	> git clone https://github.com/jamesrenfro/poochable.git
	> virtualenv poochable
	> cd poochable
	> source bin/activate
	> pip install -r requirements
	> python manage.py syncdb
	> python manage.py runserver  


	You can also do the following, before starting the server, to add your own settings, start up using Celery, use Postgres as your database, etc. 

	Optional Step:
	> cp poochable/local_settings.template poochable/local_settings.py
	> edit local_settings.py as necessary, including AWS credentials, etc.


## Configuring to use S3 and CloudFront to store and distribute images

	In local_settings.py, in addition to setting up your database connection
	parameters, you can also provide AWS credentials. If you don't already have
	an existing S3 bucket and CloudFront distribution for this purpose, you'll
	need to log in to the AWS Management console [https://console.aws.amazon.com]
	and create one of each.

## Configuring to use Celery as a distributed task queue

	You'll need to add the setting USE_CELERY=True to your settings.py (or your
	local_settings.py). You may also want to configure the BROKER_URL for a non-guest
 	user, though it's easier to start up as guest initially. To run celery as a daemon 
	process you'll want to follow these directions: [http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html] 
	It may be tricky to get the file permissions right if you run celeryd talking
	to a sqlite3 db, but if you use postgres (or mysql, etc...) you shouldn't have
	any problems. With sqlite3, you should be able to run celery workers at the command
	line using the following command:
	- python manage.py celery worker --loglevel=info

## Troubleshooting pillow/PIL installation

	Doesn't seem to be straightforward to install pillow on all environments. On
	my local development environment it turned out to be easiest to just use
	apt-get to install, but on EC2 ubuntu was able to get it working using
	virtualenv with the following help from stackoverflow.com:
	
	[http://stackoverflow.com/questions/4632261/pil-jpeg-library-help]


## Authors

**James Renfro**

+ [http://github.com/jamesrenfro](http://github.com/jamesrenfro)

## Copyright and license

Copyright 2013 James Renfro

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this work except in compliance with the License.
You may obtain a copy of the License in the LICENSE file, or at:

  [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

