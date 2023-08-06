import mmtapi


def main():
     t = mmtapi.Target(token='0f3732fcfb1c8577c390e71a176f3c8f', targetid=6302)
     t.upload_finder('M51.jpg')

main()
