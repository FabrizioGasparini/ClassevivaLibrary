import json

with open('orario.json', 'rb') as file:
    data = json.load(file)

classi = data["classi"]

giorni = ["lun", "mar", "mer", "gio", "ven", "sab"]

def new_class():
    classe = input("\n\n\n\nClasse: ")
    aula_default = input("Aula Default: ")
    output = {}
    lista_mat = []
    for giorno in giorni:
        output[giorno] = []
        materia = ""
        aula = ""
        ore = 0

        print("\n\n")
        print(giorno)

        while materia != None:
            mat = {}
            materia = input("\nMateria: ")
            if materia == "":
                materia = None
            else:
                insegnanti = []

                copiato = False
                for m in lista_mat:
                    if m["materia"] == materia:
                        print(m)
                        copia = input("Copiare? (t/i/n)").lower()
                        if copia == "t":
                            mat = m
                            copiato = True
                            break
                        elif copia == "i":
                            insegnanti = m["insegnanti"]
                            break
                        else:
                            break


                if not copiato:
                    if insegnanti == []:
                        insegnanti = input("Insegnanti: ").split(',')

                    aula = input("Aula: ")
                    if aula == "":
                        aula = aula_default

                    ore = input("Ore: ")
                    if ore == "":
                        ore = 1
                    else:
                        ore = (int)(ore)

                    mat = {"materia": materia, "insegnanti": insegnanti, "aula": aula, "durata": ore}
                    
                output[giorno].append(mat)
                lista_mat.append(mat)
                print("Materia Aggiunta!")

    return (classe, output)

continua = ""
while continua != None:
    classe, output = new_class()
    classi[classe] = output

    json_data = json.dumps({"classi": classi})

    with open('orario.json', 'w') as file:
        file.writelines(json_data)

    continua = input("Continuare? (S/N)").lower()
    if continua != "s":
        continua = None
