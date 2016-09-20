# Redmine for lazy people

## Requirements
- Python 2 (Install it via [Chocolatey](https://chocolatey.org/))

  `choco install python2`
  
## Usage
1. Invoke the script with the JSON file that contains your time entries.

  `python redmine.py entries.json`
  
## JSON file format and stuff

You can have an object root (if you only want 1 time entry) or a list root (1 or more entries). Each entry should have a key for the **Issue ID** (id) and **Number of hours spent** (hours). The date can also be specified using the key (date) and must follow the "YYYY-MM-DD" format. Activity can be [design, dev, meeting, review, others, mgt, admin, test], it default to "others" if not specified or other value was given. Comment can also be specified using the key (comment), it is empty by default.

## Example JSON file
```
[
	{
		"id": 96,
		"date": "2016-09-20",
		"hours": 0.25,
		"activity": "dev",
		"comment": "HEHEHEHEHEH :)"
	}
]
```