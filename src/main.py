import coloredlogs

from server import APP

coloredlogs.install(fmt="%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s")

if __name__ == "__main__":
    APP.run()
