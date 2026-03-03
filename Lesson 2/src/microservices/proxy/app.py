from fastapi import FastAPI
from fastapi import Request, Response
import requests
import re
from urllib.parse import urlparse


app = FastAPI()

BAD_HEADERS = ['Content-Encoding', 'Transfer-Encoding', 'content-encoding',
               'transfer-encoding', 'content-length', 'Content-Length']


async def _proxy(request: Request):
    # Changing url domain
    if (re.search('movies',(str(request.url)))):
        HOSTNAME = 'movies-service:8081'
    elif (re.search('users',(str(request.url)))):
        HOSTNAME = 'monolith:8080'
    else:
        HOSTNAME = 'proxy-service:8000'
    components = urlparse(str(request.url))
    components = components._replace(netloc=HOSTNAME)._replace(scheme='http')

    # Changing headers
    headers = {k: v for k, v in request.headers.items()}
    headers['host'] = HOSTNAME

    body = await request.body()

    # Sending request
    r = requests.request(request.method, components.geturl(), data=body, headers=headers, cookies=request.cookies)

    # Fixing headers and cookies
    bad_keys = set(map(str.lower, BAD_HEADERS))
    headers = {k: v for k, v in r.headers.items() if k.lower() not in bad_keys}
    response = Response(content=r.content, status_code=r.status_code, headers=headers)
    for k, v in r.cookies.items():
        response.set_cookie(k, v)
    return response

@app.get("/health")
def read_root():
    return {"status":"OK"}

@app.api_route("/{full_path:path}", methods=['GET', 'POST', 'DELETE', 'PUT', 'HEAD'])
async def root(request: Request):
    return await _proxy(request)
