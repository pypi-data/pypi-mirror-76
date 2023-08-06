"""Console script for nbreproduce."""
import argparse
import sys

from .nbreproduce import (
    _download_notebook_from_url,
    check_docker_image,
    reproduce,
    _link_docker_notebook,
    reproduce_script,
    _run_live_env,
)


def main():
    """Console script for nbreproduce."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "notebook",
        help="Path to notebook/script locally",
        default="reproduce.sh",
        nargs="?",
    )
    parser.add_argument(
        "--url",
        help="URL to notebook, currently works only for GitHub",
        dest="url",
        action="store_true",
    )
    parser.add_argument(
        "--docker",
        help="Name of Docker image on DockerHub",
        default="econark/econ-ark-notebook:latest",
    )
    parser.add_argument(
        "--live",
        help="Run nbreproduce in live mode, it exposes a jupyter server instance running inside the docker container on port 8888",
        dest='live',
        action="store_true",
    )
    parser.add_argument("--timeout", help="indvidual cell timeout limit, default 600s")
    args = parser.parse_args()
    if args.live:
        print(f"Running in live interactive mode using the {args.docker} docker image.")
        _run_live_env(args.docker)
        return 0
    if args.url:
        notebook = _download_notebook_from_url(args.notebook)
        reproduce(notebook, args.timeout, args.docker)
        return 0
    elif args.notebook is not None:
        # sanity check, notebook extension or bash script
        if args.notebook[-6:] != ".ipynb" and args.notebook[-3:] != ".sh":
            raise ValueError("Not a Jupyter notebook or a bash script.")
        if args.notebook[:4] == "http":
            raise ValueError("Use --url flag to pass in a URL to a Jupyter Notebook.")
        notebook = args.notebook

    if notebook[-3:] == ".sh":
        if args.docker is None:
            raise ValueError("Please provide a docker image to execute the script.")
        reproduce_script(notebook, args.docker)
        return 0

    # if not check_docker_image(notebook):
    #     if args.docker is None:
    #         raise ValueError(
    #             f'No linked Docker image found in the metadata, link it using "nbreproduce --docker image_name {notebook}" \
    #             The Docker image should be built using the base Jupyter docker-stacks images, https://jupyter-docker-stacks.readthedocs.io'
    #         )
    #     link_docker_notebook(notebook, args.docker)

    # # force new docker link
    # if args.docker is not None:
    #     link_docker_notebook(notebook, args.docker)

    reproduce(notebook, args.timeout, args.docker)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
