from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from rest_framework import viewsets
from .serializers import DashSerializer
from .forms import DashForm
from .models import User, DashModel
from django.db.models import Sum as Soma
from django.contrib import messages
from django.db.models import Sum, Min

import pandas as pd
import plotly.express as px


@method_decorator(login_required, name="dispatch")
class HomeView(TemplateView):
    def get(self, request):
        # template_name = "index.html"
        return render(request, "home.html")


class IndexView(TemplateView):
    def get(self, request):
        return render(request, "index.html")


def logoutView(request):
    messages.success(request, "Logout realizado!")
    logout(request)
    return redirect("/")


class ServicosView(TemplateView):
    def get(self, request):
        idUsuario = request.user.id

        if idUsuario is None:
            return redirect("/login/")
        else:
            return render(request, "servicos.html")


def LoginCadastroView(request):
    idUsuario = request.user.id
    if idUsuario is None:
        if "email" in request.POST.keys():
            entrar = True
        else:
            entrar = False

        if entrar:
            if request.method == "POST":
                Entraremail = request.POST["email"]
                password = request.POST["password"]
                user = authenticate(request, email=Entraremail, password=password)

                if user is not None:
                    login(request, user)
                    return redirect("/home")
                elif user is None:
                    return render(
                        request, "login.html", {"errors": ["Email ou senha inválidos."]}
                    )
            return render(request, "login.html")

        if "CadastroEmail" in request.POST.keys():
            cadastrar = True
        else:
            cadastrar = False

        if cadastrar:
            if request.method == "POST":
                cadastroEmail = request.POST["CadastroEmail"]
                InsertPassword = request.POST["CadastroPassword"]
                confirmPassword = request.POST["ConfirmCadastroPassword"]
                first_name = request.POST["first_name"]
                last_name = request.POST["last_name"]

                if InsertPassword != confirmPassword:
                    return render(
                        request, "login.html", {"errors": ["Senhas divergentes."]}
                    )

                user = User.objects.filter(email=cadastroEmail).first()
                if user:
                    return render(
                        request, "login.html", {"errors": ["Email já cadastrado."]}
                    )

                User.objects.create_user(
                    email=cadastroEmail,
                    password=InsertPassword,
                    first_name=first_name,
                    last_name=last_name,
                )
            return render(request, "login.html")
    if idUsuario:
        return redirect("/")
    return render(request, "login.html")


class DashModificar(TemplateView):
    def get(self, request):
        idUsuario = request.user.id
        label = request.GET.get("label", "Quantidade de Alface")
        title = request.GET.get("title", "Quantidade de Alface colhido")
        # parametroX = request.GET.get('parametroX', 'dataInspecao')
        parametroY = request.GET.get("parametroY", "qtdeAlfaceColhida")

        if idUsuario is None:
            return redirect("/login/")
        else:
            if len(DashModel.objects.filter(idCliente=request.user.id)) > 0:
                # print(idUsuario)
                df = pd.DataFrame(
                    list(
                        DashModel.objects.values("dataInspecao", parametroY).filter(
                            idCliente=request.user.id
                        )
                    )
                )

                line_fig = px.line(
                    df,
                    x="dataInspecao",
                    y=parametroY,
                    labels={"dataInspecao": "Data", parametroY: label},
                    title=title,
                )
                bar_fig = px.bar(
                    df,
                    x="dataInspecao",
                    y=parametroY,
                    labels={"dataInspecao": "Data", parametroY: label},
                    title=title,
                )

                quantity_min = "f{parametroY}__min"
                initial_quantity = (
                    DashModel.objects.filter(idCliente=request.user.id)
                    .aggregate(Min(parametroY))
                    .get(f"{parametroY}__min", 0)
                    or 0
                )

                # Obter a quantidade total de alface colhido
                total_quantity = (
                    DashModel.objects.filter(idCliente=request.user.id)
                    .aggregate(Sum(parametroY))
                    .get(f"{parametroY}__sum", 0)
                    or 0
                )

                last_record = DashModel.objects.filter(
                    idCliente=request.user.id
                ).latest("dataInspecao")
                last_quantity = getattr(last_record, parametroY, 0)

                chart_line = line_fig.to_html()
                chart_bar = bar_fig.to_html()

                contexto = {
                    "dash_line": chart_line,
                    "dash_bar": chart_bar,
                    "title": title,
                    "dado_inicio_label": label,
                    "quantidade_inicial": initial_quantity,
                    "quantidade_total": total_quantity,
                    "quantidade_final": last_quantity,
                }
                return render(request, "dash.html", contexto)
            else:
                sem_info = "Sem informações no banco para este usuário"
                contexto = {"dash_line": sem_info, "dash_bar": sem_info}
                return render(request, "dash.html", contexto)


class DashAlfacePadrão(TemplateView):
    def get(self, request):
        if len(DashModel.objects.filter(idCliente=1)) > 0:
            df = pd.DataFrame(
                list(
                    DashModel.objects.values(
                        "dataInspecao", "qtdeAlfaceColhida"
                    ).filter(idCliente=1)
                )
            )

            line_fig = px.line(
                df,
                x="dataInspecao",
                y="qtdeAlfaceColhida",
                labels={
                    "dataInspecao": "Data",
                    "qtdeAlfaceColhida": "Quantidade de Alface",
                },
                title="Quantidade de Alface Colhido | Data",
            )
            bar_fig = px.bar(
                df,
                x="dataInspecao",
                y="qtdeAlfaceColhida",
                labels={
                    "dataInspecao": "Data",
                    "qtdeAlfaceColhida": "Quantidade de Alface",
                },
                title="Quantidade de Alface Colhido | Data",
            )

            chart_line = line_fig.to_html()
            chart_bar = bar_fig.to_html()

            contexto = {"dash_line": chart_line, "dash_bar": chart_bar}
            return render(request, "dashpadrao.html", contexto)
        else:
            sem_info = "Sem informações no banco para este usuário"
            contexto = {"dash_line": sem_info, "dash_bar": sem_info}
            return render(request, "dashpadrao.html", contexto)


class CadastroDash(TemplateView):
    def get(self, request):
        idUsuario = request.user.id

        if idUsuario is None:
            return redirect("/login/")
        else:
            form = DashForm()
            contexto = {"form": form}
            return render(request, "registro.html", contexto)

    def post(self, request):
        data_atual = datetime.now()
        data_atual_str = data_atual.strftime("%Y-%m-%d")

        somaAlface = DashModel.objects.filter(idCliente=request.user.id).aggregate(
            Soma("qtdeAlfaceColhida")
        )
        somaAlfaceInt = 0
        for chave in somaAlface:
            somaAlfaceInt = somaAlface[chave]

        if request.method == "POST":
            nomeCliente = request.user
            capacidadeTanque = 900
            idCliente = request.user.id
            idTanque = 1
            qtdeAlimentoPeixe = request.POST.get("qtdeAlimentoPeixe")
            limpezaAgua = request.POST.get("limpezaAgua")
            if int(request.POST.get("qtdePeixesTanque")) < 40:
                peixeMorto = "Sim"
            elif int(request.POST.get("qtdePeixesTanque")) >= 40:
                peixeMorto = "Não"
            statusTanque = request.POST.get("statusTanque")
            valorAlface = request.POST.get("valorAlface")
            valorPeixe = request.POST.get("valorPeixe")
            vendaPeixe = float(request.POST.get("qtdeVendaPeixe", 0.0) or 0.0)
            vendaAlface = float(request.POST.get("qtdeVendaAlface", 0.0) or 0.0)
            dataInspecao = request.POST.get("dataInspecao")
            qtdeAgua = request.POST.get("qtdeAgua")
            qtdeAlfaceColhida = request.POST.get("qtdeAlfaceColhida")
            qtdeAlfacePlantada = request.POST.get("qtdeAlfacePlantada")
            if somaAlfaceInt == None:
                qtdeAlfaceTotal = qtdeAlfaceColhida
            elif somaAlfaceInt != None:
                qtdeAlfaceTotal = somaAlfaceInt + int(qtdeAlfaceColhida)
            qtdePeixesTanque = request.POST.get("qtdePeixesTanque")

            # if len(DashModel.objects.filter(idCliente = request.user.id)) > 0:
            if (
                dataInspecao == data_atual_str
                and len(
                    DashModel.objects.values("dataInspecao").filter(
                        idCliente=request.user.id
                    )
                )
                >= 1
            ):
                print("Data igual teste" + data_atual_str + "  " + dataInspecao)
                DashModel.objects.filter(
                    idCliente=request.user.id, dataInspecao=data_atual_str
                ).update(
                    nomeCliente=str(nomeCliente),
                    idCliente=idCliente,
                    capacidadeTanque=capacidadeTanque,
                    idTanque=idTanque,
                    qtdeAlimentoPeixe=qtdeAlimentoPeixe,
                    limpezaAgua=limpezaAgua,
                    peixeMorto=peixeMorto,
                    statusTanque=statusTanque,
                    valorAlface=valorAlface,
                    valorPeixe=valorPeixe,
                    qtdeVendaPeixe=vendaPeixe,
                    qtdeVendaAlface=vendaAlface,
                    dataInspecao=dataInspecao,
                    qtdeAgua=qtdeAgua,
                    qtdeAlfaceColhida=qtdeAlfaceColhida,
                    qtdeAlfacePlantada=qtdeAlfacePlantada,
                    qtdePeixesTanque=qtdePeixesTanque,
                )
            elif (
                dataInspecao == data_atual_str
                and len(
                    DashModel.objects.values("dataInspecao").filter(
                        idCliente=request.user.id
                    )
                )
                == 0
            ):
                DashModel.objects.create(
                    nomeCliente=nomeCliente,
                    idCliente=idCliente,
                    capacidadeTanque=capacidadeTanque,
                    idTanque=idTanque,
                    qtdeAlimentoPeixe=qtdeAlimentoPeixe,
                    limpezaAgua=limpezaAgua,
                    peixeMorto=peixeMorto,
                    statusTanque=statusTanque,
                    valorAlface=valorAlface,
                    valorPeixe=valorPeixe,
                    qtdeVendaPeixe=vendaPeixe,
                    qtdeVendaAlface=vendaAlface,
                    dataInspecao=dataInspecao,
                    qtdeAgua=qtdeAgua,
                    qtdeAlfaceColhida=qtdeAlfaceColhida,
                    qtdeAlfacePlantada=qtdeAlfacePlantada,
                    qtdePeixesTanque=qtdePeixesTanque,
                )
            else:
                DashModel.objects.create(
                    nomeCliente=nomeCliente,
                    idCliente=idCliente,
                    capacidadeTanque=capacidadeTanque,
                    idTanque=idTanque,
                    qtdeAlimentoPeixe=qtdeAlimentoPeixe,
                    limpezaAgua=limpezaAgua,
                    peixeMorto=peixeMorto,
                    statusTanque=statusTanque,
                    valorAlface=valorAlface,
                    valorPeixe=valorPeixe,
                    qtdeVendaPeixe=vendaPeixe,
                    qtdeVendaAlface=vendaAlface,
                    dataInspecao=dataInspecao,
                    qtdeAgua=qtdeAgua,
                    qtdeAlfaceColhida=qtdeAlfaceColhida,
                    qtdeAlfacePlantada=qtdeAlfacePlantada,
                    qtdePeixesTanque=qtdePeixesTanque,
                )
            return redirect("/home")


def ContatoView(request):
    return render(request, "contato.html")


def PerfilView(request):
    loggedUserId = request.user.id
    userInfo = User.objects.get(id=loggedUserId)

    if request.method == "POST":
        userInfo.first_name = request.POST.get("first-name")
        userInfo.last_name = request.POST.get("last-name")
        userInfo.email = request.POST.get("email")
        userInfo.save()
        return redirect("/perfil")

    contexto = {
        "firstName": userInfo.get_short_name(),
        "lastName": userInfo.get_last_name(),
        "email": userInfo.get_email(),
    }
    return render(request, "perfil.html", contexto)


class DashModelViewSet(viewsets.ModelViewSet):
    queryset = DashModel.objects.all()
    serializer_class = DashSerializer
