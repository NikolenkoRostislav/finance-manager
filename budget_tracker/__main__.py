import argparse
import logging

from .analytics import *
from .categorizer import *
from .cleaning import *
from .config import *
from .loaders import *
from .reports import *


def main():
    logger = logging.getLogger()

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--input", help="Input file path")
        parser.add_argument("-m","--month", default=None, help="Display analytics for a specific month (format: YYYY-MM). If not provided, analytics won't be displayed.")

        args = parser.parse_args()

        data_path = args.input
        month = args.month

        config = Config(data_path)

        data = load_data(config)

        data, rejected_rows = clean(data)

        data = categorize(data, config)

        analytics_results = generate_analytics(data, month)

        generate_reports(analytics_results, rejected_rows)

    except Exception as e:
        logger.error("An error occurred: %s", e)
        raise SystemExit(1)


if __name__ == "__main__":
    main()