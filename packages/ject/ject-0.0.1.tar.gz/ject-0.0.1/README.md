## ject
##### function/lambda extensions

### Usage
```python
from ject.length import length

def fun(a, b, *args, **kwargs): return a, b, args, kwargs

print(length(fun))
```