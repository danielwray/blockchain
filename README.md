# Overview

Very simple blockchain service written in Python.

## How to use

* Requires Flask, Flask-restful, Python3.5.x

Clone repository, navigate into directory and run:

```
export FLASK_APP=api.py
pyhon3 -m flask run
```

Add a block:
```
curl -X PUT http://localhost:5000/transaction -d "data={'your_keys': 'your_values'}"
```

View block chain index count:
```
curl -X GET http://localhost:5000/
```

View all blocks on the block chain:
```
curl -X GET http://localhost:5000/view
```
