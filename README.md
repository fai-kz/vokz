# Python API client for vo.fai.kz


## Usage
```python
from vokz import Client
client = Client("<your API key>")
```
The API key is available upon registering at vo.fai.kz

```python
# Query status of your submissions
status = client.get_submissions()
```

## Dependency
- `pyzmq` (installed automatically with `pip`)
