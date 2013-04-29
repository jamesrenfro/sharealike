Share-alike
=========

Share pictures with everybody! 

This project is a technical exercise that uses Python Django on the server-side along with several current Javascript frameworks on the client, including Backbone.js, Handlebars.js, Requirejs, and Twitter Bootstrap. The high-level goal is to take advantage of Django's server-side templating and relational ORM, while building modular, testable Javascript on the frontend that can be easily optimized and minified for production deployment. By using Requirejs and Backbone together it's possible to develop self-contained units of code, following the Java pattern where each class has its own separate file, without (at least post-optimization) incurring the cost of all those additional roundtrips to the server. Following the lead of projects like Bootstrap and Angular, it's clearly possible to eliminate a lot of the tight-coupling between Javascript and a particular HTML layout. In this case, I try to do that by building Backbone Views that can be pointed at a particular element at runtime, and avoiding too much direct jQuery DOM manipulation based on ids. 

## Goals

1. To take advantage of Django's capabilities on the server-side to do object relational mapping 
2. To take advantage of Django's templating to allow initial screens to load quickly without additional round-trips
3. To cleanly decouple client-side code so it can be tested independently
4. To use Backbone.js and Require.js to build modular, maintainable MV* user interface
5. To use Bootstrap to produce clean HTML5 with data attributes that avoid unnecessary explicit Javascript wiring
6. To make all communication with the server after the page load use REST/json api calls 

## Quick start

This will start the app using a sqlite database under the top-level project directory, and store
uploaded files under a local directory called 'media/shareserver'. Note that you will need to have a few dependencies 
installed already to get started, including vitualenv and bower, which is easiest to install with the node package manager npm.

	> git clone https://github.com/jamesrenfro/poochable.git
	> virtualenv sharealike
	> cd sharealike
	> source bin/activate
	> bower install
	> pip install -r requirements
	> python manage.py syncdb
	> python manage.py migrate
	> python manage.py runserver  


You may want to add your own settings, start up using Celery, use Postgres as your database, etc. Look under the following directory for the relevant files:

	> cd sharealike/shareproject/settings

## Testing the server-side

	> python manage.py test shareserver
	
	
## Testing the client/browser

To test the client-side code you'll need to install testem

	> npm install -g testem
	
Then do the following

	> cd sharealike/shareproject/assets
	> testem
	
You'll be prompted to go to a URL with each browser that you want to test. 


## Configuring to use S3 and CloudFront to store and distribute images

In settings/development.py or settings/production.py, in addition to setting up your database connection parameters, you can also provide AWS credentials. If you don't already have an existing S3 bucket and CloudFront distribution for this purpose, you'll need to log in to the [AWS Management console](https://console.aws.amazon.com) and create one of each.

## Configuring to use Celery as a distributed task queue

You'll need to add the setting USE_CELERY=True to one of your settings files. You may also want to configure the BROKER_URL for a non-guest user, though it's easier to start up as guest initially. To run celery as a daemon process you'll want to follow these directions: [http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html](http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html) It may be tricky to get the file permissions right if you run celeryd talking to a sqlite3 db, but if you use postgres (or mysql, etc...) you shouldn't have any problems. With sqlite3, you should be able to run celery workers at the command line using the following command:
- python manage.py celery worker --loglevel=info

## Troubleshooting pillow/PIL installation

Doesn't seem to be straightforward to install pillow on all environments. On
my local development environment it turned out to be easiest to just use
apt-get to install, but on EC2 ubuntu was able to get it working using
virtualenv with the following help from stackoverflow.com:
	
[http://stackoverflow.com/questions/4632261/pil-jpeg-library-help](http://stackoverflow.com/questions/4632261/pil-jpeg-library-help)


## Project structure acknowledgements

Project structure is mostly inherited from https://github.com/rdegges/django-skel and https://github.com/integricho/django-skel-modular-js-example  
thanks to https://github.com/rdegges and https://github.com/integricho 

This is worth reading: http://integricho.github.io/2013/04/10/django-and-modular-js/



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

