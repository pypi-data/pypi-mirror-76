An unofficial API wrapper for the forismatic.com API.

# Installation
 
## Install with Pip (Recommended)

```bash
pip install forismatic.py
```

## Install from source 

```bash
git clone https://github.com/ihumanbeing/forismatic.py.git
cd forismatic.py
python setup.py install
```

# Usage

Example getting an english quote:

```python
from forismatic import *
f = forismatic.ForismaticPy()
f.get_Quote('en') # English, for russian, use 'ru'
```

Output:
```bash
('Victory belongs to the most persevering.  ', 'Napoleon Bonaparte ')
```
