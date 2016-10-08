# Api Specification

Login
-----

Request:
```
POST /v1/login
{
    "username": "<some_username>",
    "password": "<some_password>"
}
```

Response:
```
{
    "success": "true"
}
```

Logout
------

Request
```
POST /v1/logout
```

Response:
```
{
    "success": "true"
}
```

Change Password
---------------

Request
```
POST /v1/change_password
{
    "old_password": "<old_password>",
    "new_password": "<new_password>"
}
```

Response:
```
{
    "success": "true"
}
```

Forgot Password
---------------

Request:
```
POST /v1/forgot_password/p1
{
    "username": "<some_username>"
}
```

Response:
```
{
    "valid": "true"
}

or

{
	"valid": "false"
}
```

Request:
```
POST /v1/forgot_password/p2
{
	"username": "<some_username>",
	"token": "<some_token>",
	"new_password": "<some_new_password>"
}
```

Response:
```
{
	"success": "true"
}

or

{
	"success": "false"
}
```

View Complaints
===============

View all complaints
-------------------

Request:
```
GET /v1/complaints/all/{from}/{to}
```

Response:
```
{
	[
		{
			"number": ,
			"time_stamp": ,
			"status": ,
			"text": ,
			"by": ,
			"source": ,
		},
		...
		...
		{
			"number": ,
			"time_stamp": ,
			"status": ,
			"text": ,
			"by": ,
			"source": ,
		}
	]
}
```

View a specific complaint
-------------------------

Request:
```
GET /v1/complaints/{complaint_no}
```
Response:

```
{
	"number": ,
	"time_stamp": ,
	"status": ,
	"text": ,
	"by": ,
	"source": ,
}
```

Resolve or Reject a complaint
-----------------------------

Request:

```
POST /v1/complaint/{complaint_no}/status/

{
	status: {resolved or rejected}
}
```

Response:
```
{
	success: "true"
}
```
