import os
import shutil
import info

def start(projectname, path='.'):
	os.mkdir(projectname)
	os.chdir(projectname)
	os.mkdir('HTML')
	os.mkdir('static')
	os.mkdir('cache')

	with open('main.py', 'wb') as f:
		f.write(info.main.encode())

	with open('handle.py', 'wb') as f:
		f.write(info.handle.encode())

	with open('urls.py', 'wb') as f:
		f.write(info.urls.encode())

	with open('db.sqlite3', 'wb') as f:
		pass

	os.chdir('cache')
	with open('httpResponses.py', 'wb') as f:
		f.write(info.httpResponses.encode())

	with open('handle.py', 'wb') as f:
		f.write(info.handle.encode())

	with open('exceptionHandling.py', 'wb') as f:
		f.write(info.exception.encode())

	print('Project setup finished')

