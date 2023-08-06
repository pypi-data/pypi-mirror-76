from . import client

from .sorting import sort_by_name
from .cache import cache
from .helpers import normalize_model_parameter


@cache
def all_previews_for_shot(shot):
    """
    Args:
        shot (str / dict): The shot dict or the shot ID.

    Returns:
        list: Previews from database for given shot.
    """
    shot = normalize_model_parameter(shot)
    return client.fetch_all("shots/%s/preview-files" % shot["id"])


@cache
def all_shots_for_project(project):
    """
    Args:
        project (str / dict): The project dict or the project ID.

    Returns:
        list: Shots from database or for given project.
    """
    project = normalize_model_parameter(project)
    shots = client.fetch_all("projects/%s/shots" % project["id"])

    return sort_by_name(shots)


@cache
def all_shots_for_sequence(sequence):
    """
    Args:
        sequence (str / dict): The sequence dict or the sequence ID.

    Returns:
        list: Shots which are children of given sequence.
    """
    sequence = normalize_model_parameter(sequence)
    return sort_by_name(
        client.fetch_all("sequences/%s/shots" % sequence["id"])
    )


@cache
def all_sequences_for_project(project):
    """
    Args:
        sequence (str / dict): The sequence dict or the sequence ID.

    Returns:
        list: Sequences from database for given project.
    """
    project = normalize_model_parameter(project)
    sequences = client.fetch_all("projects/%s/sequences" % project["id"])
    return sort_by_name(sequences)


@cache
def all_sequences_for_episode(episode):
    """
    Args:
        sequence (str / dict): The sequence dict or the sequence ID.

    Returns:
        list: Sequences which are children of given episode.
    """
    episode = normalize_model_parameter(episode)
    sequences = client.fetch_all("episodes/%s/sequences" % episode["id"])
    return sort_by_name(sequences)


@cache
def all_episodes_for_project(project):
    """
    Args:
        project (str / dict): The project dict or the project ID.

    Returns:
        list: Episodes from database for given project.
    """
    project = normalize_model_parameter(project)
    episodes = client.fetch_all("projects/%s/episodes" % project["id"])
    return sort_by_name(episodes)


@cache
def get_episode(episode_id):
    """
    Args:
        episode_id (str): Id of claimed episode.

    Returns:
        dict: Episode corresponding to given episode ID.
    """
    return client.fetch_one("episodes", episode_id)


@cache
def get_episode_by_name(project, episode_name):
    """
    Args:
        project (str / dict): The project dict or the project ID.
        episode_name (str): Name of claimed episode.

    Returns:
        dict: Episode corresponding to given name and project.
    """
    project = normalize_model_parameter(project)
    return client.fetch_first(
        "episodes", {"project_id": project["id"], "name": episode_name}
    )


@cache
def get_episode_from_sequence(sequence):
    """
    Args:
        sequence (str / dict): The sequence dict or the sequence ID.

    Returns:
        dict: Episode which is parent of given sequence.
    """
    sequence = normalize_model_parameter(sequence)
    return get_episode(sequence["parent_id"])


@cache
def get_sequence(sequence_id):
    """
    Args:
        sequence_id (str): ID of claimed sequence.

    Returns:
        dict: Sequence corresponding to given sequence ID.
    """
    return client.fetch_one("sequences", sequence_id)


@cache
def get_sequence_by_name(project, sequence_name, episode=None):
    """
    Args:
        project (str / dict): The project dict or the project ID.
        sequence_name (str): Name of claimed sequence.
        episode (str / dict): The episode dict or the episode ID (optional).

    Returns:
        dict: Seqence corresponding to given name and project (and episode in
        case of TV Show).
    """
    project = normalize_model_parameter(project)
    if episode is None:
        params = {"project_id": project["id"], "name": sequence_name}
    else:
        episode = normalize_model_parameter(episode)
        params = {"episode_id": episode["id"], "name": sequence_name}
    return client.fetch_first("sequences", params)


@cache
def get_sequence_from_shot(shot):
    """
    Args:
        shot (str / dict): The shot dict or the shot ID.

    Returns:
        dict: Sequence which is parent of given shot.
    """
    shot = normalize_model_parameter(shot)
    return get_sequence(shot["parent_id"])


@cache
def get_shot(shot_id):
    """
    Args:
        episode_id (str): Id of claimed episode.

    Returns:
        dict: Shot corresponding to given shot ID.
    """
    return client.fetch_one("shots", shot_id)


@cache
def get_shot_by_name(sequence, shot_name):
    """
    Args:
        sequence (str / dict): The sequence dict or the sequence ID.
        shot_name (str): Name of claimed shot.

    Returns:
        dict: Shot corresponding to given name and sequence.
    """
    sequence = normalize_model_parameter(sequence)
    return client.fetch_first(
        "shots/all", {"sequence_id": sequence["id"], "name": shot_name}
    )

@cache
def get_shot_url(shot):
    """
    Args:
        shot (str / dict): The shot dict or the shot ID.

    Returns:
        url (str): Web url associated to the given shot
    """
    shot = normalize_model_parameter(shot)
    path = "{host}/productions/{project_id}/shots/{shot_id}/"
    return path.format(
        host=client.get_zou_url_from_host(),
        project_id=shot["project_id"],
        shot_id=shot["id"],
    )

def new_sequence(project, name, episode=None):
    """
    Create a sequence for given project and episode.

    Args:
        project (str / dict): The project dict or the project ID.
        episode (str / dict): The episode dict or the episode ID.
        name (str): The name of the sequence to create.

    Returns:
        Created sequence.
    """
    project = normalize_model_parameter(project)
    data = {"name": name}

    if episode is not None:
        episode = normalize_model_parameter(episode)
        data["episode_id"] = episode["id"]

    sequence = get_sequence_by_name(project, name, episode=episode)
    if sequence is None:
        return client.post("data/projects/%s/sequences" % project["id"], data)
    else:
        return sequence


def new_shot(
    project,
    sequence,
    name,
    nb_frames=None,
    frame_in=None,
    frame_out=None,
    data={}
):
    """
    Create a shot for given sequence and project. Add frame in and frame out
    parameters to shot extra data. Allow to set metadata too.

    Args:
        project (str / dict): The project dict or the project ID.
        sequence (str / dict): The sequence dict or the sequence ID.
        name (str): The name of the shot to create.
        frame_in (int):
        frame_out (int):
        data (dict): Free field to set metadata of any kind.

    Returns:
        Created shot.
    """
    project = normalize_model_parameter(project)
    sequence = normalize_model_parameter(sequence)

    if frame_in is not None:
        data["frame_in"] = frame_in
    if frame_out is not None:
        data["frame_out"] = frame_out

    data = {"name": name, "data": data, "sequence_id": sequence["id"]}
    if nb_frames is not None:
        data["nb_frames"] = nb_frames

    shot = get_shot_by_name(sequence, name)
    if shot is None:
        return client.post("data/projects/%s/shots" % project["id"], data)
    else:
        return shot


def update_shot(shot):
    """
    Save given shot data into the API. Metadata are fully replaced by the ones
    set on given shot.

    Args:
        shot (dict): The shot dict to update.

    Returns:
        dict: Updated shot.
    """
    return client.put("data/entities/%s" % shot["id"], shot)


def update_sequence(sequence):
    """
    Save given sequence data into the API. Metadata are fully replaced by the
    ones set on given sequence.

    Args:
        sequence (dict): The sequence dict to update.

    Returns:
        dict: Updated sequence.
    """
    return client.put("data/entities/%s" % sequence["id"], sequence)


@cache
def get_asset_instances_for_shot(shot):
    """
    Return the list of asset instances linked to given shot.
    """
    return client.get("data/shots/%s/asset-instances" % shot["id"])


def update_shot_data(shot, data={}):
    """
    Update the metadata for the provided shot. Keys that are not provided are
    not changed.

    Args:
        shot (dict / ID): The shot dicto or ID to save in database.
        data (dict): Free field to set metadata of any kind.

    Returns:
        dict: Updated shot.
    """
    shot = normalize_model_parameter(shot)
    current_shot = get_shot(shot["id"])
    updated_shot = {"id": current_shot["id"], "data": current_shot["data"]}
    updated_shot["data"].update(data)
    update_shot(updated_shot)


def update_sequence_data(sequence, data={}):
    """
    Update the metadata for the provided sequence. Keys that are not provided are
    not changed.

    Args:
        sequence (dict / ID): The sequence dicto or ID to save in database.
        data (dict): Free field to set metadata of any kind.

    Returns:
        dict: Updated sequence.
    """
    sequence = normalize_model_parameter(sequence)
    current_sequence = get_sequence(sequence["id"])

    if not current_sequence.get('data'):
        current_sequence["data"] = {}

    updated_sequence = {
        "id": current_sequence["id"],
        "data": current_sequence["data"]
    }
    updated_sequence["data"].update(data)
    update_sequence(updated_sequence)


def remove_shot(shot, force=False):
    """
    Remove given shot from database.

    Args:
        shot (dict / str): Shot to remove.
    """
    shot = normalize_model_parameter(shot)
    path = "data/shots/%s" % shot["id"]
    params = {}
    if force:
        params = {"force": "true"}
    return client.delete(path, params)


def new_episode(project, name):
    """
    Create an episode for given project.

    Args:
        project (str / dict): The project dict or the project ID.
        name (str): The name of the episode to create.

    Returns:
        dict: Created episode.
    """
    project = normalize_model_parameter(project)
    data = {"name": name}
    episode = get_episode_by_name(project, name)
    if episode is None:
        return client.post("data/projects/%s/episodes" % project["id"], data)
    else:
        return episode


def update_episode(episode):
    """
    Save given episode data into the API. Metadata are fully replaced by the
    ones set on given episode.

    Args:
        episode (dict): The episode dict to update.

    Returns:
        dict: Updated episode.
    """
    return client.put("data/entities/%s" % episode["id"], episode)


def update_episode_data(episode, data={}):
    """
    Update the metadata for the provided episode. Keys that are not provided
    are not changed.

    Args:
        episode (dict / ID): The episode dict or ID to save in database.
        data (dict): Free field to set metadata of any kind.

    Returns:
        dict: Updated episode.
    """
    episode = normalize_model_parameter(episode)
    current_episode = get_sequence(episode["id"])
    updated_episode = {
        "id": current_episode["id"],
        "data": current_episode["data"]
    }
    updated_episode["data"].update(data)
    update_episode(updated_episode)


def remove_episode(episode):
    """
    Remove given episode and related from database.

    Args:
        episode (dict / str): Episode to remove.
    """
    episode = normalize_model_parameter(episode)
    path = "data/entities/%s" % episode["id"]
    return client.delete(path)


def remove_sequence(sequence):
    """
    Remove given sequence and related from database.

    Args:
        sequence (dict / str): Sequence to remove.
    """
    sequence = normalize_model_parameter(sequence)
    path = "data/entities/%s" % sequence["id"]
    return client.delete(path)


@cache
def all_asset_instances_for_shot(shot):
    """
    Args:
        shot (str / dict): The shot dict or the shot ID.

    Returns:
        list: Asset instances linked to given shot.
    """
    shot = normalize_model_parameter(shot)
    return client.get("data/shots/%s/asset-instances" % shot["id"])


def add_asset_instance_to_shot(shot, asset_instance):
    """
    Link a new asset instance to given shot.

    Args:
        shot (str / dict): The shot dict or the shot ID.
        asset_instance (str / dict): The asset instance dict or ID.

    Returns:
        dict: Related shot.
    """
    shot = normalize_model_parameter(shot)
    asset_instance = normalize_model_parameter(asset_instance)
    data = {"asset_instance_id": asset_instance["id"]}
    return client.post("data/shots/%s/asset-instances" % shot["id"], data)


def remove_asset_instance_from_shot(shot, asset_instance):
    """
    Remove link between an asset instance and given shot.

    Args:
        shot (str / dict): The shot dict or the shot ID.
        asset_instance (str / dict): The asset instance dict or ID.
    """
    shot = normalize_model_parameter(shot)
    asset_instance = normalize_model_parameter(asset_instance)
    path = "data/shots/%s/asset-instances/%s" % (
        shot["id"],
        asset_instance["id"],
    )
    return client.delete(path)
