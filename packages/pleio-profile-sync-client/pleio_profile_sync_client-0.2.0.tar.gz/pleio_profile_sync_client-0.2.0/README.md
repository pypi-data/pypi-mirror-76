# Profile sync client
The profile sync client automatically synchronises users from a local identity store to a Pleio subsite. The client is built in Python and uses a REST/JSON API to connect to Pleio.

## How does it work?
The client is installed on a server that is maintained by the subsite holder. The client reads a local file (CSV) that contains a list users. It synchronises the state of the Pleio subsite with the local file. Users that are not on the site are added, the profile of existing users is updated and users not on the list are optionally banned.

The client uses two attributes to link local users with users on the subsite: **external_id** and **email**.

The profile sync client can be used together with Single Sign On (SSO) through SAML2. The SSO flow and the creation of a Pleio user is managed by [account.pleio.nl](https://account.pleio.nl). The authorisation of the Pleio user on the subsite is handled by the profile sync client.

The profile sync client outputs logs to standard output, but also writes the logs to the REST API. The logs can be inspected by the subsite administrator.

## Features
- Automatically creating, updating and blocking users from a subsite
- Ability to sync profile fields and site-specific avatars
- Test the synchronization with the dry-run option
- Remote log inspection by uploading the logs to the REST API

## Requirements
The package requires a Python version >= 3.3.

## Installation
Installation (and updates) are done with a single command:

```bash
$ pip3 install pleio-profile-sync-client
```

## Usage
Use the CLI tool as follows:

```bash
$ pleio-profile-sync-client --api-secret {secret} --source example/users.csv --destination https://{subsite}.pleio.nl/profile_sync_api/
```

The CSV accepts the following fields:

- **external_id**, attribute to link local users with users on the subsite (optional)
- **name**, the full name of the user (required)
- **email**, the e-mailaddress of the user (required)
- **avatar**, a relative link to the avatar in jpeg of the user (optional)
- **groups**, a comma separated field of group guids that adds a user to a group, example field content: `57979220,57979234` (optional)
- **profile.\***, a field containing profile information, example field name: `profile.occupation` (optional)

Check [example/users.csv](./example/users.csv) for an example.

See the help function for the flags that can be used:

```bash
$ pleio-profile-sync-client --help
Usage: pleio-profile-sync-client [OPTIONS]

Options:
  --api-secret TEXT   The profile sync API secret. [envvar=API_SECRET]
  --source TEXT       The source file (formatted as CSV).
  --destination TEXT  The Pleio subsite providing the profile sync.
  --ban BOOLEAN       Ban users on the site who are not listed in the CSV
                      file. [default=False]
  --delete BOOLEAN    Delete users on the site who are not listed in the CSV
                      file. [default=False]
  --dry-run BOOLEAN   Perform a dry run. [default=False]
  --verbose BOOLEAN   Show verbose output [default=True]
  --help              Show this message and exit.
  ```

**Please note** the api-secret is stored in the processlist and in the shell history when running the command like this. For a more secure way of executing the command, check out [example-script.sh](example-script.sh).

## Development
Install the package in development mode with:

```bash
$ pip3 install -e .
```

You can now run pleio-profile-sync-client and at the same time alter the code.

To run the tests:

```bash
$ pip install -r requirements.txt
$ prospector --tool pylint --tool pep8
$ python -m nose2
```
