import argparse
import os

from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--obsidian_folder", type=Path, required=True)
    return parser.parse_args()


def clear_text(raw_text: str):
    return "\n".join(
        line for line in raw_text.strip().split("\n")
        if not line.startswith("<!--SR")
    ) + "\n"


def update_folder(obsidian_folder: Path, folder: str):
    folder_path = Path(folder)
    obs_folder_path_files = list((obsidian_folder / folder).iterdir())

    for file in obs_folder_path_files:
        raw_obs_file = clear_text(open(file).read())
        with open(folder_path / file.name, "w") as cur_file:
            cur_file.write(raw_obs_file)


def update_verbs(obsidian_folder: Path):
    update_folder(obsidian_folder, "verbs")
    verbs = sorted([
        (f.name.split(".")[0], open(f).readlines()[2].strip())
        for f in Path("verbs").iterdir()
    ])
    with open("verb_list.md", "w") as verb_list:
        verb_list.writelines(
            ["Глагол | Перевод\n", "----|----\n"] +
            [f"[[{v[0]}]]|{v[1]}\n" for v in verbs]
        )


def main(args: argparse.Namespace):
    update_folder(args.obsidian_folder, "grammar")
    update_verbs(args.obsidian_folder)


if __name__ == "__main__":
    args = parse_args()
    main(args)
