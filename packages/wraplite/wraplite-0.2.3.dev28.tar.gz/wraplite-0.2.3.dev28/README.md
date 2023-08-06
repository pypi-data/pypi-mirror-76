# WrapLite
Python No SQL SQLite Wrapper

## Installation

```
pip install wraplite
```

## Usage

```python
import wraplite as wl
import datetime as dt
import pandas as pd

# get will automatically create the database if need
simpsons = wl.get('simpsons')

# table definition without any SQL knowledge
simpsons.create_table('sons', wl.TableFormat(
    id = str,
    name = str,
    email = str,
    birthday = dt.date,
    address = str,
).primary_keys(['id']))

data = []
data.append({
  'id': 1,
  'name': 'Bart',
  'email': 'bart@simpsons.com',
  'birthday': dt.date('23-02-1980'),
  'address': '742 Evergreen Terrace in Springfield',
})
data.append({
  'id': 2,
  'name': 'Lisa',
  'email': 'lisa@simpsons.com',
  'birthday': dt.date('09-05-1981'),
  'address': '742 Evergreen Terrace in Springfield',
})

# insert to table with any pandas DataFrame that respect the table format
simpsons.sons.insert(pd.DataFrame(data))
```
