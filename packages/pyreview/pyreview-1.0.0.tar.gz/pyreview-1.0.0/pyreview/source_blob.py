import tarfile

import requests


def create_archive(path, tag):
    """
    create the artifact to upload to Heroku Source API

    Notes:
        - recursive=True is the default
        - consult tar.add() filter kwarg for excluding files and paths
    """
    name = f"source_blob_{tag}.tar.gz"

    print("Zipping the project...")
    with tarfile.open(name=name, mode="x:gz") as tar:
        tar.add(path, recursive=True, arcname=".")

    print("Done!")
    print()
    return name


def create_source_blob(base_url, headers, base_dir, project_name, version):
    """
    Upload the a gzipped tar archive of source code
    Necessary for creating a new Review App

    Returns a url with the archive for build.
    """
    url = f"{base_url}/apps/{project_name}/sources"

    res = requests.post(url, headers=headers)
    res.raise_for_status()

    source_blob = res.json().get("source_blob", {})
    get_url = source_blob.get("get_url")
    put_url = source_blob.get("put_url")

    source_blob_filename = create_archive(base_dir, version)

    print("Uploading zipped project... This can take a bit...")
    res = requests.put(
        put_url, headers={"Content-Type": ""}, data=open(source_blob_filename, "rb")
    )
    res.raise_for_status()

    print("Done!")
    print()
    return get_url
