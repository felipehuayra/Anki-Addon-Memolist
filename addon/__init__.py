# Progressive Cloze - add-on que instala o tipo de nota "Progressive Cloze" no Anki.
# O cartão em si é só HTML/CSS/JS (pasta templates/); este arquivo apenas cria o tipo de nota.

import os

from aqt import mw
from aqt.qt import QAction
from aqt.utils import showInfo

NOME_TIPO = "Progressive Cloze"
CAMPOS = ["Pergunta", "Itens", "Observações"]


def ler_arquivo(nome):
    # Lê um arquivo da pasta templates/ que fica ao lado deste arquivo.
    pasta = os.path.dirname(__file__)
    caminho = os.path.join(pasta, "templates", nome)
    with open(caminho, encoding="utf-8") as arquivo:
        return arquivo.read()


def instalar_tipo_de_nota():
    colecao = mw.col

    # Se o tipo de nota já existe, não cria de novo (evita duplicar ou sobrescrever).
    if colecao.models.by_name(NOME_TIPO):
        showInfo("O tipo de nota '" + NOME_TIPO + "' já existe nesta coleção.")
        return

    # 1) cria o tipo de nota vazio
    modelo = colecao.models.new(NOME_TIPO)

    # 2) adiciona os campos
    for nome_campo in CAMPOS:
        campo = colecao.models.new_field(nome_campo)
        colecao.models.add_field(modelo, campo)

    # 3) cria o cartão com a frente e o verso HTML
    cartao = colecao.models.new_template("Cartão 1")
    cartao["qfmt"] = ler_arquivo("front.html")  # frente
    cartao["afmt"] = ler_arquivo("back.html")  # verso
    colecao.models.add_template(modelo, cartao)

    # 4) define o estilo CSS
    modelo["css"] = ler_arquivo("style.css")

    # 5) salva na coleção
    colecao.models.add(modelo)

    showInfo("Tipo de nota '" + NOME_TIPO + "' instalado! Crie uma nota com ele para testar.")


# Cria o item "Instalar Progressive Cloze" no menu Ferramentas
acao = QAction("Instalar Progressive Cloze", mw)
acao.triggered.connect(instalar_tipo_de_nota)
mw.form.menuTools.addAction(acao)
