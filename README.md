# WOOF
WOOF - Web Operation &amp; Outlier Firewall

A Smart WAF System.
## Features:
WOOF detects whether a user is attempting to use an SQL injection vs using a username or a password. It functions off a classification model we developed using the SKLearn library.


## Run backend:
```
$ cd backend && python -m fastapi dev app/main.py
```
Dependencies can be installed with
```
$ cd backend && pip3 install .
```

## Run frontend:
```
$ cd frontend && pnpm i && pnpm run dev 
```
The frontend should now be hosted at http://localhost:5183

## Summary:
WOOF was our submission to the 2025 Cipherhacks hackathon. We learned not to use a monorepo after having conflicts while merging the frontend into the project right before the submission deadline.
