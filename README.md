# seminar-manager

Pre-requisite:
    1. mysql server-5.7.10
    2. python 3.7

Step-by-step process: 
    1. Create a DB schema as 'root_proj' 
        -you can name it as you want, change name for DATABASES in settings.py
    2. Create a directory and extract code in directory.
    3. Create a virtual env inside it. (command: python -m venv venv)
    4. Activate the virtual env  (command: source venv/bin/activate)
    5. Install the /root_proj/requirements.txt (command: pip install -r /root_proj/requirements.txt)
    6. Change directory to /root_proj/ and run the server. (command python manage.py runserver)

server will be running on your localhost:8000


API-Documentations:

API-1 : localhost:8000/halls - To get available seminar halls : 
        requeset-Method : GET
        requeset-JSON : {
                            "capacity": 10,
                            "date": "2021-03-15",
                            "start_time" : "10:00",
                            "end_time" : "10:30"
                        }
        
        response-JSON : {
                            "message": [
                                "F",
                                "D",
                                "E",
                                "C"
                            ]
                        }

        Error-Resonse:  {
                            "error": "missing capacity in request body."
                        }

API-2 : localhost:8000/book_hall - To book an available seminar halls : 
        requeset-Method : POST
        requeset-JSON : {
                            "hall_id": "B",
                            "date": "2021-03-16",
                            "start_time" : "11:00",
                            "end_time" : "13:30"
                        }
        
        response-JSON : {
                            "message": "Seminar Hall Booked."
                        }

        Error-Resonse:  {
                            "error": "Seminar hall already occupied for requested timings."
                        }

API-3 : localhost:8000/seminars - To get list of all seminars for given date range : 
        requeset-Method : GET
        requeset-JSON : {
                            "start_date" : "2021-03-15",
                            "end_date" : "2021-03-16"
                        }
        
        response-JSON : {
                            "message": [
                                {
                                    "hall": "A",
                                    "start_time": "09:00:00",
                                    "end_time": "10:00:00"
                                },
                                {
                                    "hall": "A",
                                    "start_time": "11:00:00",
                                    "end_time": "01:00:00"
                                },
                                {
                                    "hall": "A",
                                    "start_time": "12:00:00",
                                    "end_time": "13:30:00"
                                }
                            ]
                        }
    
    Error-Resonse:      {
                            "message": "No seminar found for requested date range."
                        }