import traceback
from time import sleep
from src.route import fetch_data

if __name__ == '__main__':
    while True:
        try:
            print("loop start")
            fetch_data()
        except Exception as err:
            print(f"err: {err}")
            sleep(5)

