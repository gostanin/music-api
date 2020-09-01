# Music API project

#### Author: Grigory Ostanin

## Installation


Application served on _localhost:8000/api/v1/_

​	Docker:

​		Run `make docker_up`

​		Tests `make docker_test`

​		Stop `make docker_stop`

​		Tear down container `make docker_down`

​	Regular installation:

​		Virtual environment `python -m venv .venv`

​		Start venv `source .venv/bin/activate`

​		Dependencies `pip3 install -r requirements.txt`

​		Tests run `pytest`

​		Run `python app.py`



## Design decisions

### Docker and makefile:

I have used docker simply to make sure that my project can be run and tested effortless. Makefile makes running some repetitive docker operations more convenient.

 

### Back-end:
  
- #### API:

  - I have controllers and model for API service. Controllers include logic how to handle requests. Model controls data processing part. I have used a factory pattern for application creation, model object. That provides a better control and decoupling between different parts of application. It provides less changes to a code abstracting out a logic how to create object to control data for controllers and makes code cleaner.
  - I have made a dummy function to return a chunk of music data. I have not make it a binary and did not handle binary data. I did not have time to figure it out properly. So 'from' and 'to' parameters are dummy parameters, because the best way would be to use Range header which I did not accoplished. On the side of a binary file flask has send_file function if it's possible to send file in its enternity. I have simplified this due to the time limit.



