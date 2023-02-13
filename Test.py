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
    QTabWidget,
)
from PySide2.QtCore import (
    Signal,
)
from PySide2.QtCore import QSortFilterProxyModel, Qt, QRect
from sqlalchemy import create_engine
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Text,
    ForeignKey,
    insert,
    select,
    delete,
)
import sys


class DateBase:
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///database2.db")
        self.engine.connect()
        metadata = MetaData()
        self.Car = Table(
            "Car",
            metadata,
            Column("Vin", Text(), nullable=False),
            Column("Марка", Text(), nullable=False),
            Column("Модель", Text(), nullable=False),
            Column("Цвет", Text(), nullable=False),
        )

        self.Owner = Table(
            "Owner",
            metadata,
            Column("Номер_удостоверения", Text(), primary_key=True),
            Column("ФИО", Text(), nullable=False),
            Column("Дата_рождения", Text(), nullable=False),
            Column("Номер_и_серия_паспорта", Text(), nullable=False),
        )

        self.Docs = Table(
            "Docs",
            metadata,
            Column("Номер_удостоверения", ForeignKey(self.Owner.c.Номер_удостоверения)),
            Column("Vin", ForeignKey(self.Car.c.Vin)),
            Column("Дата_выдачи_документа", Text(), nullable=False),
            Column("Категория_прав", Text(), nullable=False),
        )
        metadata.create_all(self.engine)
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("database2.db")
        if not db.open():
            return False
        self.conn = self.engine.connect()

        if not self.table_is_empty():
            ins = insert(self.Car)
            r = self.conn.execute(
                ins,
                Vin="1KLBN52TWXM186109",
                Марка="Лада",
                Модель="Приора",
                Цвет="Красный",
            )
            r = self.conn.execute(
                ins,
                Vin="2KLBN52QWER186109",
                Марка="Нива",
                Модель="Тревел",
                Цвет="Черный",
            )
            r = self.conn.execute(
                ins,
                Vin="3KLBN52QWER186109",
                Марка="УАЗ",
                Модель="Патриот",
                Цвет="Синий",
            )
            ins = insert(self.Owner)
            r = self.conn.execute(
                ins,
                Номер_удостоверения="3130675567",
                ФИО="Cиманский М.Ю",
                Дата_рождения="09.09.1999",
                Номер_и_серия_паспорта="0719568675",
            )
            r = self.conn.execute(
                ins,
                Номер_удостоверения="2130175567",
                ФИО="Шиманский Л.Ш",
                Дата_рождения="08.08.1998",
                Номер_и_серия_паспорта="0399568675",
            )
            r = self.conn.execute(
                ins,
                Номер_удостоверения="6430175567",
                ФИО="Лиманский П.Н",
                Дата_рождения="07.07.1997",
                Номер_и_серия_паспорта="1999568675",
            )
            ins = insert(self.Docs)
            r = self.conn.execute(
                ins,
                Номер_удостоверения="3130675567",
                Vin="1KLBN52TWXM186109",
                Дата_выдачи_документа="05.05.2015",
                Категория_прав="BC",
            )
            r = self.conn.execute(
                ins,
                Номер_удостоверения="2130175567",
                Vin="2KLBN52QWER186109",
                Дата_выдачи_документа="06.06.2016",
                Категория_прав="B",
            )
            r = self.conn.execute(
                ins,
                Номер_удостоверения="6430175567",
                Vin="3KLBN52QWER186109",
                Дата_выдачи_документа="07.07.2017",
                Категория_прав="BCD",
            )

    def table_is_empty(self):
        data = self.Car.select()
        table_data = self.conn.execute(data)
        return table_data.fetchall()


class TableView:
    tabBarClicked = Signal(int)

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.SetupUI()
        self.current_tab = "Car"
        self.tab_id = "VIN"

    def SetupUI(self):
        self.parent.setGeometry(400, 500, 1000, 650)
        self.parent.setWindowTitle("Транспортная служба Ставропольского Края")
        self.main_conteiner = QGridLayout()
        self.frame1 = QFrame()
        self.frame2 = QFrame()
        self.frame2.setVisible(False)
        self.main_conteiner.addWidget(self.frame1, 0, 0)
        self.main_conteiner.addWidget(self.frame2, 0, 0)
        self.frame1.setStyleSheet(
            """
            font: bold;
            font-size: 15px;
            """
        )
        self.frame2.setStyleSheet(
            """
            font: bold;
            font-size: 15px;
            """
        )
        self.table_view = QTableView()
        self.table_view.setModel(self.tableCar())
        self.table_view2 = QTableView()
        self.table_view2.setModel(self.tableOwner())
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
        self.tab_conteiner.setTabShape(QTabWidget.Triangular)
        self.tab_conteiner.addTab(self.table_view, "Автомобили")
        self.tab_conteiner.addTab(self.table_view2, "Владельцы")
        self.tab_conteiner.addTab(self.table_view3, "Документы")
        self.layout_main.addWidget(self.tab_conteiner, 0, 0)
        self.layout_main.addLayout(self.layh, 1, 0)
        self.parent.setLayout(self.main_conteiner)
        self.btn_del.clicked.connect(self.delete)
        self.btn_add.clicked.connect(self.add)
        self.layout_grid = QGridLayout(self.frame2)
        self.btn_add2 = QPushButton("Добавить данные")
        self.btn_add2.setFixedWidth(300)
        self.btn_otmena = QPushButton("Отмена")
        self.line_name = QLineEdit()
        self.name = QLabel("ФИО: ")
        self.doc_num_line = QLineEdit()
        self.doc_num = QLabel("Номер удостоверения: ")
        self.color_line = QLineEdit()
        self.color = QLabel("Цвет: ")
        self.dateb_line = QDateEdit()
        self.dateb_line.setCalendarPopup(True)
        self.dateb_line.setTimeSpec(Qt.LocalTime)
        self.dateb_line.setGeometry(QRect(220, 31, 133, 20))
        self.dateb = QLabel("Дата рождения: ")
        self.line_pasport = QLineEdit()
        self.pasport = QLabel("Номер и серия паспорта: ")
        self.vin_line = QLineEdit()
        self.vin = QLabel("VIN-номер: ")
        self.marka_line = QLineEdit()
        self.marka = QLabel("Марка авто: ")
        self.model_line = QLineEdit()
        self.models = QLabel("Модель: ")
        self.docs_reg = QLabel("Дата выдачи документа: ")
        self.docs_reg_line = QDateEdit()
        self.docs_reg_line.setCalendarPopup(True)
        self.docs_reg_line.setTimeSpec(Qt.LocalTime)
        self.docs_reg_line.setGeometry(QRect(220, 31, 133, 20))
        self.cate_line = QLineEdit()
        self.cate = QLabel("Категория прав: ")
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

    def tableCar(self):
        self.raw_model = QSqlTableModel()
        self.query = self.db.Car.select()
        self.sqlquery = QSqlQuery()
        self.sqlquery.exec_(str(self.query))
        self.raw_model.setQuery(self.sqlquery)
        self.current_tab = "Car"
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.raw_model)
        return self.model

    def tableOwner(self):
        self.raw_model = QSqlTableModel()
        self.query = self.db.Owner.select()
        self.sqlquery = QSqlQuery()
        self.sqlquery.exec_(str(self.query))
        self.raw_model.setQuery(self.sqlquery)
        self.current_tab = "Owner"
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.raw_model)
        return self.model

    def tableDocs(self):
        self.raw_model = QSqlTableModel()
        self.query = self.db.Docs.select()
        self.sqlquery = QSqlQuery()
        self.sqlquery.exec_(str(self.query))
        self.raw_model.setQuery(self.sqlquery)
        self.current_tab = "Docs"
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
        self.table_view.setModel(self.tableCar())
        self.table_view2.setModel(self.tableOwner())
        self.table_view3.setModel(self.tableDocs())

    def add_data(self):
        ins = insert(self.db.Car)
        r = self.db.conn.execute(
            ins,
            Vin=self.vin_line.text(),
            Марка=self.marka_line.text(),
            Модель=self.model_line.text(),
            Цвет=self.color_line.text(),
        )
        ins = insert(self.db.Owner)
        r = self.db.conn.execute(
            ins,
            Номер_удостоверения=self.doc_num_line.text(),
            ФИО=self.line_name.text(),
            Дата_рождения=self.dateb_line.text(),
            Номер_и_серия_паспорта=self.line_pasport.text(),
        )
        ins = insert(self.db.Docs)
        r = self.db.conn.execute(
            ins,
            Номер_удостоверения=self.doc_num_line.text(),
            Vin=self.vin_line.text(),
            Дата_выдачи_документа=self.docs_reg_line.text(),
            Категория_прав=self.cate_line.text(),
        )
        self.update()
        self.frame1.setVisible(True)
        self.frame2.setVisible(False)

    def cell_click(self):
        if self.current_tab == "Car":
            return self.table_view.model().data(self.table_view.currentIndex())
        if self.current_tab == "Docs":
            return self.table_view3.model().data(self.table_view3.currentIndex())
        if self.current_tab == "Owner":
            return self.table_view2.model().data(self.table_view2.currentIndex())

    def delete(self):
        if self.current_tab == "Car":
            del_item = delete(self.db.Car).where(
                self.db.Car.c.Vin.like(self.cell_click())
            )
            r = self.db.conn.execute(del_item)
        if self.current_tab == "Docs":
            del_item = delete(self.db.Docs).where(
                self.db.Docs.c.Номер_удостоверения.like(self.cell_click())
            )
            r = self.db.conn.execute(del_item)
        if self.current_tab == "Owner":
            del_item = delete(self.db.Owner).where(
                self.db.Owner.c.Номер_удостоверения.like(self.cell_click())
            )
            r = self.db.conn.execute(del_item)
        self.update()

    def handle_tabbar_clicked(self, index):
        if index == 0:
            self.current_tab = "Car"
            self.tab_id = "VIN"
        elif index == 1:
            self.current_tab = "Owner"
            self.tab_id = "Номер_удостоверения"
        else:
            self.tab_id = "Номер_удостоверения"
            self.current_tab = "Docs"


class MainWindow(QWidget):
    def __init__(self) -> None:
        QWidget.__init__(self)
        my_datebase = DateBase()
        self.main_view = TableView(self, my_datebase)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()