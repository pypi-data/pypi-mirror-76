# Bytes Argument Serializer

```python
from byarse import Pickle, BAS


bas = BAS()


# Serialize
x = bas.s([
    b'Bytes',
    'String',
    1, # Int
    1.1, # Float
    Pickle(Class)
])


# Deserialize and print arguments
z = bas.u(x)

for i in z:
    print(i)
```
