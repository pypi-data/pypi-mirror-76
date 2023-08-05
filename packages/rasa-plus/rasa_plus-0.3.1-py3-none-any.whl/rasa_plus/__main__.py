from os import walk
import click


def _get_files(path, type=None):
    if path.endswith("/"):
        path = path[:-1]
    files = []
    for (dirpath, dirnames, filenames) in walk(path):
        for file in filenames:
            files.append(f"{dirpath}/{file}")
    files.sort()
    return files


def _unify_files(path):
    result = ""
    for file in _get_files(path):
        with open(file, "r") as content:
            c = content.read().rstrip()
            if not c.endswith("\n"):
                c += "\n"
            c += "\n"
            result += c
    return result


def _generate_file(path, filename, content):
    if path.endswith("/"):
        path = path[:-1]
    with open(f"{path}/{filename}", "w+") as f:
        f.write(content)


def _validate(content):
    if len(content) == 0:
        return (content, "Origin file is empty.")
    return (content, "")


@click.group()
def rasa_plus():  # pragma: no cover
    pass


def generic_unify(path, to, filename):
    content = _unify_files(path)
    validated_content, error = _validate(content)
    if validated_content:
        _generate_file(to, filename, content)
        click.echo(f"[SUCCESS] File {filename} created successfully.")
        return "OK"
    else:
        click.echo(f"[ERROR] File {filename} wasn't created. {error}")


def _unify_domain(path="./domain", to=".", filename="domain.yml"):  # pragma: no cover
    generic_unify(path, to, filename)


def _unify_nlu(path="./data/nlu", to="./data", filename="nlu.md"):  # pragma: no cover
    generic_unify(path, to, filename)


def _unify_stories(
    path="./data/stories", to="./data", filename="stories.md"
):  # pragma: no cover
    generic_unify(path, to, filename)


@rasa_plus.command()
def unify_domain(path="./domain", to=".", filename="domain.yml"):  # pragma: no cover
    _unify_domain(path, to, filename)


@rasa_plus.command()
def unify_nlu(path="./data/nlu", to="./data", filename="nlu.md"):  # pragma: no cover
    _unify_nlu(path, to, filename)


@rasa_plus.command()
def unify_stories(
    path="./data/stories", to="./data", filename="stories.md"
):  # pragma: no cover
    _unify_nlu(path, to, filename)


def _unify_project():  # pragma: no cover
    unify_domain()
    unify_nlu()
    unify_stories()
    return "OK"


@rasa_plus.command()
def unify_project():  # pragma: no cover
    _unify_project()


if __name__ == "__main__":  # pragma: no cover
    rasa_plus()
