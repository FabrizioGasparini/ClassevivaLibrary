from classeviva import User, RequestURLs

utente = User("G10409310F", "Fabrizio2008#")
utente.login()
subjects = utente.request(RequestURLs.AGENDA_URL, ("20240919", "20240925"))
utente.print_prettify_output(subjects)