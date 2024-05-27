import requests


data = {
    "steps" : [
        {
            
        }
    ]
}

# requests.post("http://dalbypi:8000/api/job", json=data)
requests.post("http://localhost:8000/api/job", json=data)