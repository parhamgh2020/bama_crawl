import traceback
from time import sleep
from src.route import fetch_data


start_msg = "initializing"

if __name__ == '__main__':
    while True:
        try:
            print(start_msg)
            res = fetch_data(start_msg)
            start_msg = "loop start" if res else start_msg
        except Exception as err:
            print(f"err: {err}")
            print(traceback.format_exc())
            sleep(5)


