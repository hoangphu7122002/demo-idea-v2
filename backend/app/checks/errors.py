"""Domain errors of the check feature. Each carries the HTTP status the API maps it to."""


class CheckError(Exception):
    """Base class for check failures that the API reports to the client."""

    status_code = 500


class PostNotFound(CheckError):
    """No post exists with the requested slug."""

    status_code = 404

    def __init__(self) -> None:
        super().__init__("Post not found")


class InvalidRelease(CheckError):
    """The release input is unusable: unknown URL, or neither URL nor text was given."""

    status_code = 422


class CheckServiceUnavailable(CheckError):
    """The live check failed or is disabled, and no cached result exists for these inputs."""

    status_code = 503
