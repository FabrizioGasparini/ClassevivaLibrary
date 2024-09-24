from classeviva import User, RequestURLs

utente = User("G10409310F", "Fabrizio2008#")
utente.login()
#subjects = utente.request(RequestURLs.AGENDA_URL, ("20240919", "20240925"))
#utente.print_prettify_output(subjects)

azioni = {"bacheca": RequestURLs.NOTICE_BOARD_URL, "materie": RequestURLs.SUBJECTS_URL, "lezioni": RequestURLs.TODAY_LESSONS_URL, "card": RequestURLs.CARD_URL, "libri":RequestURLs.SCHOOLBOOKS_URL}

inp = " "
while inp != "":
    inp = input("Azione: ")
    richiesta = utente.request(azioni[inp])
    utente.print_prettify_output(richiesta)
    