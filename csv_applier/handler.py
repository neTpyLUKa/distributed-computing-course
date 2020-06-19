import pandas as pd

from model import Product

data_path = "/csv_data/"


def handle_message(ch, method, properties, body):
    filename = body.decode("utf-8")
    path = data_path + filename
    for df in pd.read_csv(path, sep=',', header=None, chunksize=1000):
        print("Applying...")
        df.apply(lambda line: Product.insert(uniq_id=line[0], title=line[1], category=line[8]), axis=1)
        Product.commit()
    print("Done")

