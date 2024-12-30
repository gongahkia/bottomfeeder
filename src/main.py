# ----- REQUIRED IMPORTS -----

import helper as h
import scraper as s

# ----- EXECUTION CODE -----

if __name__ == "__main__":
    LOG_FILEPATH = "./src/generated_log/log.json"
    elit_endpoint_array = s.smart_find_url_endpoint(50)
    storage_map = {}
    for url in elit_endpoint_array:
        storage_map = s.silly_scrape(url, storage_map)
    overall_wrapper = {
        "num_url": h.check_true_number(elit_endpoint_array),
        "log_data": storage_map,
    }
    h.unsafe_write_json(overall_wrapper, LOG_FILEPATH)
