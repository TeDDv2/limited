import threading
import bot.main as bot
import buzzsneakers.main as buzzsneakers
import database.main as database
from buzzsneakers.start import Start

def main():

    database.connect()

    threading.Thread(target=Start).start()
    

if __name__ == "__main__":
    main()