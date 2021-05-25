from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.response import Response
import json
import mysql.connector as mysql
import os

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

def welcome(req):
  # Connect to the database and retrieve the users
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select first_name, last_name, email, comment from Users;")
  records = cursor.fetchall()
  db.close()

  return render_to_response('templates/welcome.html', {'users': records}, request=req)

def get_home(req):
  return render_to_response('templates/home.html', [], request=req)

def get_about(req):
  return render_to_response('templates/about.html', [], request=req)

def get_cv(req):
  return render_to_response('templates/cv.html', [], request=req)

def add_user(req):
  new_user = json.loads(req.text)
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  insert_stmt = "INSERT INTO Commands (first_name, last_name, email, comment) VALUES (%s, %s, %s, %s)"
  print('NEW USER: ', new_user)
  data = (new_user, 0)
  cursor.execute(insert_stmt, data)
  print('-----INSERT-----')
  print(cursor.rowcount, "record inserted.")
  print('-----ALL ROWS-----')
  cursor.execute("SELECT * FROM Commands")

def get_avatar(req, req1):
  return { 
    "image_src":"assets/avatar.JPG"
  }

def get_personal(req, req1):
  return {
    "first_name": "Muhammad Adib Thaqif",
    "last_name": "Taufek",
    "email": "mtaufek@ucsd.edu"
  }
def get_education(req, req1):
  return {
    "school": "UC San Diego",
    "degree": "Bachelor of Science",
    "major": "Computer Engineering",
    "date": "2022"
  }

def get_project(req, req1):
  return {
    "title": "EZ Trader",
    "description": "Educational Investment Web Application for New Investors",
    "link": "ez-trader.com",
    "image_src": "assets/ez-trader-logo.png",
    "team": {
    "api_link": {
      "Hector": "165.232.152.55", 
      "Michael": "143.110.229.54",
      "Tanvir": "128.199.10.10",
      }
    }
  }


if __name__ == '__main__':
  config = Configurator()

  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')

  config.add_route('get_home', '/')
  config.add_view(get_home, route_name='get_home')

  config.add_route('get_cv', '/cv')
  config.add_view(get_cv, route_name='get_cv')

  config.add_route('welcome', '/welcome')
  config.add_view(welcome, route_name='welcome')

  config.add_route('about', '/about')
  config.add_view(get_about, route_name='about')

  config.add_route('add_user', '/add_user')
  config.add_view(add_user, route_name='add_user')

  config.add_route('avatar', '/avatar')
  config.add_view(get_avatar, route_name='avatar', renderer='json')

  config.add_route('personal', '/personal')
  config.add_view(get_personal, route_name='personal', renderer='json')

  config.add_route('education', '/education')
  config.add_view(get_education, route_name='education', renderer='json')

  config.add_route('project', '/project')
  config.add_view(get_project, route_name='project', renderer='json')

  config.add_static_view(name='/', path='./public', cache_max_age=3600)

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()