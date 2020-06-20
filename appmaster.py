from master import Master


if __name__ == '__main__':
    master = Master()
    try:
        master.start()
    except KeyboardInterrupt:
        master.stop()
