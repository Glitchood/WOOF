# WOOF
WOOF - Web Operation &amp; Outlier Firewall

A Smart WAF System.
## Features:
TBD

## Contibribute:

Linux and Mac
```
$ git clone https://github.com/Glitchood/WOOF.git 
$ cd WOOF
$ python -m venv .venv 
$ source .venv/bin/activate
$ pip3 install .
```

## Run backend:
```
$ cd backend && python -m fastapi dev app/main.py
```

## Run frontend:
```
$ cd frontend && pnpm i && pnpm run dev 
```
The frontend should now be hosted at http://localhost:5183

