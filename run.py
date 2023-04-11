import multiprocessing
import time,requests

PROCESSES = 1


def process_txn(task_queue):
    while not task_queue.empty():
        txn = task_queue.get()
        data = requests.get(f"https://api.buydigit.com/kraken/check-kraken-deposit/{txn}").json()
        print("PROCESSED", txn,data)
    return True

def run():
    while 1:
        task_queue = multiprocessing.Queue()
        data = requests.get("https://api.buydigit.com/gateway/transactions/toprocess").json()
        for txn in data["transactions"]:
            task_queue.put(txn[0])
        processes = []
        print(f"Running with {PROCESSES} processes!")
        start = time.time()
        for n in range(PROCESSES):
            p = multiprocessing.Process(target=process_txn, args=(task_queue,))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()

        print(f"Time taken = {time.time() - start:.10f}")
        time.sleep(60)
if __name__ == "__main__":
    run()