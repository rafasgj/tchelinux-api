# Tchelinux CMS API

The Tchelinux CMS API main goal is to allow for easier management of
Tchelinux's events.

## Security

Some API endpoints are not available for unauthorized access, some are only
available for a small set of _administrator_ users. We use JWT (JSON Web Tokens)
to verify access.

## User

Manages users and their attributes in the database.

### Endpoints

> /user

* POST: Create a new user. The required fields are name, email and password.

> /login

* POST: Start a user session. The required fields are email and password.

> /logout

* GET: Terminates user session.

### User Object Schema

> TODO: Add user schema.

## City

Manage cities in the database.

### Endpoints

> /cities

* GET: Retrieve all available cities.

> /city

* POST: Add a new city.

### City Object Schema
```json
{
    "type": "object",
    "description": "A city object.",
    "required": ["cname", "name"],
    "properties": {
        "cname": {
            "type": "string",
            "description": "The city code, used as subdomain.",
            "examples": ["nh", "poa", "camaqua"]
        },
        "name": {
            "type": "string",
            "description": "The city name.",
            "examples": ["Novo Hamburgo", "Porto Alegre", "Camaquã"]
        }
    }
}
```

## Institution

Manage institutions in the database.

### Endpoints

> /institution/\<city\>

* GET: Retrieve all available institutions in the given city name or CNAME.


> /institution

* POST: Add a new institution.

### Institution Object Schema

```json
{
    "type": "object",
    "description": "The institution where the event occurs.",
    "required": ["name", "nick", "city", "address"],
    "properties": {
        "name": {
            "type": "string",
            "description": "The institution official name."
        },
        "nick": {
            "type": "string",
            "description": "A shorter version of the institution name."
        },
        "city": {
            "type": "string",
            "description": "The CNAME of a city. It must exist in the database."
        },
        "address": {
            "type": "string",
            "description": "The address of the institution."
        }
    }
}
```

## Event

Manage events in the database.

### Endpoints

> /events

* GET: Retrieve the next programmed events.

> /event
* POST: Create a new event.

* GET: Retrieve the next programmed events closer than a given distance.

> /event

* GET: Retrieve the next programmed event.
* POST: Create a new event.

> /event/<city>

* GET: Retrieve the next event programmed for the given city.

> TODO: All the remaining endpoints are not yet implemented.

> /events/<latitude>/<longitude>

* GET: Retrieve the next programmed events closer than 150Km.

> /events/<latitude>/<longitude>/<distance>

### Event Object Schema

> TODO: Add event schema.

## Database Migration

Database migration is performed using Alembic, but is automatically executed
when the system version (see the file [tchelinux.version](tchelinux/version.py))
is changed.
