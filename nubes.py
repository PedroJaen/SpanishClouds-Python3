import datetime
import time
import urllib.request  # descargar archivos
import imageio  # crear gifs
import os  # borrar archivos


# imprimir bonito
def recuadro(texto, decoracion1, decoracion2):
    print()
    tamano = len(texto) + 10
    print(decoracion1 * tamano)
    print(decoracion2 + "    " + texto + "    " + decoracion2)
    print(decoracion1 * tamano, end="\n\n")


# comprobamos que la fecha esta en el rango correcto
def validaFecha(choosed_day, today, last_day):
    if today <= choosed_day and last_day >= choosed_day:
        return False
    else:
        return True


def getImages(choosed_day, hour="none"):
    horas_validas = ["0600", "0900", "1200", "1500", "1800", "2100", "0000"]
    nombres_archivos = ["1.jpg", "2.jpg", "3.jpg",
                        "4.jpg", "5.jpg", "6.jpg", "7.jpg"]
    d = str(choosed_day).split('-')
    copia = d  # mantenemos la lista original para el gif
    # colocamos el contador de la lista en la posicion adecuada
    contador = 0
    if hour is not "none":
        for x in range(6):
            if hour > horas_validas[x] and hour < horas_validas[x + 1]:
                contador = x
    # descargamos las fotos
    print("\nDescargando fotos", end="")
    for x in range(contador, 7):
        if x == 6:  # pala las 00 hay que coger el del dia siguiente
            one_day = datetime.timedelta(days=1)
            choosed_day = choosed_day + one_day
            d = str(choosed_day).split('-')
        url = "https://maps.eltiempo.es/eltiempo/maps/" + \
            d[0] + "/" + d[1] + "/" + d[2] + "/weather/cloud/spain/680x537/spain-weather-cloud-" + \
            d[0] + d[1] + d[2] + horas_validas[x] + ".jpg"
        urllib.request.urlretrieve(url, nombres_archivos[x])
        print(".", end="")
    print()
    # creamos el gif y borramos la imagen usada
    archivo = "_".join(copia) + "_" + horas_validas[contador] + ".gif"
    print("Creando animacion", end="")
    kwargs = {'duration': 0.5}  # velocidad del gif
    writer = imageio.get_writer(
        archivo, mode='I', **kwargs)  # abrimos el flujo
    for x in range(contador, 7):
        image = imageio.imread(nombres_archivos[x])  # leemos el archivo
        writer.append_data(image)  # mandamos al flujo
        os.remove(nombres_archivos[x])  # borrar imagen
        print(".", end="")
    print()


recuadro("Aplicacion para obtener el tiempo", "#", "#")
today = datetime.date.today()  # obtenemos el dia de hoy
hour = time.strftime("%H") + "00"  # obtenemos la hora UTC
four_days = datetime.timedelta(days=4)  # creamos un dia+4
last_day = today + four_days  # sumamos 4 dias a hoy
correcto = True
choosed_day = ""
while correcto:
    # pedimos los datos
    year = input("Indique el año: ").strip()
    month = input("Indique el mes: ").strip()
    day = input("Indique el dia: ").strip()
    # si solo nos da 1 digito para mes/dia, añadimos 0 delante
    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day
    # si introdujo mal algun dato, saltara el try/except y asi ahorramos comprobaciones
    try:
        choosed_day = datetime.date(int(year), int(month), int(day))
        correcto = validaFecha(choosed_day, today, last_day)
        if correcto:
            print("La fecha tiene que comprenderse entre", today, "y", last_day)
    except ValueError:
        print("La fecha tiene que seguir el formato YYYY/MM/DD")
if choosed_day == today:
    getImages(choosed_day, hour)
else:
    getImages(choosed_day)
recuadro("Gif generado!", "#", "#")
