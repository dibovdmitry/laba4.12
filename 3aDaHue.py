#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PySide2.QtWidgets import (
    QTableView,
    QApplication,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QWidget,
    QLineEdit,
    QFrame,
    QLabel,
    QHeaderView,
    QDateEdit,
    QTabWidget
)
from PySide2.QtCore import (
    QAbstractTableModel,
    Signal,
    Slot,
)
from PySide2.QtCore import QSortFilterProxyModel, Qt, QRect
import sys


class DateBase:
    def __init__(self, db_file) -> None:
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(db_file)
        if not db.open():
            return False
        self.q = QSqlQuery()
        self.q.exec_(
            """
        CREATE TABLE IF NOT EXISTS Patient (
            "ФИО пациента" text PRIMARY KEY,
            "Дата рождения" date,
            "Номер полиса" text,
            "Номер СНИЛС" text);"""
        )
        self.q.exec_(
            """
        CREATE TABLE IF NOT EXISTS Doctor (
            "Должность врача" text PRIMARY KEY,
            "ФИО врача" text,
            "Заболевание пациента" text,
            "Жалобы" text);"""
        )
        self.q.exec_(
            """
        CREATE TABLE IF NOT EXISTS Docs (
            "Должность врача" text PRIMARY KEY,
            "ФИО пациента" text,
            "Дата записи" date,
            "Время записи" text);"""
        )
        self.q.exec_(
            """INSERT INTO Patient VALUES("Арбузов Артём Михайлович", "20.10.1987", "1923761282000012", 
            "188-188-188 32")"""
        )
        self.q.exec_(
            """INSERT INTO Patient VALUES("Дыбов Дмитрий Вячеславович", "26.05.2002", "2817218192192891", 
            "122-345-584 32")"""
        )
        self.q.exec_(
            """INSERT INTO Patient VALUES("Васильев Иван Сергеевич", "15.07.1999", "4958343358444588", 
            "245-462-768 75")"""
        )
        self.q.exec_(
            """INSERT INTO Doctor VALUES("Окулист", "Иванов Руслан Викторович", "Катаракта", "Частые глазные боли")"""
        )
        self.q.exec_(
            """INSERT INTO Doctor VALUES("Эндокринолог", "Вараева Ольга Александровна", "Сахарный Диабет", 
            "Тошнота, Усталость")"""
        )
        self.q.exec_(
            """INSERT INTO Doctor VALUES("Хирург", "Петров Николай Игоревич", "Скалиоз", "Боль в пояснице")"""
        )
        self.q.exec_(
            """INSERT INTO Docs VALUES("Окулист", "Арбузов Артём Михайлович", "12.12.2022", "11:30")"""
        )
        self.q.exec_(
            """INSERT INTO Docs VALUES("Эндокринолог", "Дыбов Дмитрий Вячеславович", "15.12.2022", "9:30")"""
        )
        self.q.exec_(
            """INSERT INTO Docs VALUES("Хирург", "Васильев Иван Сергеевич", "11.01.2023", "15:00")"""
        )


class TableView:
    tabBarClicked = Signal(int)

    def __init__(self, parent):
        self.parent = parent
        self.SetupUI()
        self.current_tab = "Patient"
        self.tab_id = "ФИО пациента"

    def SetupUI(self):
        self.parent.setGeometry(400, 500, 1000, 650)
        self.parent.setWindowTitle("База данных поликлиники")
        self.main_conteiner = QGridLayout()
        self.frame1 = QFrame()
        self.frame2 = QFrame()
        self.frame2.setVisible(False)
        self.main_conteiner.addWidget(self.frame1, 0, 0)
        self.main_conteiner.addWidget(self.frame2, 0, 0)
        self.frame1.setStyleSheet(
            """
            font: times new roman;
            font-size: 15px;
            """
        )
        self.frame2.setStyleSheet(
            """
            font: times new roman;
            font-size: 15px;
            """
        )
        self.table_view = QTableView()
        self.table_view.setModel(self.tablePatient())
        self.table_view2 = QTableView()
        self.table_view2.setModel(self.tableDoctor())
        self.table_view3 = QTableView()
        self.table_view3.setModel(self.tableDocs())
        self.table_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.layout_main = QGridLayout(self.frame1)
        self.layh = QHBoxLayout()
        self.btn_add = QPushButton("Добавить")
        self.btn_del = QPushButton("Удалить")
        self.layh.addWidget(self.btn_add)
        self.layh.addWidget(self.btn_del)
        self.tab_conteiner = QTabWidget()
        self.tab_conteiner.addTab(self.table_view, "Пациенты")
        self.tab_conteiner.addTab(self.table_view2, "Врачи")
        self.tab_conteiner.addTab(self.table_view3, "Запись")
        self.layout_main.addWidget(self.tab_conteiner, 0, 0)
        self.layout_main.addLayout(self.layh, 1, 0)
        self.parent.setLayout(self.main_conteiner)
        self.btn_del.clicked.connect(self.delete)
        self.btn_add.clicked.connect(self.add)
        self.layout_grid = QGridLayout(self.frame2)
        self.btn_add2 = QPushButton("Записаться на приём")
        self.btn_add2.setFixedWidth(300)
        self.btn_otmena = QPushButton("Отмена")
        self.line_name = QLineEdit()
        self.name = QLabel("ФИО врача: ")
        self.doc_num_line = QLineEdit()
        self.doc_num = QLabel("Должность врача: ")
        self.color_line = QLineEdit()
        self.color = QLabel("Номер СНИЛС: ")
        self.dateb_line = QLineEdit()
        self.dateb = QLabel("Заболевание пациента: ")
        self.line_pasport = QLineEdit()
        self.pasport = QLabel("Жалобы: ")
        self.vin_line = QLineEdit()
        self.vin = QLabel("ФИО пациента: ")
        self.marka = QLabel("Дата рождения пациента: ")
        self.marka_line = QDateEdit()
        self.marka_line.setCalendarPopup(True)
        self.marka_line.setTimeSpec(Qt.LocalTime)
        self.marka_line.setGeometry(QRect(220, 31, 133, 20))
        self.model_line = QLineEdit()
        self.models = QLabel("Номер полиса: ")
        self.docs_reg = QLabel("Дата записи: ")
        self.docs_reg_line = QDateEdit()
        self.docs_reg_line.setCalendarPopup(True)
        self.docs_reg_line.setTimeSpec(Qt.LocalTime)
        self.docs_reg_line.setGeometry(QRect(220, 31, 133, 20))
        self.cate_line = QLineEdit()
        self.cate = QLabel("Время записи: ")
        self.layout_grid.addWidget(self.line_name, 0, 1)
        self.layout_grid.addWidget(self.name, 0, 0)
        self.layout_grid.addWidget(self.doc_num, 1, 0)
        self.layout_grid.addWidget(self.doc_num_line, 1, 1)
        self.layout_grid.addWidget(self.dateb, 2, 0)
        self.layout_grid.addWidget(self.dateb_line, 2, 1)
        self.layout_grid.addWidget(self.marka_line, 3, 1)
        self.layout_grid.addWidget(self.marka, 3, 0)
        self.layout_grid.addWidget(self.model_line, 4, 1)
        self.layout_grid.addWidget(self.models, 4, 0)
        self.layout_grid.addWidget(self.line_pasport, 5, 1)
        self.layout_grid.addWidget(self.pasport, 5, 0)
        self.layout_grid.addWidget(self.vin_line, 6, 1)
        self.layout_grid.addWidget(self.vin, 6, 0)
        self.layout_grid.addWidget(self.color_line, 7, 1)
        self.layout_grid.addWidget(self.color, 7, 0)
        self.layout_grid.addWidget(self.docs_reg_line, 8, 1)
        self.layout_grid.addWidget(self.docs_reg, 8, 0)
        self.layout_grid.addWidget(self.cate, 9, 0)
        self.layout_grid.addWidget(self.cate_line, 9, 1)
        self.layout_grid.addWidget(self.btn_add2, 10, 1)
        self.layout_grid.addWidget(self.btn_otmena, 10, 0)
        self.btn_otmena.clicked.connect(self.back)
        self.btn_add2.clicked.connect(self.add_data)
        self.tab_conteiner.tabBarClicked.connect(self.handle_tabbar_clicked)

    def tablePatient(self):
        self.raw_model = QSqlTableModel()
        self.sqlquery = QSqlQuery()
        self.query = """SELECT * FROM Patient"""
        self.sqlquery.exec_(self.query)
        self.raw_model.setQuery(self.sqlquery)
        self.current_tab = "Patient"
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.raw_model)
        return self.model

    def tableDoctor(self):
        self.raw_model = QSqlTableModel()
        self.sqlquery = QSqlQuery()
        self.query = """SELECT * FROM Doctor"""
        self.sqlquery.exec_(self.query)
        self.raw_model.setQuery(self.sqlquery)
        self.current_tab = "Doctor"
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.raw_model)
        return self.model

    def tableDocs(self):
        self.raw_model = QSqlTableModel()
        self.sqlquery = QSqlQuery()
        self.query = """SELECT * FROM Docs"""
        self.sqlquery.exec_(self.query)
        self.raw_model.setQuery(self.sqlquery)
        self.current_tab = "Docs"
        self.tab_id = "Должность врача"
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.raw_model)
        return self.model

    def add(self):
        self.frame1.setVisible(False)
        self.frame2.setVisible(True)

    def back(self):
        self.frame1.setVisible(True)
        self.frame2.setVisible(False)

    def update(self):
        self.table_view.setModel(self.tablePatient())
        self.table_view2.setModel(self.tableDoctor())
        self.table_view3.setModel(self.tableDocs())


    def add_data(self):
        self.sqlquery = QSqlQuery()
        self.query = "INSERT INTO Patient VALUES('{}', '{}', '{}', '{}')".format(self.vin_line.text(), self.marka_line.text(), self.color_line.text(), self.model_line.text())
        self.sqlquery.exec_(self.query)
        self.query = "INSERT INTO Doctor VALUES('{}', '{}', '{}', '{}')".format(self.doc_num_line.text(), self.line_name.text(), self.dateb_line.text(), self.line_pasport.text())
        self.sqlquery.exec_(self.query)
        self.query = "INSERT INTO Docs VALUES('{}', '{}', '{}', '{}')".format(self.doc_num_line.text(), self.vin_line.text(), self.docs_reg_line.text(), self.cate_line.text())
        self.sqlquery.exec_(self.query)
        self.update()
        self.frame1.setVisible(True)
        self.frame2.setVisible(False)

    def cell_click(self):
        if self.current_tab == "Patient":
            return self.table_view.model().data(self.table_view.currentIndex())
        if self.current_tab == "Docs":
            return self.table_view3.model().data(self.table_view3.currentIndex())
        if self.current_tab == "Doctor":
            return self.table_view2.model().data(self.table_view2.currentIndex())

    def delete(self):
        self.sqlquery = QSqlQuery()
        self.query = f"""DELETE FROM {self.current_tab} WHERE ("{self.tab_id}" = "{self.cell_click()}")"""
        print(self.query)
        self.sqlquery.exec_(self.query)
        self.update()

    def handle_tabbar_clicked(self, index):
        if(index==0):
            self.current_tab = "Patient"
            self.tab_id = "ФИО пациента"
        elif(index==1):
            self.current_tab = "Doctor"
            self.tab_id = "Должность врача"
        else:
            self.tab_id = "Должность врача"
            self.current_tab = "Docs"

class MainWindow(QWidget):
    def __init__(self) -> None:
        QWidget.__init__(self)
        self.my_datebase = DateBase("hospital.db")
        if not self.my_datebase:
            sys.exit(-1)
        self.main_view = TableView(self)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()