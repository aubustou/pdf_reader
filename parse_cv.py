import argparse
import logging
import shutil
from pathlib import Path

from pdfminer.high_level import extract_text

LANGUAGE_KEYWORDS: list[str] = []
LANGUAGE_KEYWORDS_RATE = 10
HOBBY_KEYWORDS: list[str] = []
HOBBY_KEYWORDS_RATE = 2


def parse_cv(file_path: Path, destination_folder: Path) -> bool:
    content = extract_text(file_path)

    cv_rate = sum(x.lower() in content.lower() for x in
                  LANGUAGE_KEYWORDS) * LANGUAGE_KEYWORDS_RATE
    cv_rate += sum(
        x.lower() in content.lower() for x in HOBBY_KEYWORDS) * HOBBY_KEYWORDS_RATE

    if cv_rate:
        logging.info("Found CV %s rated %s", str(file_path), cv_rate)
        rate_folder = destination_folder / ("rated_" + str(cv_rate))
        rate_folder.mkdir(exist_ok=True)
        shutil.copy(file_path,
                    destination_folder / ("rated_" + str(cv_rate)) / file_path.name)
        return True
    else:
        logging.debug("CV %s does not contain keywords", str(file_path))
        return False


from typing import Iterable


def iter_on_files(local_folder: Path, path_file: Path) -> Iterable[Path]:
    if path_file:
        yield Path(path_file.read_text())
    else:
        yield from local_folder.iterdir()


def main():
    global LANGUAGE_KEYWORDS, HOBBY_KEYWORDS

    parser = argparse.ArgumentParser(
        description="Sort CVs according to keywords. Rate them too")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--folder", type=Path,
                       help="folder where CVs are located")
    group.add_argument("--file", type=Path,
                       help="file with links to the files or websites")
    parser.add_argument("--destination-folder", type=Path,
                        help="folder where the CVs will be copied")
    parser.add_argument("--language-keywords", nargs="+",
                        help="keywords to find")
    parser.add_argument("--hobby-keywords", nargs="+",
                        help="keywords to find")

    args = parser.parse_args()
    if not args.folder or args.file:
        parser.print_usage()

    local_folder = args.folder if args.folder else Path()
    destination_folder = args.destination_folder if args.destination_folder else local_folder / "kept"
    destination_folder.mkdir(exist_ok=True)

    LANGUAGE_KEYWORDS = args.language_keywords
    HOBBY_KEYWORDS = args.hobby_keywords

    logging.basicConfig(level=logging.INFO)
    logging.getLogger("pdfminer").setLevel(logging.WARNING)
    logging.info("Start")

    for file_ in iter_on_files(local_folder, args.file):
        logging.debug(str(file_))
        if file_.suffix not in {".pdf"}:
            continue

        parse_cv(file_, destination_folder)


if __name__ == '__main__':
    main()

