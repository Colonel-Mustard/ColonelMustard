import BasicBot


def main():
    cm = BasicBot.BasicBot()
    cm.do_login()
    cm.update_state()

    # Show some resource data
    print("[*] Village iron:", cm.state['village']['iron'])
    print("[*] Village stone:", cm.state['village']['stone'])
    print("[*] Village wood:", cm.state['village']['wood'])


if __name__ == "__main__":
    main()