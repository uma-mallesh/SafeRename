from pathlib import Path


def resolve_collision(directory, filename):

    file_path = Path(filename)

    stem = file_path.stem
    suffix = file_path.suffix

    counter = 1

    new_name = filename

    while (Path(directory) / new_name).exists():

        new_name = f"{stem}({counter}){suffix}"

        counter += 1

    return new_name