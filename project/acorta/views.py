from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .models import Web
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

FORMULARIO = """
    <form action="" method="POST">
        URL que quieres acortar:<br>
        <input type="text" name="url" value="gsyc.urjc.es"/>
        <br><br>
        <input type="submit" value="Acortar URL">
    </form>
"""

INICIO_REDIR = "<br><br><br><a href='http://localhost:8000/'>Pagina principal</a>"

@csrf_exempt
def barra(request):
    if request.method == "GET":
        respuesta = "<h1>Bienvenido al acortador de URLs.</h1>"
        respuesta += FORMULARIO + "<br>"
        respuesta += "Listado de URLs almacenadas:<br>"

        webs = Web.objects.all() #lista de objetos tipo Web
        respuesta += "<ul>"
        for web in webs:
            respuesta += ("<li><a href='" + str(web.id)+ "'>" + web.address + "</a>" +
                            " --> " + "<a href='" + str(web.id)+ "'>" + str(web.id) + "</a>")
        respuesta += "</ul>"
        return HttpResponse(respuesta)

    elif request.method == "POST":
        url = request.POST["url"]

        #form vacio (sin QS)
        if url == "":
            respuesta = "ERROR: Metodo POST sin QS. No se ha introducido ninguna url."
            respuesta += INICIO_REDIR
            return HttpResponseNotFound(respuesta)

        #form relleno
        else:
            if not (url.startswith("http://") or (url.startswith("https://"))):
                url = "http://" + url

            try: #url ya esta en BD
                pagina = Web.objects.get(address=url)
                respuesta = "La url " + str(url) + " ya habia sido acortada y almacenada. <br><br>"
                respuesta += ("<a href='" + pagina.address + "'>" + str(pagina.id) + "</a>" +
                                " : " +
                                "<a href='" + pagina.address + "'>" + pagina.address + "</a>")
                respuesta += INICIO_REDIR
                return HttpResponse(respuesta)

            except Web.DoesNotExist: #url no esta en BD
                pagina = Web(address=url)
                pagina.save()

                respuesta = ("<a href='" + pagina.address + "'>" + str(pagina.id) + "</a>" +
                                " : " +
                                "<a href='" + pagina.address + "'>" + pagina.address + "</a>")
                respuesta += INICIO_REDIR
                return HttpResponse(respuesta)

    else:
        respuesta = "Not Found. Metodo incorrecto."
        respuesta += INICIO_REDIR
        return HttpResponseNotFound(respuesta)


def redirect(request, identificador):
    if identificador.isdigit(): #returns true if all characters in the string are digits

        try:
            pagina = Web.objects.get(id=int(identificador))
            return HttpResponseRedirect(pagina.address)

        except Web.DoesNotExist:
            respuesta = "ERROR: Recurso no disponible."
            respuesta += INICIO_REDIR
            return HttpResponseNotFound(respuesta)

    else:
        respuesta = "ERROR: Recurso debe ser un numero."
        respuesta += INICIO_REDIR
        return HttpResponseNotFound(respuesta)
