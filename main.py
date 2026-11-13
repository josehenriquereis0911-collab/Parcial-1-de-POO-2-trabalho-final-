from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, 
    QWidget, QLabel, QToolBar, QLineEdit, QTableWidget, QTableWidgetItem, 
    QMessageBox, QHeaderView, QGroupBox
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt,QTimer

from filmes import DialogoCadastroFilme
from clientes import JanelaClientes
from locacoes import DialogoLocacoes, DialogoNovaLocacao
from api_client import get_filmes, post_filme, delete_filme, post_locacao, get_clientes

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Locadora de Filmes - Inhuma")
        self.resize(950, 600)

        self.criar_menu()
        self.criar_barra_ferramentas()
        self.criar_interface()
        self.atualizar_tabela()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_tabela)
        

       

    def showEvent(self, event):
        super().showEvent(event)
        self.atualizar_tabela()

    def criar_menu(self):
        menu_barra = self.menuBar()

        menu_arquivo = menu_barra.addMenu("Arquivo")
        menu_cadastros = menu_barra.addMenu("Cadastros")
        menu_ajuda = menu_barra.addMenu("Ajuda")

        acao_novo_filme = QAction("Novo filme", self)
        acao_novo_filme.setShortcut("Ctrl+N")
        acao_novo_filme.triggered.connect(self.abrir_cadastro_filme)

        acao_sair = QAction("Sair", self)
        acao_sair.setShortcut("Ctrl+Q")
        acao_sair.triggered.connect(self.close)

        acao_clientes = QAction("Clientes", self)
        acao_clientes.triggered.connect(self.abrir_clientes)

        acao_locacoes = QAction("Locações", self)
        acao_locacoes.triggered.connect(self.abrir_locacoes)

        acao_sobre = QAction("Sobre o sistema", self)
        acao_sobre.triggered.connect(self.mostrar_sobre)

        menu_arquivo.addAction(acao_novo_filme)
        menu_arquivo.addSeparator()
        menu_arquivo.addAction(acao_sair)

        menu_cadastros.addAction(acao_novo_filme)
        menu_cadastros.addAction(acao_clientes)
        menu_cadastros.addAction(acao_locacoes)

        menu_ajuda.addAction(acao_sobre)

    def criar_barra_ferramentas(self):
        barra = QToolBar("Barra de ferramentas")
        barra.setMovable(False)
        self.addToolBar(barra)

        acao_filmes = QAction("Novo Filme", self)
        acao_filmes.triggered.connect(self.abrir_cadastro_filme)

        acao_clientes = QAction("Clientes", self)
        acao_clientes.triggered.connect(self.abrir_clientes)

        acao_locacoes = QAction("Locações", self)
        acao_locacoes.triggered.connect(self.abrir_locacoes)

        acao_excluir = QAction("Excluir Filme", self)
        acao_excluir.triggered.connect(self.excluir_filme)

        acao_sair = QAction("Sair", self)
        acao_sair.triggered.connect(self.close)

        barra.addAction(acao_filmes)
        barra.addAction(acao_clientes)
        barra.addAction(acao_locacoes)
        barra.addSeparator()
        barra.addAction(acao_excluir)
        barra.addSeparator()
        barra.addAction(acao_sair)

    def criar_interface(self):
        central = QWidget()
        layout_principal = QVBoxLayout()

        titulo = QLabel("Locadora de Filmes - Inhuma")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px;")

        descricao = QLabel("Cadastre, consulte e gerencie os filmes disponíveis.")
        descricao.setAlignment(Qt.AlignCenter)

        grupo_pesquisa = QGroupBox("Pesquisa de filmes")
        layout_pesquisa = QHBoxLayout()

        self.campo_pesquisa = QLineEdit()
        self.campo_pesquisa.setPlaceholderText("Digite o título ou diretor para pesquisar.")

        botao_pesquisar = QPushButton("Pesquisar")
        botao_limpar = QPushButton("Limpar pesquisa")

        layout_pesquisa.addWidget(self.campo_pesquisa)
        layout_pesquisa.addWidget(botao_pesquisar)
        layout_pesquisa.addWidget(botao_limpar)
        grupo_pesquisa.setLayout(layout_pesquisa)

        self.tabela_filmes = QTableWidget()
        self.tabela_filmes.setColumnCount(6)
        self.tabela_filmes.setHorizontalHeaderLabels([
            "ID", "Título", "Gênero", "Classificação", "Diretor", "Quantidade"
        ])
        self.tabela_filmes.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela_filmes.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela_filmes.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela_filmes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout_botoes = QHBoxLayout()
        botao_novo = QPushButton("Cadastrar filme")
        botao_excluir = QPushButton("Excluir selecionado")
        botao_detalhes = QPushButton("Ver detalhes")
        botao_alugar = QPushButton("Alugar Filme")
       


        layout_botoes.addWidget(botao_novo)
        layout_botoes.addWidget(botao_excluir)
        layout_botoes.addWidget(botao_detalhes)
        layout_botoes.addWidget(botao_alugar)
        layout_principal.addWidget(titulo)
        layout_principal.addWidget(descricao)
        layout_principal.addWidget(grupo_pesquisa)
        layout_principal.addWidget(self.tabela_filmes)
        layout_principal.addLayout(layout_botoes)

        central.setLayout(layout_principal)
        self.setCentralWidget(central)

        botao_novo.clicked.connect(self.abrir_cadastro_filme)
        botao_excluir.clicked.connect(self.excluir_filme)
        botao_detalhes.clicked.connect(self.mostrar_detalhes)
        botao_alugar.clicked.connect(self.alugar_filme)
        botao_pesquisar.clicked.connect(self.pesquisar_filmes)
        botao_limpar.clicked.connect(self.limpar_pesquisa)
        self.campo_pesquisa.textChanged.connect(self.pesquisar_filmes)
        self.tabela_filmes.cellDoubleClicked.connect(self.mostrar_detalhes)

    def abrir_cadastro_filme(self):
        dialogo = DialogoCadastroFilme(self)
        if dialogo.exec():
            dados = dialogo.obter_dados()
            if post_filme(dados):
                self.atualizar_tabela()
                QMessageBox.information(self, "Cadastro realizado", "Filme cadastrado com sucesso.")
                self.statusBar().showMessage("Novo filme cadastrado.")
            else:
                QMessageBox.critical(self, "Erro", "Erro ao cadastrar o filme na API.")

    def atualizar_tabela(self, filmes=None):
        if filmes is None:
            filmes = get_filmes()

        if not isinstance(filmes, list):
            filmes = []

        self.tabela_filmes.setRowCount(0)
        for filme in filmes:
            linha = self.tabela_filmes.rowCount()
            self.tabela_filmes.insertRow(linha)

            self.tabela_filmes.setItem(linha, 0, QTableWidgetItem(str(filme['id'])))
            self.tabela_filmes.setItem(linha, 1, QTableWidgetItem(filme['titulo']))
            self.tabela_filmes.setItem(linha, 2, QTableWidgetItem(filme.get('genero', '')))
            self.tabela_filmes.setItem(linha, 3, QTableWidgetItem(filme.get('classificacao', '')))
            self.tabela_filmes.setItem(linha, 4, QTableWidgetItem(filme.get('diretor', '')))
            self.tabela_filmes.setItem(linha, 5, QTableWidgetItem(str(filme['quantidade'])))

    def alugar_filme(self):
        linha = self.tabela_filmes.currentRow()
        if linha < 0:
            QMessageBox.warning(self, "Nenhum filme selecionado", "Selecione um filme na tabela para alugar.")
            return

        id_filme = int(self.tabela_filmes.item(linha, 0).text())
        filmes = get_filmes()
        filme_selecionado = next((f for f in filmes if f['id'] == id_filme), None)

        if not filme_selecionado:
            return

        if filme_selecionado['quantidade'] <= 0:
            QMessageBox.warning(self, "Filme esgotado", "Não há unidades disponíveis desse filme.")
            return

        self.iniciar_nova_locacao(filme_selecionado)

    def iniciar_nova_locacao(self, filme_preselecionado=None):
        clientes = get_clientes()
        if not clientes:
            QMessageBox.warning(self, "Nenhum cliente cadastrado", "Cadastre pelo menos um cliente antes de realizar uma locação.")
            return False

        filmes = get_filmes()
        filmes_disponiveis = [f for f in filmes if f['quantidade'] > 0]
        if not filmes_disponiveis:
            QMessageBox.warning(self, "Sem filmes disponíveis", "Não há filmes disponíveis para locação.")
            return False

        dialogo = DialogoNovaLocacao(self, filme_preselecionado)
        if not dialogo.exec():
            return False

        dados = dialogo.obter_dados()
        if post_locacao(dados):
            self.atualizar_tabela()
            QMessageBox.information(self, "Locação realizada", "Locação registrada com sucesso na API.")
            self.statusBar().showMessage("Nova locação registrada.")
            return True
        else:
            QMessageBox.critical(self, "Erro", "Erro ao registrar locação.")
            return False

    def pesquisar_filmes(self):
        texto = self.campo_pesquisa.text().strip().lower()
        filmes = get_filmes()

        if texto:
            filmes = [
                f for f in filmes
                if texto in f['titulo'].lower() or texto in f['diretor'].lower()
            ]

        self.atualizar_tabela(filmes)
        self.statusBar().showMessage(f"{len(filmes)} filme(s) encontrado(s).")

    def limpar_pesquisa(self):
        self.campo_pesquisa.clear()
        self.atualizar_tabela()
        self.statusBar().showMessage("Pesquisa limpa.")

    def excluir_filme(self):
        linha = self.tabela_filmes.currentRow()
        if linha < 0:
            QMessageBox.warning(self, "Nenhum filme selecionado", "Selecione um filme na tabela para excluir.")
            return

        id_filme = int(self.tabela_filmes.item(linha, 0).text())
        titulo_filme = self.tabela_filmes.item(linha, 1).text()

        resposta = QMessageBox.question(
            self, "Confirmar exclusão", f"Deseja excluir o filme '{titulo_filme}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            if delete_filme(id_filme):
                self.atualizar_tabela()
                QMessageBox.information(self, "Filme excluído", "O filme foi excluído com sucesso.")
            else:
                QMessageBox.warning(self, "Erro", "Não é possível excluir um filme com histórico de locações associadas.")

    def mostrar_detalhes(self):
        linha = self.tabela_filmes.currentRow()
        if linha < 0:
            QMessageBox.information(self, "Detalhes", "Selecione um filme para visualizar os detalhes.")
            return

        id_filme = int(self.tabela_filmes.item(linha, 0).text())
        filmes = get_filmes()
        filme = next((f for f in filmes if f['id'] == id_filme), None)

        if filme:
            mensagem = (
                f"ID: {filme['id']}\n"
                f"Título: {filme['titulo']}\n"
                f"Gênero: {filme.get('genero', '')}\n"
                f"Classificação indicativa: {filme.get('classificacao', '')}\n"
                f"Diretor: {filme.get('diretor', '')}\n"
                f"Quantidade disponível: {filme['quantidade']}"
            )
            QMessageBox.information(self, "Detalhes do filme", mensagem)

    def abrir_clientes(self):
        self.janela_clientes = JanelaClientes(self)
        self.janela_clientes.show()

    def abrir_locacoes(self):
        dialogo = DialogoLocacoes(self)
        dialogo.exec()

    def mostrar_sobre(self):
        QMessageBox.about(
            self, "Sobre o sistema",
            "Locadora de Filmes - Inhuma\n\nSistema cliente-servidor desenvolvido em Python, PySide6 e Flask/Docker."
        )

    def keyPressEvent(self, evento):
        if evento.key() == Qt.Key_Delete:
            self.excluir_filme()
        elif evento.key() == Qt.Key_Escape:
            self.campo_pesquisa.clear()
        else:
            super().keyPressEvent(evento)

    def closeEvent(self, evento):
        resposta = QMessageBox.question(
            self, "Sair", "Deseja realmente sair do sistema?",
            QMessageBox.Yes | QMessageBox.No
        )
        if resposta == QMessageBox.Yes:
            evento.accept()
        else:
            evento.ignore()


if __name__ == "__main__":
    app = QApplication([])
    janela = JanelaPrincipal()
    janela.show()
    app.exec()