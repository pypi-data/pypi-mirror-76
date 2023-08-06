from . import client

from .sorting import sort_by_name
from .helpers import normalize_model_parameter
from .cache import cache


@cache
def all_organisations():
    """
    Returns:
        list: Organisations listed in database.
    """
    return sort_by_name(client.fetch_all("organisations"))


@cache
def all_persons():
    """
    Returns:
        list: Persons listed in database.
    """
    return sort_by_name(client.fetch_all("persons"))


@cache
def get_person(id):
    """
    Args:
        id (str): An uuid identifying a person.

    Returns:
        dict: Person corresponding to given id.
    """
    return client.fetch_one("persons", id)


@cache
def get_person_by_desktop_login(desktop_login):
    """
    Args:
        desktop_login (str): Login used to sign in on the desktop computer.

    Returns:
        dict: Person corresponding to given desktop computer login.
    """
    return client.fetch_first("persons", {"desktop_login": desktop_login})


@cache
def get_person_by_email(email):
    """
    Args:
        email (str): User's email.

    Returns:
        dict:  Person corresponding to given email.
    """
    return client.fetch_first("persons", {"email": email})


@cache
def get_person_by_full_name(full_name):
    """
    Args:
        full_name (str): User's full name

    Returns:
        dict: Person corresponding to given name.
    """
    if " " in full_name:
        first_name, last_name = full_name.lower().split(" ")
    else:
        first_name, last_name = full_name.lower().strip(), ""
    for person in all_persons():
        is_right_first_name = first_name == person["first_name"].lower().strip()
        is_right_last_name = \
            len(last_name) == 0 or last_name == person["last_name"].lower()
        if is_right_first_name and is_right_last_name:
            return person
    return None


@cache
def get_person_url(person):
    """
    Args:
        person (str / dict): The person dict or the person ID.

    Returns:
        url (str): Web url associated to the given person
    """
    person = normalize_model_parameter(person)
    path = "{host}/people/{person_id}/"
    return path.format(
        host=client.get_zou_url_from_host(),
        person_id=person["id"],
    )


@cache
def get_organisation():
    """
    Returns:
        dict: Database information for organisation linked to auth tokens.
    """
    return client.get("auth/authenticated")["organisation"]


def new_person(
    first_name, last_name, email, phone="", role="user", desktop_login=""
):
    """
    Create a new person based on given parameters. His/her password will is
    set automatically to default.

    Args:
        first_name (str):
        last_name (str):
        email (str):
        phone (str):
        role (str): user, manager, admin (wich match CG artist, Supervisor
                    and studio manager)
        desktop_login (str): The login the users uses to log on its computer.

    Returns:
        dict: Created person.
    """
    person = get_person_by_email(email)
    if person is None:
        person = client.post(
            "data/persons/new",
            {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "role": role,
                "desktop_login": desktop_login,
            },
        )
    return person


def set_avatar(person, file_path):
    """
    Upload picture and set it as avatar for given person.

    Args:
        person (str / dict): The person dict or the person ID.
        file_path (str): Path where the avatar file is located on the hard
                         drive.
    """
    person = normalize_model_parameter(person)
    return client.upload(
        "/pictures/thumbnails/persons/%s" % person["id"], file_path
    )


def get_presence_log(year, month):
    """
    Args:
        year (int):
        month (int):

    Returns:
        The presence log table for given month and year.
    """
    path = "data/persons/presence-logs/%s-%s" % (year, str(month).zfill(2))
    return client.get(path, json_response=False)
