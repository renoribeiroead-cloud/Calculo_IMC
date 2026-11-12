# -*- coding: latin1 -*-

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Manipulador:
    def __init__(self, builder):
        self.builder = builder

        # Mapeando os campos de entrada e saída
        self.entry_nome = self.builder.get_object("entry_nome")
        self.entry_endereco = self.builder.get_object("entry_endereco")
        self.entry_altura = self.builder.get_object("entry_altura")
        self.entry_peso = self.builder.get_object("entry_peso")
        self.lbl_resultado = self.builder.get_object("lbl_resultado")

        # Conectando os eventos da janela e dos botões
        janela = self.builder.get_object("janela_imc")
        janela.connect("destroy", self.on_destroy)

        btn_calcular = self.builder.get_object("btn_calcular")
        btn_calcular.connect("clicked", self.on_calcular_clicked)

        btn_reiniciar = self.builder.get_object("btn_reiniciar")
        btn_reiniciar.connect("clicked", self.on_reiniciar_clicked)

        btn_sair = self.builder.get_object("btn_sair")
        btn_sair.connect("clicked", self.on_destroy)

    def on_destroy(self, *args):
        Gtk.main_quit()

    def on_calcular_clicked(self, button):
        try:
            nome = self.entry_nome.get_text().strip()
            endereco = self.entry_endereco.get_text().strip()

            # Substitui vírgula por ponto - formato brasileiro
            altura = float(self.entry_altura.get_text().replace(",", "."))
            peso_kg = float(self.entry_peso.get_text().replace(",", "."))

            if altura <= 0 or peso_kg <= 0:
                self.lbl_resultado.set_text("Altura e peso devem ser maiores que zero.")
                return

            imc = peso_kg / (altura ** 2)
            classificacao = self.classificar_imc(imc)

            # Monta o texto de exibição dentro do frame_resultado
            cabecalho = f"Paciente: {nome}\n" if nome else ""
            local = f"Endereço: {endereco}\n\n" if endereco else ("\n" if nome else "")

            texto_final = (
                f"{cabecalho}{local}"
                f"IMC: {imc:.2f} kg/m²\n"
                f"Classificação: {classificacao}"
            )

            self.lbl_resultado.set_text(texto_final)

        except ValueError:
            self.lbl_resultado.set_text("Erro: Preencha Altura e Peso com números válidos.")

    def on_reiniciar_clicked(self, button):
        # Limpa todas as caixas de texto
        self.entry_nome.set_text("")
        self.entry_endereco.set_text("")
        self.entry_altura.set_text("")
        self.entry_peso.set_text("")
        self.lbl_resultado.set_text("Resultado")
        self.entry_nome.grab_focus()  # Volta o cursor para o campo Nome

    def classificar_imc(self, imc):
        if imc < 18.5:
            return "Abaixo do peso"
        elif imc < 25:
            return "Peso normal"
        elif imc < 30:
            return "Sobrepeso"
        elif imc < 35:
            return "Obesidade Grau I"
        elif imc < 40:
            return "Obesidade Grau II"
        else:
            return "Obesidade Grau III"


# Inicialização
builder = Gtk.Builder()
builder.add_from_file("calculo_imc.glade")

app = Manipulador(builder)

janela = builder.get_object("janela_imc")
janela.show_all()

Gtk.main()
