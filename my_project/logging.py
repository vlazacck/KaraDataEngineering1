import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="data_cleaning.log"
)

logging.info("Starting data cleaning process...")