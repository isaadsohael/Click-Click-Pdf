white_theme = """

QMainWindow, QFrame, QMenuBar{
    background-color: rgb(224, 227, 234);
}

QTabWidget::tab-bar {
            alignment: center;
}

QLabel{
    color: black;
}

QPushButton{ 
    color: black;
    background-color: rgb(234, 141, 49);
    border-style: outset;
    border-width: 1px;
    border-radius: 6px;
    border-color: rgb(216, 35, 35);
}

QPushButton:hover{
    background-color: rgb(248, 216, 54);
}

QPushButton:pressed, QPushButton:checked{
    background-color: rgb(220, 83, 14);
}

QLineEdit{
    border-style: outset;
    border-width: 1px;
    border-radius: 6px;
    border-color: rgb(220, 83, 14);
}

"""

black_theme = """

QMainWindow, QFrame,QMenuBar{
    background-color: rgb(55, 55, 55);
}

QTabWidget::tab-bar {
            alignment: center;
}

QMenuBar::item
{
    background-color: rgb(55, 55, 55);
    color: rgb(176, 176, 176);
}
QMenuBar::item::selected
{
    background-color: #3399cc;
    color: #fff;
}
QMenu
{
    background-color: #3399cc;
    color: #fff;
}
QMenu::item::selected
{
    background-color: #333399;
    color: #999;
}

QLabel{
    color: white;
}

QLabel#ccp_title_1, QLabel#ccp_title_2, QLabel#ccp_title_3{
    color: rgb(244, 142, 13);
}

QPushButton{
    color: white;
    background-color: rgb(73, 114, 181);
    border-style: outset;
    border-width: 1px;
    border-radius: 6px;
    border-color: rgb(29, 71, 138);
}

QPushButton:hover{
    background-color: rgb(106, 145, 211);
}

QPushButton:pressed, QPushButton:checked{
    background-color: rgb(25, 70, 144);
}

QLineEdit{
    background-color: rgb(75, 75, 75);
    color: white;
    border-style: outset;
    border-width: 1px;
    border-radius: 6px;
    border-color: rgb(29, 71, 138);
}

QComboBox, QSpinBox{
    background-color: rgb(75, 75, 75);
    color: white;
}

QTabBar::tab{
    background-color: rgb(130, 130, 130);
}
QTabBar::tab:hover{
    background-color: rgb(78, 78, 79);
    color: white;
}


"""
