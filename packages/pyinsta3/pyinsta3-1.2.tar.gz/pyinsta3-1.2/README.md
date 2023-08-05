# pyinsta3
pyinsta3 is a package to get instagram profile info of any user.

# Installation
```
pip install pyinsta3
```
OR
```
pip3 install pyinsta3
```

# Usage
## Profile Class
```python
from pyinsta3 import Profile

profile = Profile("officialrickastley")
data = profile.get_data()
name = data["full_name"]
print(name)

> Rick Astley
```

## Profile Class
```python
from pyinsta3 import AsyncProfile
import asyncio

async def test():
	profile = AsyncProfile("officialrickastley")
	data = await profile.get_data
	name = data["full_name"]
	print(name)
	
asyncio.run(test())

> Rick Astley
```

Keys in the data dictionary -
```
username
full_name
biography
followers
following
posts
is_private
is_verified
profile_pic_url
```