import mynetwork


def deep_sleep():
    print("bye")
    from powermgm import deep_sleep
    deep_sleep()


def ota_check():
    import otapromoter
    try:
        from machine import reset
    except:
        from moc.machine import reset
    try:
        promoter = otapromoter.OTAPromoter('http://192.168.0.10:9090')
        if promoter.check_and_update():
            reset()
    except otapromoter.OTAException as e:
        print(e)
        return
    except OSError as e:
        print(e)
        return


def on_hard_reset():
    try:
        import utime as time
    except:
        import time

    try:
        print('powered on or hard reset, wait {} sec before start'.format(5, 'sec before start'))
        time.sleep(5)  # wait to firmware update
    except KeyboardInterrupt:
        print("key interrupt")
        import sys
        sys.exit()

    mynetwork.connect_and_wait()
    if not mynetwork.is_connected():
        print("failed to connect to net")
        return

    ota_check()


def gc():
    import gc
    gc.collect()


def main():
    try:
        import powermgm
        if not powermgm.is_woke_from_deep_sleep():
            on_hard_reset()
        mynetwork.connect_and_wait()
        if mynetwork.is_connected():
            import app
            app.on_wake_up()
    except mynetwork.WifiError as e:
        print(str(e))

    # deep_sleep()


if __name__ == '__main__':
    main()
