import requests


data = {
    "steps" : [
        { "content" : "This is a test."}
    ]
}

requests.post("http://dalbypi:8000/api/job", json=data)