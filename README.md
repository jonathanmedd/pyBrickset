# pyBrickset

Thanks to Brickfront for inspiration for much of this module: https://github.com/4Kaylum/Brickfront . Have re-used what I found there and updated to work with v3 of the API.

The [www.brickset.com](http://www.brickset.com) website provides an [API](https://brickset.com/api/v3.asmx) for working with their data. This Python module works with version 3 of that [API](https://brickset.com/api/v3.asmx).

**Pre-Requisites**

Created using Python 3.9.1.

An API key from Brickset is required. Currently they are free and you can get one [here](https://brickset.com/tools/webservices/requestkey).
In order to use the inventory features of Brickset to track your own Lego collection a Brickset account is also required.

**Quick Start**

Use of non-inventory functions:

Supply your API key and make a connection using the Client

```
client = pyBrickset.Client('4-e3wM-sWsw-Su3pI')
```

Use of all functions including inventory:

Supply your API key and also Brickset Website credentials to make a connection using the Client

```
client = pyBrickset.Client('4-e3wM-sWsw-Su3pI')
client.login('testuser@test.com', 'P@ssw0rd!')
```

Return all Indiana Jones themed Lego sets

```
sets = client.getSets(theme='Indiana Jones')
print(json.dumps(sets, indent=4))
```

More examples can be found in ```examples.py```