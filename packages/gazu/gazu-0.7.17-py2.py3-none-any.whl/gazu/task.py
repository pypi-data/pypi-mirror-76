import string

from . import client
from .sorting import sort_by_name
from .helpers import normalize_model_parameter

from .cache import cache


@cache
def all_task_statuses():
    """
    Returns:
        list: Task statuses stored in database.
    """
    task_statuses = client.fetch_all("task-status")
    return sort_by_name(task_statuses)


@cache
def all_task_types():
    """
    Returns:
        list: Task types stored in database.
    """
    task_types = client.fetch_all("task-types")
    return sort_by_name(task_types)


@cache
def all_tasks_for_shot(shot, relations=False):
    """
    Args:
        shot (str / dict): The shot dict or the shot ID.

    Returns:
        list: Tasks linked to given shot.
    """
    shot = normalize_model_parameter(shot)
    params = {}
    if relations:
        params = {"relations": "true"}
    tasks = client.fetch_all("shots/%s/tasks" % shot["id"], params)
    return sort_by_name(tasks)


@cache
def all_tasks_for_sequence(sequence, relations=False):
    """
    Args:
        sequence (str / dict): The sequence dict or the sequence ID.

    Returns
        list: Tasks linked to given sequence.
    """
    sequence = normalize_model_parameter(sequence)
    params = {}
    if relations:
        params = {"relations": "true"}
    tasks = client.fetch_all("sequences/%s/tasks" % sequence["id"], params)
    return sort_by_name(tasks)


@cache
def all_tasks_for_scene(scene, relations=False):
    """
    Args:
        sequence (str / dict): The scene dict or the scene ID.

    Returns:
        list: Tasks linked to given scene.
    """
    scene = normalize_model_parameter(scene)
    params = {}
    if relations:
        params = {"relations": "true"}
    tasks = client.fetch_all("scenes/%s/tasks" % scene["id"], params)
    return sort_by_name(tasks)


@cache
def all_tasks_for_asset(asset, relations=False):
    """
    Args:
        asset (str / dict): The asset dict or the asset ID.

    Returns:
        list: Tasks directly linked to given asset.
    """
    asset = normalize_model_parameter(asset)
    params = {}
    if relations:
        params = {"relations": "true"}
    tasks = client.fetch_all("assets/%s/tasks" % asset["id"], params)
    return sort_by_name(tasks)


@cache
def all_tasks_for_episode(episode, relations=False):
    """
    Retrieve all tasks directly linked to given episode.
    """
    episode = normalize_model_parameter(episode)
    params = {}
    if relations:
        params = {"relations": "true"}
    tasks = client.fetch_all("episodes/%s/tasks" % episode["id"], params)
    return sort_by_name(tasks)


@cache
def all_shot_tasks_for_sequence(sequence, relations=False):
    """
    Retrieve all tasks directly linked to all shots of given sequence.
    """
    sequence = normalize_model_parameter(sequence)
    params = {}
    if relations:
        params = {"relations": "true"}
    tasks = client.fetch_all("sequences/%s/shot-tasks" % sequence["id"], params)
    return sort_by_name(tasks)


@cache
def all_shot_tasks_for_episode(episode, relations=False):
    """
    Retrieve all tasks directly linked to all shots of given episode.
    """
    episode = normalize_model_parameter(episode)
    params = {}
    if relations:
        params = {"relations": "true"}
    tasks = client.fetch_all("episodes/%s/shot-tasks" % episode["id"], params)
    return sort_by_name(tasks)


@cache
def all_tasks_for_task_status(project, task_type, task_status):
    """
    Args:
        project (str / dict): The project dict or the project ID.
        task_type (str / dict): The task type dict or ID.
        task_status (str / dict): The task status dict or ID.

    Returns:
        list: Tasks set at given status for given project and task type.
    """
    project = normalize_model_parameter(project)
    task_type = normalize_model_parameter(task_type)
    task_status = normalize_model_parameter(task_status)
    return client.fetch_all(
        "tasks",
        {
            "project_id": project["id"],
            "task_type_id": task_type["id"],
            "task_status_id": task_status["id"],
        },
    )


@cache
def all_tasks_for_task_type(project, task_type):
    """
    Args:
        project (str / dict): The project dict or the project ID.
        task_type (str / dict): The task type dict or ID.

    Returns:
        list: Tasks for given project and task type.
    """
    project = normalize_model_parameter(project)
    task_type = normalize_model_parameter(task_type)
    return client.fetch_all(
        "tasks",
        {
            "project_id": project["id"],
            "task_type_id": task_type["id"],
        },
    )


@cache
def all_task_types_for_shot(shot):
    """
    Args:
        shot (str / dict): The shot dict or the shot ID.

    Returns
        list: Task types of task linked to given shot.
    """
    shot = normalize_model_parameter(shot)
    task_types = client.fetch_all("shots/%s/task-types" % shot["id"])
    return sort_by_name(task_types)


@cache
def all_task_types_for_asset(asset):
    """
    Args:
        asset (str / dict): The asset dict or the asset ID.

    Returns:
        list: Task types of tasks related to given asset.
    """
    asset = normalize_model_parameter(asset)
    task_types = client.fetch_all("assets/%s/task-types" % asset["id"])
    return sort_by_name(task_types)


@cache
def all_task_types_for_scene(scene):
    """
    Args:
        scene (str / dict): The scene dict or the scene ID.

    Returns:
        list: Task types of tasks linked to given scene.
    """
    scene = normalize_model_parameter(scene)
    task_types = client.fetch_all("scenes/%s/task-types" % scene["id"])
    return sort_by_name(task_types)


@cache
def all_task_types_for_sequence(sequence):
    """
    Args:
        sequence (str / dict): The sequence dict or the sequence ID.

    Returns:
        list: Task types of tasks linked directly to given sequence.
    """
    sequence = normalize_model_parameter(sequence)
    task_types = client.fetch_all("sequences/%s/task-types" % sequence["id"])
    return sort_by_name(task_types)


@cache
def all_task_types_for_episode(episode):
    """
    Returns:
        list: Task types of tasks linked directly to given episode.
    """
    episode = normalize_model_parameter(episode)
    task_types = client.fetch_all("episodes/%s/task-types" % episode["id"])
    return sort_by_name(task_types)


@cache
def all_tasks_for_entity_and_task_type(entity, task_type):
    """
    Args:
        entity (str / dict): The entity dict or the entity ID.
        task_type (str / dict): The task type dict or ID.

    Returns:
        list: Tasks for given entity or task type.
    """
    entity = normalize_model_parameter(entity)
    task_type = normalize_model_parameter(task_type)
    task_type_id = task_type["id"]
    entity_id = entity["id"]
    return client.fetch_all(
        "entities/%s/task-types/%s/tasks" % (entity_id, task_type_id)
    )


@cache
def all_tasks_for_person(person):
    """
    Returns:
        list: Tasks that are not done for given person (only for open projects).
    """
    person = normalize_model_parameter(person)
    return client.fetch_all("persons/%s/tasks" % person["id"])


@cache
def all_done_tasks_for_person(person):
    """
    Returns:
        list: Tasks that are done for given person (only for open projects).
    """
    person = normalize_model_parameter(person)
    return client.fetch_all("persons/%s/done-tasks" % person["id"])


@cache
def get_task_by_name(entity, task_type, name="main"):
    """
    Deprecated.

    Args:
        entity (str / dict): The entity dict or the entity ID.
        task_type (str / dict): The task type dict or ID.
        name (str): Name of the task to look for.

    Returns:
        Task matching given name for given entity and task type.
    """
    entity = normalize_model_parameter(entity)
    task_type = normalize_model_parameter(task_type)
    return client.fetch_first(
        "tasks",
        {
            "name": name,
            "task_type_id": task_type["id"],
            "entity_id": entity["id"],
        },
    )


@cache
def get_task_type(task_type_id):
    """
    Args:
        task_type_id (str): Id of claimed task type.

    Returns:
        dict: Task type matching given ID.
    """
    return client.fetch_one("task-types", task_type_id)


@cache
def get_task_type_by_name(task_type_name):
    """
    Args:
        task_type_name (str): Name of claimed task type.

    Returns:
        dict: Task type object for given name.
    """
    return client.fetch_first("task-types", {"name": task_type_name})


@cache
def get_task_by_path(project, file_path, entity_type="shot"):
    """
    Args:
        project (str / dict): The project dict or the project ID.
        file_path (str): The file path to find a related task.
        entity_type (str): asset, shot or scene.

    Returns:
        dict: A task from given file path. This function requires context:
        the project related to the given path and the related entity type.
    """
    project = normalize_model_parameter(project)
    data = {
        "file_path": file_path,
        "project_id": project["id"],
        "type": entity_type,
    }
    return client.post("data/tasks/from-path/", data)


@cache
def get_task_status(task):
    """
    Args:
        task (str / dict): The task dict or the task ID.

    Returns:
        A task status object corresponding to status set on given task.
    """
    task = normalize_model_parameter(task)
    return client.fetch_first("task-status", {"id": task["task_status_id"]})


@cache
def get_task_status_by_name(name):
    """
    Args:
        name (str / dict): The name of claimed task status.

    Returns:
        dict: Task status matching given name.
    """
    return client.fetch_first("task-status", {"name": name})


@cache
def get_task_status_by_short_name(task_status_short_name):
    """
    Args:
        short_name (str / dict): The short name of claimed task status.

    Returns:
        dict: Task status matching given short name.
    """
    return client.fetch_first(
        "task-status", {"short_name": task_status_short_name}
    )


def remove_task_status(task_status):
    """
    Remove given task status from database.

    Args:
        task_status (str / dict): The task status dict or ID.
    """
    task_status = normalize_model_parameter(task_status)
    return client.delete(
        "data/task-status/%s" % task_status["id"], {"force": "true"}
    )


@cache
def get_task(task_id):
    """
    Args:
        task_id (str): Id of claimed task.

    Returns:
        dict: Task matching given ID.
    """
    task_id = normalize_model_parameter(task_id)
    return client.get("data/tasks/%s/full" % task_id["id"])


def new_task(
    entity,
    task_type,
    name="main",
    task_status=None,
    assigner=None,
    assignees=None,
):
    """
    Create a new task for given entity and task type.

    Args:
        entity (dict): Entity for which task is created.
        task_type (dict): Task type of created task.
        name (str): Name of the task (default is "main").
        task_status (dict): The task status to set (default status is Todo).
        assigner (dict): Person who assigns the task.
        assignees (list): List of people assigned to the task.

    Returns:
        Created task.
    """
    entity = normalize_model_parameter(entity)
    task_type = normalize_model_parameter(task_type)
    if task_status is None:
        task_status = get_task_status_by_name("Todo")

    data = {
        "project_id": entity["project_id"],
        "entity_id": entity["id"],
        "task_type_id": task_type["id"],
        "task_status_id": task_status["id"],
        "name": name,
    }

    if assigner is not None:
        data["assigner_id"] = assigner["id"]

    if assignees is not None:
        data["assignees"] = [person["id"] for person in assignees]
    else:
        data["assignees"] = []

    task = get_task_by_name(entity, task_type, name)
    if task is None:
        task = client.post("data/tasks", data)
    return task


def remove_task(task):
    """
    Remove given task from database.

    Args:
        task (str / dict): The task dict or the task ID.
    """
    task = normalize_model_parameter(task)
    client.delete("data/tasks/%s" % task["id"], {"force": "true"})


def start_task(task):
    """
    Change a task status to WIP and set its real start date to now.

    Args:
        task (str / dict): The task dict or the task ID.

    Returns:
        dict: Modified task.
    """
    task = normalize_model_parameter(task)
    path = "actions/tasks/%s/start" % task["id"]
    return client.put(path, {})


def task_to_review(task, person, comment, revision=1, change_status=True):
    """
    Deprecated.
    Mark given task as pending, waiting for approval. Author is given through
    the person argument.

    Args:
        task (str / dict): The task dict or the task ID.
        person (str / dict): The person dict or the person ID.
        comment (str): Comment text
        revision (int): Force revision of related preview file
        change_status (bool): If set to false, the task status is not changed.

    Returns:
        dict: Modified task
    """
    task = normalize_model_parameter(task)
    person = normalize_model_parameter(person)
    path = "actions/tasks/%s/to-review" % task["id"]
    data = {
        "person_id": person["id"],
        "comment": comment,
        "revision": revision,
        "change_status": change_status,
    }

    return client.put(path, data)


@cache
def get_time_spent(task, date):
    """
    Get the time spent by CG artists on a task at a given date. A field contains
    the total time spent.  Durations are given in seconds. Date format is
    YYYY-MM-DD.

    Args:
        task (str / dict): The task dict or the task ID.
        date (str): The date for which time spent is required.

    Returns:
        dict: A dict with person ID as key and time spent object as value.
    """
    task = normalize_model_parameter(task)
    path = "actions/tasks/%s/time-spents/%s" % (task["id"], date)
    return client.get(path)


def set_time_spent(task, person, date, duration):
    """
    Set the time spent by a CG artist on a given task at a given date. Durations
    must be set in seconds. Date format is YYYY-MM-DD.

    Args:
        task (str / dict): The task dict or the task ID.
        person (str / dict): The person who spent the time on given task.
        date (str): The date for which time spent must be set.
        duration (int): The duration of the time spent on given task.

    Returns:
        dict: Created time spent entry.
    """
    task = normalize_model_parameter(task)
    person = normalize_model_parameter(person)
    path = "actions/tasks/%s/time-spents/%s/persons/%s" % (
        task["id"],
        date,
        person["id"],
    )
    return client.post(path, {"duration": duration})


def add_time_spent(task, person, date, duration):
    """
    Add given duration to the already logged duration for given task and person
    at a given date. Durations must be set in seconds. Date format is
    YYYY-MM-DD.

    Args:
        task (str / dict): The task dict or the task ID.
        person (str / dict): The person who spent the time on given task.
        date (str): The date for which time spent must be added.
        duration (int): The duration to add on the time spent on given task.

    Returns:
        dict: Updated time spent entry.
    """
    task = normalize_model_parameter(task)
    person = normalize_model_parameter(person)
    path = "actions/tasks/%s/time-spents/%s/persons/%s/add" % (
        task["id"],
        date,
        person["id"],
    )
    return client.post(path, {"duration": duration})


def add_comment(
    task,
    task_status,
    comment="",
    person=None,
    attachments=[],
    created_at=None
):
    """
    Add comment to given task. Each comment requires a task_status. Since the
    addition of comment triggers a task status change. Comment text can be
    empty.

    Args:
        task (str / dict): The task dict or the task ID.
        task_status (str / dict): The task status dict or ID.
        comment (str): Comment text
        person (str / dict): Comment author
        date (str): Comment date

    Returns:
        dict: Created comment.
    """
    task = normalize_model_parameter(task)
    task_status = normalize_model_parameter(task_status)
    data = {"task_status_id": task_status["id"], "comment": comment}

    if person is not None:
        person = normalize_model_parameter(person)
        data["person_id"] = person["id"]

    if created_at is not None:
        data["created_at"] = created_at

    if len(attachments) == 0:
        return client.post("actions/tasks/%s/comment" % task["id"], data)

    else:
        attachment = attachments.pop()
        return client.upload(
            "actions/tasks/%s/comment" % task["id"],
            attachment,
            data=data,
            extra_files=attachments
        )


def remove_comment(comment):
    """
    Remove given comment and related (previews, news, notifications) from
    database.

    Args:
        comment (str / dict): The comment dict or the comment ID.
    """
    comment = normalize_model_parameter(comment)
    return client.delete("data/comments/%s" % comment["id"])


def create_preview(task, comment):
    """
    Create a preview into given comment.

    Args:
        task (str / dict): The task dict or the task ID.
        comment (str / dict): The comment or the comment ID.

    Returns:
        dict: Created preview file model.
    """
    task = normalize_model_parameter(task)
    comment = normalize_model_parameter(comment)
    path = "actions/tasks/%s/comments/%s/add-preview" % (
        task["id"],
        comment["id"],
    )
    return client.post(path, {})


def upload_preview_file(preview, file_path):
    """
    Create a preview into given comment.

    Args:
        task (str / dict): The task dict or the task ID.
        file_path (str): Path of the file to upload as preview.
    """
    path = "pictures/preview-files/%s" % preview["id"]
    client.upload(path, file_path)


def add_preview(task, comment, preview_file_path):
    """
    Add a preview to given comment.

    Args:
        task (str / dict): The task dict or the task ID.
        comment (str / dict): The comment or the comment ID.
        preview_file_path (str): Path of the file to upload as preview.

    Returns:
        dict: Created preview file model.
    """
    preview_file = create_preview(task, comment)
    upload_preview_file(preview_file, preview_file_path)
    return preview_file


def set_main_preview(preview_file):
    """
    Set given preview as thumbnail of given entity.

    Args:
        preview_file (str / dict): The preview file dict or ID.

    Returns:
        dict: Created preview file model.
    """
    preview_file = normalize_model_parameter(preview_file)
    path = "actions/preview-files/%s/set-main-preview" % preview_file["id"]
    return client.put(path, {})


@cache
def all_comments_for_task(task):
    """
    Args:
        task (str / dict): The task dict or the task ID.

    Returns:
        Comments linked to the given task.
    """
    task = normalize_model_parameter(task)
    return client.fetch_all("tasks/%s/comments" % task["id"])


@cache
def get_last_comment_for_task(task):
    """
    Args:
        task (str / dict): The task dict or the task ID.

    Returns:
        Last comment posted for given task.
    """
    task = normalize_model_parameter(task)
    return client.fetch_first("tasks/%s/comments" % task["id"])


@cache
def assign_task(task, person):
    """
    Assign one Person to a Task.
    Args:
        task (str / dict): The task dict or the task ID.
        person (str / dict): The person dict or the person ID.

    Returns:
        (dict) the affected Task
    """
    person = normalize_model_parameter(person)
    task = normalize_model_parameter(task)
    route = "/actions/persons/%s/assign" % person["id"]
    return client.put(route, {"task_ids": task["id"]})


def new_task_type(name):
    """
    Create a new task type with the given name.

    Args:
        name (str): The name of the task type

    Returns:
        dict: The created task type
    """
    data = {"name": name}
    return client.post("data/task-types", data)


def new_task_status(name, short_name, color):
    """
    Create a new task status with the given name, short name and color.

    Args:
        name (str): The name of the task status
        short_name (str): The short name of the task status
        color (str): The color of the task status has an hexadecimal string
        with # as first character. ex : #00FF00

    Returns:
        dict: The created task status
    """
    assert color[0] == "#"
    assert all(c in string.hexdigits for c in color[1:])

    data = {"name": name, "short_name": short_name, "color": color}
    return client.post("data/task-status", data)


def update_task(task):
    """
    Save given task data into the API. Metadata are fully replaced by the ones
    set on given task.

    Args:
        task (dict): The task dict to update.

    Returns:
        dict: Updated task.
    """
    return client.put("data/tasks/%s" % task["id"], task)


def update_task_data(task, data={}):
    """
    Update the metadata for the provided task. Keys that are not provided are
    not changed.

    Args:
        task (dict / ID): The task dict or ID to save in database.
        data (dict): Free field to set metadata of any kind.

    Returns:
        dict: Updated task.
    """
    task = normalize_model_parameter(task)
    current_task = get_task(task["id"])

    updated_task = {"id": current_task["id"], "data": current_task["data"]}
    if updated_task["data"] is None:
        updated_task["data"] = {}
    updated_task["data"].update(data)
    update_task(updated_task)


@cache
def get_task_url(task):
    """
    Args:
        task (str / dict): The task dict or the task ID.

    Returns:
        url (str): Web url associated to the given task
    """
    task = normalize_model_parameter(task)
    path = "{host}/productions/{project_id}/shots/tasks/{task_id}/"
    return path.format(
        host=client.get_zou_url_from_host(),
        project_id=task["project_id"],
        task_id=task["id"],
    )
