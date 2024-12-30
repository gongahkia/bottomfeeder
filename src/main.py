# ----- REQUIRED IMPORTS -----

import helper as h
import scraper as s

# ----- EXECUTION CODE -----

if __name__ == "__main__":
    LOG_FILEPATH = "./src/generated_log/log.json"
    elit_endpoint_array = s.smart_find_url_endpoint(50)
    overall_wrapper = {
        "num_url": h.check_true_number(elit_endpoint_array),
        "log_data": [s.silly_scrape(url) for url in elit_endpoint_array],
    }
    h.unsafe_write_json(overall_wrapper, LOG_FILEPATH)
