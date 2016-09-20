import json
import datetime
import requests
import getpass
import sys

# date today in YYYY-MM-DD
DATE_TODAY = str(datetime.datetime.now())[:10]

# activity names and their IDs in redmine
ACTIVITIES = {
    'design': 8,
    'dev': 9,
    'meeting': 10,
    'review': 11,
    'others': 12,
    'mgt': 13,
    'admin': 14,
    'test': 15,
}

# result of running this script
DATA = {
    'success': 0,
    'failed': 0,
}


# calls the redmine API to create a new time entry
def create_entry(entry):
    entry = clean_entry(entry)

    r = requests.post(
        'http://redmine.rococoglobaltechnologies.com/time_entries.json',
        json=entry, auth=(DATA['u'], DATA['p']))

    if r.status_code is 201:
        DATA['success'] += 1
    else:
        DATA['failed'] += 1


# tidies the time entry and sets defaults accordingly
def clean_entry(entry):
    # validate issue ID
    check('id', int, entry)
    entry['issue_id'] = entry['id']

    # validate number of hours
    check('hours', float, entry)

    entry['spent_on'] = entry['date'] if 'date' in entry else DATE_TODAY
    entry['comments'] = entry['comment'] if 'comment' in entry else ''

    # validate type of activity done
    check('activity', unicode, entry)
    try:
        entry['activity_id'] = ACTIVITIES[entry['activity']]
    except KeyError:
        print "%s activity is not found, defaulting to 'others'" % entry['activity']

    return {'time_entry': entry}


# empty check and type check
def check(param, expected_type, entry):
    if param not in entry:
        raise ValueError("'%s' is required!" % param)

    if type(entry[param]) is not expected_type:
        raise ValueError("'%s' should be %s, not %s" % (param, expected_type, type(entry[param])))


if __name__ == '__main__':
    with open(sys.arg[1]) as data:
        try:
            entries = json.load(data)

            DATA['u'] = raw_input('Redmine username: ')
            DATA['p'] = getpass.getpass('Redmine password: ')

            if type(entries) is list:
                for entry in entries:
                    create_entry(entry)
            else:
                # probably single entry lang
                create_entry(entries)

            print 'No. of successfully created time entries: %s' % DATA['success']
            print 'No. of failed time entries: %s' % DATA['failed']
        except ValueError as e:
            print str(e)
