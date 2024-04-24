from prefect import flow


@flow(name="hliluya")
def hello():
    print("Hello, World!")

if __name__ == "__main__":
    hello()