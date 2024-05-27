import requests


data = {
    "steps" : [
        {
            "content": "Please print this line."
        },
                {
            "content": "Also print this one."
        }
    ]
}

requests.post("http://dalbypi:8000/api/job", json=data)
# requests.post("http://localhost:8000/api/job", json=data)