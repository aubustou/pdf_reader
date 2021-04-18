import argparse
import logging
import shutil
from pathlib import Path

from pdfminer.high_level import extract_text

LOCAL_FOLDER = Path()
KEYWORDS = []
KEPT_CVS_PATH = Path()


def parse_cv(file_path: Path) -> bool:
    content = extract_text(file_path)
    logging.info([x.lower() in content.lower() for x in KEYWORDS])

    cv_rate = sum(x.lower() in content.lower() for x in KEYWORDS)

    if cv_rate:
        logging.info("Found CV %s rated %s", str(file_path), cv_rate)
        rate_folder = KEPT_CVS_PATH / ("rated_" + str(cv_rate))
        rate_folder.mkdir(exist_ok=True)
        shutil.copy(file_path,
                    KEPT_CVS_PATH / ("rated_" + str(cv_rate)) / file_path.name)
    else:
        logging.debug("CV %s does not contain keywords", str(file_path))


def main():
    global LOCAL_FOLDER, KEYWORDS, KEPT_CVS_PATH

    parser = argparse.ArgumentParser(
        description="Sort CVs according to keywords. Rate them too")
    parser.add_argument("--folder", type=Path, default=Path(),
                        help="folder where CVs are located")
    parser.add_argument("--keywords", nargs="+",
                        help="keywords to find")

    args = parser.parse_args()
    LOCAL_FOLDER = args.folder
    KEYWORDS = args.keywords

    logging.basicConfig(level=logging.INFO)
    logging.getLogger("pdfminer").setLevel(logging.WARNING)
    logging.info("Start")

    KEPT_CVS_PATH = LOCAL_FOLDER / "kept"
    KEPT_CVS_PATH.mkdir(exist_ok=True)

    for file_ in LOCAL_FOLDER.iterdir():
        logging.debug(str(file_))
        if file_.suffix not in {".pdf"}:
            continue

        parse_cv(file_)


if __name__ == '__main__':
    main()

