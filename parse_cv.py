import argparse
import logging
import shutil
from pathlib import Path

from pdfminer.high_level import extract_text

LOCAL_FOLDER = Path()
LANGUAGE_KEYWORDS: list[str] = []
LANGUAGE_KEYWORDS_RATE = 10
HOBBY_KEYWORDS: list[str] = []
HOBBY_KEYWORDS_RATE = 2
KEPT_CVS_PATH = Path()


def parse_cv(file_path: Path) -> bool:
    content = extract_text(file_path)

    cv_rate = sum(x.lower() in content.lower() for x in
                  LANGUAGE_KEYWORDS) * LANGUAGE_KEYWORDS_RATE
    cv_rate += sum(
        x.lower() in content.lower() for x in HOBBY_KEYWORDS) * HOBBY_KEYWORDS_RATE

    if cv_rate:
        logging.info("Found CV %s rated %s", str(file_path), cv_rate)
        rate_folder = KEPT_CVS_PATH / ("rated_" + str(cv_rate))
        rate_folder.mkdir(exist_ok=True)
        shutil.copy(file_path,
                    KEPT_CVS_PATH / ("rated_" + str(cv_rate)) / file_path.name)
        return True
    else:
        logging.debug("CV %s does not contain keywords", str(file_path))
        return False


def main():
    global LOCAL_FOLDER, LANGUAGE_KEYWORDS, HOBBY_KEYWORDS, KEPT_CVS_PATH

    parser = argparse.ArgumentParser(
        description="Sort CVs according to keywords. Rate them too")
    parser.add_argument("--folder", type=Path, default=Path(),
                        help="folder where CVs are located")
    parser.add_argument("--language-keywords", nargs="+",
                        help="keywords to find")
    parser.add_argument("--hobby-keywords", nargs="+",
                        help="keywords to find")

    args = parser.parse_args()
    LOCAL_FOLDER = args.folder
    LANGUAGE_KEYWORDS = args.language_keywords
    HOBBY_KEYWORDS = args.hobby_keywords

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

