from PySide2.QtWidgets import QTableWidget, QListWidget


highlight = "#0e81dc"
selectedRowstylesheet = "QTableView{selection-background-color: " + highlight + ";"
selectedRowstylesheet += "selection-color: white; show-decoration-selected: 10};\n"
selectedRowstylesheet += "QTableView::item:focus{"
selectedRowstylesheet += "background-color:" + highlight + "}"


def genTableWidgetHighlightedRowSS(table: QTableWidget):
    table.setStyleSheet(selectedRowstylesheet)


def genlistWidgetHighlightedRowSS(lw: QListWidget):
    ss = """
        QListView {
        show-decoration-selected: 1; /* make the selection span the entire width of the view */
    }

    QListView::item:alternate {
        background: #EEEEEE;
    }

    QListView::item:selected {
        border: 1px solid #6a6ea9;
    }

    QListView::item:selected:!active {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #ABAFE5, stop: 1 #8588B2);
    }

    QListView::item:selected:active {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #6a6ea9, stop: 1 #888dd9);
    }

    QListView::item:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #FAFBFE, stop: 1 #DCDEF1);
    }
    """
    lw.setStyleSheet(ss)
