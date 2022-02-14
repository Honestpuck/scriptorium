# Docker Additions

As mentioned in the [MacAdmins Slack](https://macadmins.slack.com/archives/C02JJ35PZ51/p1644515156418309?thread_ts=1644273031.107999&cid=C02JJ35PZ51), this branch adds Docker support to the `scriptorium` script.

There are some minor changes in the main script that need to happen for `scriptorium` to run successfully, but a future commit will address those outstanding issues.

Please feel free to reach out via DM [@pythoninthegrass](https://macadmins.slack.com/archives/D1TE80HA7).

## Setup
* The `Dockerfile` heavily borrows from a [Medium](https://luis-sena.medium.com/creating-the-perfect-python-dockerfile-51bdec41f1c8) article
    * It creates two images:
        * `builder-image`: scaffolds the environment and its dependencies
        * `runner-image`:
            * installs minimal dependencies
            * creates user, sets permissions, copies virtualenv from builder
            * creates a virtualenv and sets `$PATH` for Python
            * calls `ENTRYPOINT` and/or `CMD`
    * By discarding the first `builder-image` it reduces file size of the final image
* To initiate the build process via `docker-compose`:
    ```bash
    # clean build (remove `--no-cache` to improve rebuilds with minor edits)
    docker-compose build --no-cache --parallel
    ```
    * Other functionality
        * Mounts the current working directory as a volume in the `WORKDIR`
            * This allows for testing on the host machine while running the container
        * Setup an interactive environment via `stdin_open` and `tty` directives set to `true`
            * Equivalent to `docker run -it`
            * If both are set to `false`, `docker-compose` will look for `ENTRYPOINT` and/or `CMD` in the `Dockerfile`

## Usage
* For general testing within a shell, leave the entrypoint commented out to simply call `CMD [ "bash" ]`
* After the main script is refactored, uncommenting out the entrypoint and `CMD ["-h"]` will run `scriptorium` with the `-h` or __help__ argument passed
* Docker commands
    ```bash
    # start container
    docker-compose up --remove-orphans -d

    # exec into container
    docker attach scriptorium

    # run command inside container
    python scriptorium.py

    # destroy container
    docker-compose down
    ```

## Further Reading
[Honestpuck/scriptorium: A utility for managing the scripts in Jamf Pro](https://github.com/Honestpuck/scriptorium)

[Orientation and setup | Docker Documentation](https://docs.docker.com/get-started/)

[Creating the Perfect Python Dockerfile | by Luis Sena | Medium](https://luis-sena.medium.com/creating-the-perfect-python-dockerfile-51bdec41f1c8)

[Dockerfile: ENTRYPOINT vs CMD - CenturyLink Cloud Developer Center](https://www.ctl.io/developers/blog/post/dockerfile-entrypoint-vs-cmd/)

[Interactive shell using Docker Compose - Stack Overflow](https://stackoverflow.com/a/39150040)
