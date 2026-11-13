from PySide6.QtWidgets import (
    QDialog, QLineEdit, QComboBox, QSpinBox, QFormLayout, QDialogButtonBox, QVBoxLayout, QMessageBox
)

class DialogoCadastroFilme(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cadastrar Filme")
        self.resize(400, 250)

        self.campo_titulo = QLineEdit()
        self.campo_diretor = QLineEdit()

        self.combo_genero = QComboBox()
        self.combo_genero.addItems([
            "Ação", "Aventura", "Comédia", "Drama", "Ficção", "Terror", "Romance"
        ])

        self.combo_classificacao = QComboBox()
        self.combo_classificacao.addItems([
            "Livre", "10 anos", "12 anos", "14 anos", "16 anos", "18 anos"
        ])

        self.campo_quantidade = QSpinBox()
        self.campo_quantidade.setMinimum(1)
        self.campo_quantidade.setMaximum(100)
        self.campo_quantidade.setValue(1)

        formulario = QFormLayout()
        formulario.addRow("Título:", self.campo_titulo)
        formulario.addRow("Diretor:", self.campo_diretor)
        formulario.addRow("Gênero:", self.combo_genero)
        formulario.addRow("Classificação indicativa:", self.combo_classificacao)
        formulario.addRow("Quantidade:", self.campo_quantidade)

        botoes = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        botoes.accepted.connect(self.validar_dados)
        botoes.rejected.connect(self.reject)

        layout_principal = QVBoxLayout()
        layout_principal.addLayout(formulario)
        layout_principal.addWidget(botoes)

        self.setLayout(layout_principal)

    def validar_dados(self):
        titulo = self.campo_titulo.text().strip()
        diretor = self.campo_diretor.text().strip()

        if not titulo:
            QMessageBox.warning(self, "Campo obrigatório", "Informe o título do filme.")
            self.campo_titulo.setFocus()
            return

        if not diretor:
            QMessageBox.warning(self, "Campo obrigatório", "Informe o diretor do filme.")
            self.campo_diretor.setFocus()
            return

        self.accept()

    def obter_dados(self):
        return {
            "titulo": self.campo_titulo.text().strip(),
            "diretor": self.campo_diretor.text().strip(),
            "genero": self.combo_genero.currentText(),
            "classificacao": self.combo_classificacao.currentText(),
            "quantidade": self.campo_quantidade.value()
        }