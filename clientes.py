from PySide6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, 
    QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, 
    QFormLayout, QHeaderView, QDialogButtonBox
)
from PySide6.QtCore import Qt
from api_client import get_clientes, post_cliente, delete_cliente

class DialogoCadastroCliente(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cadastrar Cliente")
        self.resize(420, 250)

        self.campo_nome = QLineEdit()
        self.campo_cpf = QLineEdit()
        self.campo_telefone = QLineEdit()
        self.campo_email = QLineEdit()

        formulario = QFormLayout()
        formulario.addRow("Nome:", self.campo_nome)
        formulario.addRow("CPF:", self.campo_cpf)
        formulario.addRow("Telefone:", self.campo_telefone)
        formulario.addRow("E-mail:", self.campo_email)

        # CORREÇÃO AQUI: Instanciação limpa da QDialogButtonBox
        botoes = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        botoes.accepted.connect(self.validar_dados)
        botoes.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(formulario)
        layout.addWidget(botoes)
        self.setLayout(layout)

    def validar_dados(self):
        nome = self.campo_nome.text().strip()
        cpf = self.campo_cpf.text().strip()

        if not nome:
            QMessageBox.warning(self, "Campo obrigatório", "Informe o nome do cliente.")
            self.campo_nome.setFocus()
            return

        if not cpf:
            QMessageBox.warning(self, "Campo obrigatório", "Informe o CPF do cliente.")
            self.campo_cpf.setFocus()
            return

        # Verifica se o CPF já existe na API
        clientes = get_clientes()
        if any(c.get("cpf") == cpf for c in clientes):
            QMessageBox.warning(self, "CPF já cadastrado", "Já existe um cliente cadastrado com esse CPF.")
            self.campo_cpf.setFocus()
            return

        self.accept()

    def obter_dados(self):
        return {
            "nome": self.campo_nome.text().strip(),
            "cpf": self.campo_cpf.text().strip(),
            "telefone": self.campo_telefone.text().strip(),
            "email": self.campo_email.text().strip()
        }


class JanelaClientes(QMainWindow):
    def __init__(self, janela_principal):
        super().__init__()
        self.janela_principal = janela_principal

        self.setWindowTitle("Clientes")
        self.resize(800, 450)

        central = QWidget()
        titulo = QLabel("Gerenciamento de Clientes")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; padding: 8px;")

        self.campo_pesquisa = QLineEdit()
        self.campo_pesquisa.setPlaceholderText("Pesquisar por nome ou CPF...")

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "Telefone", "E-mail"])
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        botao_novo = QPushButton("Cadastrar cliente")
        botao_excluir = QPushButton("Excluir selecionado")
        botao_fechar = QPushButton("Fechar")

        layout_botoes = QHBoxLayout()
        layout_botoes.addWidget(botao_novo)
        layout_botoes.addWidget(botao_excluir)
        layout_botoes.addStretch()
        layout_botoes.addWidget(botao_fechar)

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addWidget(self.campo_pesquisa)
        layout.addWidget(self.tabela)
        layout.addLayout(layout_botoes)

        central.setLayout(layout)
        self.setCentralWidget(central)

        botao_novo.clicked.connect(self.cadastrar_cliente)
        botao_excluir.clicked.connect(self.excluir_cliente)
        botao_fechar.clicked.connect(self.close)
        self.campo_pesquisa.textChanged.connect(self.atualizar_tabela)

        self.atualizar_tabela()
        
    def showEvent(self, event):
        super().showEvent(event)
        self.atualizar_tabela()

    def atualizar_tabela(self):
        texto = self.campo_pesquisa.text().strip().lower()
        clientes = get_clientes()

        if texto:
            clientes = [
                c for c in clientes
                if texto in c["nome"].lower() or texto in c["cpf"].lower()
            ]

        self.tabela.setRowCount(0)
        for cliente in clientes:
            linha = self.tabela.rowCount()
            self.tabela.insertRow(linha)
            self.tabela.setItem(linha, 0, QTableWidgetItem(str(cliente["id"])))
            self.tabela.setItem(linha, 1, QTableWidgetItem(cliente["nome"]))
            self.tabela.setItem(linha, 2, QTableWidgetItem(cliente["cpf"]))
            self.tabela.setItem(linha, 3, QTableWidgetItem(cliente.get("telefone", "")))
            self.tabela.setItem(linha, 4, QTableWidgetItem(cliente.get("email", "")))

    def cadastrar_cliente(self):
        dialogo = DialogoCadastroCliente(self)
        if dialogo.exec():
            dados = dialogo.obter_dados()
            if post_cliente(dados):
                self.atualizar_tabela()
                QMessageBox.information(self, "Cadastro realizado", "Cliente cadastrado com sucesso.")
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível cadastrar o cliente na API.")

    def excluir_cliente(self):
        linha = self.tabela.currentRow()
        if linha < 0:
            QMessageBox.warning(self, "Nenhum cliente selecionado", "Selecione um cliente para excluir.")
            return

        id_cliente = int(self.tabela.item(linha, 0).text())
        nome_cliente = self.tabela.item(linha, 1).text()

        resposta = QMessageBox.question(
            self, "Confirmar exclusão", f"Deseja excluir o cliente '{nome_cliente}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            sucesso = delete_cliente(id_cliente)
            if sucesso:
                self.atualizar_tabela()
                QMessageBox.information(self, "Sucesso", "Cliente excluído com sucesso.")
            else:
                QMessageBox.warning(self, "Erro", "Não é possível excluir um cliente que possui locações ativas.")