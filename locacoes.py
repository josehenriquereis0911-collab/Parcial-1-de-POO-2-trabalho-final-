from PySide6.QtWidgets import (
    QDialog, QLabel, QTableWidget, QTableWidgetItem, QPushButton, 
    QHBoxLayout, QVBoxLayout, QComboBox, QSpinBox, QFormLayout, 
    QDialogButtonBox, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt
from api_client import get_clientes, get_filmes, get_locacoes, post_locacao, put_devolver

class DialogoNovaLocacao(QDialog):
    def __init__(self, janela_principal, filme_preselecionado=None):
        super().__init__(janela_principal)
        self.janela_principal = janela_principal

        self.setWindowTitle("Nova Locação")
        self.resize(450, 260)

        self.combo_cliente = QComboBox()
        clientes = get_clientes()
        for cliente in clientes:
            self.combo_cliente.addItem(
                f"{cliente['nome']} - CPF: {cliente['cpf']}",
                cliente['id']
            )

        self.combo_filme = QComboBox()
        filmes = get_filmes()
        for filme in filmes:
            if filme['quantidade'] > 0:
                self.combo_filme.addItem(
                    f"{filme['titulo']} - disponíveis: {filme['quantidade']}",
                    filme['id']
                )

        if filme_preselecionado is not None:
            indice = self.combo_filme.findData(filme_preselecionado['id'])
            if indice >= 0:
                self.combo_filme.setCurrentIndex(indice)

        self.campo_dias = QSpinBox()
        self.campo_dias.setMinimum(1)
        self.campo_dias.setMaximum(30)
        self.campo_dias.setValue(7)

        formulario = QFormLayout()
        formulario.addRow("Cliente:", self.combo_cliente)
        formulario.addRow("Filme:", self.combo_filme)
        formulario.addRow("Prazo (dias):", self.campo_dias)

        botoes = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        botoes.accepted.connect(self.accept)
        botoes.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(formulario)
        layout.addWidget(botoes)
        self.setLayout(layout)

    def obter_dados(self):
        return {
            "id_cliente": self.combo_cliente.currentData(),
            "id_filme": self.combo_filme.currentData(),
            "dias": self.campo_dias.value()
        }


class DialogoLocacoes(QDialog):
    def __init__(self, janela_principal):
        super().__init__(janela_principal)
        self.janela_principal = janela_principal

        self.setWindowTitle("Locações")
        self.resize(900, 480)

        titulo = QLabel("Gerenciamento de Locações")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; padding: 8px;")

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(8)
        self.tabela.setHorizontalHeaderLabels([
            "ID", "Cliente", "Filme", "Classificação", "Data da locação", "Devolução prevista", "Status", "CPF"
        ])
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        botao_nova = QPushButton("Nova locação")
        botao_devolver = QPushButton("Registrar devolução")
        botao_fechar = QPushButton("Fechar")

        layout_botoes = QHBoxLayout()
        layout_botoes.addWidget(botao_nova)
        layout_botoes.addWidget(botao_devolver)
        layout_botoes.addStretch()
        layout_botoes.addWidget(botao_fechar)

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addWidget(self.tabela)
        layout.addLayout(layout_botoes)
        self.setLayout(layout)

        botao_nova.clicked.connect(self.nova_locacao)
        botao_devolver.clicked.connect(self.registrar_devolucao)
        botao_fechar.clicked.connect(self.accept)

        self.atualizar_tabela()

    def showEvent(self, event):
        super().showEvent(event)
        self.atualizar_tabela()

    def atualizar_tabela(self):
        self.tabela.setRowCount(0)
        locacoes = get_locacoes()

        for locacao in locacoes:
            linha = self.tabela.rowCount()
            self.tabela.insertRow(linha)

            status = "Devolvido" if locacao['devolvida'] else "Em aberto"

            self.tabela.setItem(linha, 0, QTableWidgetItem(str(locacao['id'])))
            self.tabela.setItem(linha, 1, QTableWidgetItem(locacao['cliente']))
            self.tabela.setItem(linha, 2, QTableWidgetItem(locacao['filme']))
            self.tabela.setItem(linha, 3, QTableWidgetItem(locacao['classificacao']))
            self.tabela.setItem(linha, 4, QTableWidgetItem(locacao['data_locacao']))
            self.tabela.setItem(linha, 5, QTableWidgetItem(locacao['data_prevista']))
            self.tabela.setItem(linha, 6, QTableWidgetItem(status))
            self.tabela.setItem(linha, 7, QTableWidgetItem(locacao['cpf']))

    def nova_locacao(self):
        self.janela_principal.iniciar_nova_locacao()
        self.atualizar_tabela()

    def registrar_devolucao(self):
        linha = self.tabela.currentRow()
        if linha < 0:
            QMessageBox.warning(self, "Nenhuma locação selecionada", "Selecione uma locação para registrar a devolução.")
            return

        id_locacao = int(self.tabela.item(linha, 0).text())
        status_atual = self.tabela.item(linha, 6).text()

        if status_atual == "Devolvido":
            QMessageBox.information(self, "Locação encerrada", "Essa locação já foi devolvida.")
            return

        resposta = QMessageBox.question(
            self, "Confirmar devolução", "Deseja registrar a devolução deste filme?",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            if put_devolver(id_locacao):
                self.atualizar_tabela()
                self.janela_principal.atualizar_tabela()
                QMessageBox.information(self, "Sucesso", "Devolução registrada e estoque atualizado.")
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível registrar a devolução.")