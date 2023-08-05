# Eve Simple ESI

The Python 3+ library for simple and **fast** work with https://esi.evetech.net data.

`Thanks Qandra-Si ( https://github.com/Qandra-Si ) for help and basis of implementation`

## This library can:

- locally autorize with eve-online user (with gui and without gui interfase)
- automatically refresh autorization without gui
- get data (include data require autorization)
- post data (include data require autorization)

## install:

### pypi:
```
pip install eve-simple-esi
```

### manual:
Just put eve_simple_esi.py to directory with your project

## how to use:

- **initialization**:
	```python
	import eve_simple_esi as esi

	settings={
		'client_id':"<Client ID>", # go to https://developers.eveonline.com/ create app and get Client ID
		'client_secret':"<Secret Key>", # go to https://developers.eveonline.com/ create app and get Secret Key
		'client_callback_url':"<Callback URL>", # default http://localhost:8635/ need to be same as in your app in https://developers.eveonline.com/
		'user_agent':"<User Agent string>",
		'scopes':<list of scopes>, # ['publicData','esi-location.read_location.v1',...etc.]
		'port':<port for local web server for authorization>, # default 8635
	}

	ESI=esi.ESI(settings)
	```
	
- **get data**:
	```python
	data=ESI.op('/characters/{character_id}/',params={'character_id':2117005244})
	```
	
- **post data**:
	```python
	data=ESI.op('/ui/autopilot/waypoint/',params={'add_to_beginning':False, 'clear_other_waypoints':False, 'destination_id':30000142}, post=True)
	```
	
- **post data with body**:
	```python
	data=ESI.op('/universe/ids/',body=json.dumps(["Gila","Thrasher","Jita","CCP Alpha"]))
	```

- gui autorization:
	```python
	ESI.gui_auth()
	```
	The builtin webserver starts only when needed for authorization and automatically shutdown when no authorization jobs found
	
- cli autorization:
	```python
	ESI.auth() #need to go by url and after autorization insert code from url (http://localhost:8635/?code=<requested_code>&state=...)
	```
	
- change character for request (if they storred):
	```python
	ESI.get("EVE Character Name") # if character never autorized in your program - ESI.gui_auth() or ESI.auth() calls automatically for login
	```
	
- get character in initialize:
	```python
	ESI=esi.ESI(settings,name="EVE Character Name")
	```
	
- force cli autorization if no storred character:
	```python
	ESI=esi.ESI(settings,name="EVE Character Name", gui=False)
	```
	
- use multiplue instance:
	```python
	import eve_simple_esi as esi
	
	web_server=esi.ESIAuthWebServer(local_address='localhost', port=8635) # make one instance of webserver for all ESI instances
	
	ESI1=esi.ESI(settings, name="first EVE Character Name", callback_web_server=web_server)
	ESI2=esi.ESI(settings, callback_web_server=web_server)
	ESI3=esi.ESI(settings, callback_web_server=web_server)
	ESI3.gui_auth()
	```

- fash user switch:
	```python
	import eve_simple_esi as esi
	
	ESI=esi.ESI(settings, name="first EVE Character Name")
	data=ESI.op('/characters/{character_id}/')
	ESI.get("second EVE Character Name")
	data=ESI.op('/characters/{character_id}/')
	data=ESI.op('/ui/autopilot/waypoint/',params={'add_to_beginning':False, 'clear_other_waypoints':False, 'destination_id':30000142}, post=True)
	ESI.get("third EVE Character Name")
	data=ESI.op('/characters/{character_id}/')
	```
	
- autoapply self character information if autorized:
	```python
	ESI=esi.ESI(settings,name="EVE Character Name")
	data=ESI.op('/characters/{character_id}/') # data for character_id with "EVE Character Name" name
	data=ESI.op('/characters/{character_id}/',params={'character_id':2117005244}) # data for character_id: 2117005244
	```
	
- you also can use your own function to get all messages from ESI class:
	```python
	def my_print_function(text_string):
		...
		print(text_string) # as example
		...
		
	ESI=esi.ESI(settings,callback_print=my_print_function)
	```
	
- and your own function for request auth_code:
	```python
	def my_input_function(text_string):
		...
		return input(text_string) # as example
		
	ESI=esi.ESI(settings,callback_input=my_input_function)
	```
	
- and your own class for store user data:
	```python
	class custom_callback_saved_data:
		def read(char_name):
			...
			return json.loads(saved_data)

		def write(char_name,data):
			saved_data=json.dumps(data)
			...
		
	ESI=esi.ESI(settings,callback_saved_data=custom_callback_saved_data)
	```
	
- and your own webserver class:
	```python
	class custom_callback_web_server(address, port):
		def reg_callback(state_string, on_success_function, on_error_function):
			...
		...
	ESI=esi.ESI(settings,callback_web_server=custom_callback_web_server)
	```
