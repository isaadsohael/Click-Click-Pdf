import PyQt5.QtWidgets as pqw
from PyQt5 import uic
import sys
import os
import shutil

from PyQt5.QtCore import QTimer

import dataHandler as dh
import theme_style as ts
from PIL import Image, ImageFile
from add_blank_page import BlankPage

# deals with splash screen to load and close
# https://shorturl.at/ghlN7
if getattr(sys, "frozen", False):
    import pyi_splash


# https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class UI(pqw.QMainWindow):
    """the below code makes the app size as designed.
    Problem - need to update: Make the window responsive
    """
    # https://stackoverflow.com/questions/64686336/when-i-try-to-run-my-pyqt5-app-the-windows-sizes-changing
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    def __init__(self):
        """Line 15 was added to avoid "image file is truncated (10 bytes not processed)" error which probably happens
        dealing with larger images. [Reference Link Given in line 14]"""
        # https://stackoverflow.com/questions/12984426/pil-ioerror-image-file-truncated-with-big-images
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        dh.create_app_data()

        self.selected_vols = []

        super(UI, self).__init__()

        # creates the drag image box gui refresh timer
        self.timer = QTimer(self)

        # load ui
        uic.loadUi(resource_path("resources/assets/ui/ccp_basic.ui"), self)
        self.setFixedSize(self.width(), self.height())

        if dh.query_app_data("theme_style")[-1][-1] == "White":
            self.setStyleSheet(ts.white_theme)
            self.actionWhite_Theme.setText("White Theme (Current)")
            self.actionBlack_Theme.setText("Black Theme")
        else:
            self.setStyleSheet(ts.black_theme)
            self.actionBlack_Theme.setText("Black Theme (Current)")
            self.actionWhite_Theme.setText("White Theme")

        # declarations
        # tab - 1
        self.crop_button = self.findChild(pqw.QPushButton, "crop_button_2")
        self.select_vol_button = self.findChild(pqw.QPushButton, "select_vol_button_2")
        self.pdf_button = self.findChild(pqw.QPushButton, "pdf_button_2")
        self.manga_browse_button = self.findChild(pqw.QPushButton, "manga_browse_button_2")
        self.volume_browse_button = self.findChild(pqw.QPushButton, "volume_browse_button_2")
        self.starting_vol_number = self.findChild(pqw.QLineEdit, "starting_vol_2")
        self.check_button = self.findChild(pqw.QCheckBox, "separate_folder_check_2")
        self.ltr_check_button = self.findChild(pqw.QPushButton, "ltr_check_button_2")
        self.rtl_check_button = self.findChild(pqw.QPushButton, "rtl_check_button_2")
        self.manga_name = self.findChild(pqw.QLineEdit, "manga_name_2")
        self.volume_number = self.findChild(pqw.QPushButton, "volume_number_button_2")

        # tab - 2
        self.add_blank_page_button = self.findChild(pqw.QPushButton, "add_blank_page_button")

        # tab - 3
        self.drag_image = self.findChild(pqw.QTextEdit, "drag_image")
        self.manual_crop_button = self.findChild(pqw.QPushButton, "manual_crop_button")
        self.browse_images = self.findChild(pqw.QPushButton, "browse_images")
        self.drag_image_label = self.findChild(pqw.QLabel, "drag_image_here_label")
        self.clear_button = self.findChild(pqw.QPushButton, "clear_button")

        # button connections
        self.crop_button.clicked.connect(self.crop_images)
        self.select_vol_button.clicked.connect(self.select_vols)
        self.pdf_button.clicked.connect(self.make_pdf)
        self.manga_browse_button.clicked.connect(self.browse_manga)
        self.blank_page_directory_browse.clicked.connect(self.browse_manga)
        self.volume_browse_button.clicked.connect(self.browse_volume)
        self.check_button.clicked.connect(self.check_button_pressed)
        self.rtl_check_button.clicked.connect(self.rtl_check_button_pressed)
        self.findChild(pqw.QPushButton, "rtl_check_button_3").clicked.connect(self.rtl_check_button_pressed)
        self.ltr_check_button.clicked.connect(self.ltr_check_button_pressed)
        self.findChild(pqw.QPushButton, "ltr_check_button_3").clicked.connect(self.ltr_check_button_pressed)
        self.add_blank_page_button.clicked.connect(self.add_blank_page)
        self.clear_button.clicked.connect(self.clear_button_pressed)
        self.volume_number.clicked.connect(self.set_volume_number)

        self.findChild(pqw.QAction, "actionWhite_Theme").triggered.connect(lambda x: self.change_theme("white"))
        self.findChild(pqw.QAction, "actionBlack_Theme").triggered.connect(lambda x: self.change_theme("black"))
        self.findChild(pqw.QAction, "actionClose").triggered.connect(lambda x: sys.exit())

        # https://stackoverflow.com/questions/63122385/pyqt5-tab-widget-how-can-i-get-the-index-of-active-tab-window-on-mouse-click
        self.findChild(pqw.QTabWidget, "tabWidget").tabBarClicked.connect(self.on_tab_click)

        self.manual_crop_button.clicked.connect(self.crop_manually)
        self.browse_images.clicked.connect(self.browse_manual_crop_image)

        # update app functionalities from saved data in dataHandler
        try:
            self.last_opened_directory = dh.query_app_data("last_opened_dir")[-1][-1]
            self.check_button.setChecked(True) if dh.query_app_data("is_separated_folder")[-1][
                                                      -1] == "YES" else self.check_button.setChecked(False)
        except:
            self.last_opened_directory = "C:\\"
            self.check_button.setChecked(False)

        # show the app
        self.show()

    def change_theme(self, change_to):
        if change_to == "white":
            self.setStyleSheet(ts.white_theme)
            dh.change_theme_style("White")
            self.actionWhite_Theme.setText("White Theme (Current)")
            self.actionBlack_Theme.setText("Black Theme")
        else:
            self.setStyleSheet(ts.black_theme)
            dh.change_theme_style("Black")
            self.actionBlack_Theme.setText("Black Theme (Current)")
            self.actionWhite_Theme.setText("White Theme")

    def rtl_check_button_pressed(self):
        self.rtl_check_button.setChecked(True)
        self.findChild(pqw.QPushButton, "rtl_check_button_3").setChecked(True)
        self.ltr_check_button.setChecked(False)
        self.findChild(pqw.QPushButton, "ltr_check_button_3").setChecked(False)

    def ltr_check_button_pressed(self):
        self.ltr_check_button.setChecked(True)
        self.findChild(pqw.QPushButton, "ltr_check_button_3").setChecked(True)
        self.rtl_check_button.setChecked(False)
        self.findChild(pqw.QPushButton, "rtl_check_button_3").setChecked(False)

    def check_button_pressed(self):
        if self.check_button.isChecked():
            dh.update_checkbox("YES")
        else:
            dh.update_checkbox("NO")

    def browse_manga(self):
        dialog = pqw.QFileDialog()
        dialog.setAcceptDrops(True)
        directory = dialog.getExistingDirectory(directory=self.last_opened_directory)
        self.directory_path_2.setText(directory)
        self.blank_page_directory.setText(directory)
        dh.update_directory(directory)
        try:
            if "vols" in os.listdir(self.directory_path_2.text()):
                self.volume_directory_2.setText(f"{self.directory_path_2.text()}/vols")
            else:
                self.volume_directory_2.setText(f"")
            self.manga_name.setText(directory.split("/")[-1].split(" - Cropped")[0])
        except:
            pass

    def crop_action(self, img_dir):
        img = Image.open(img_dir)
        save_dir = "/".join(img_dir.split("/")[:-1])
        img_name = img_dir.split("/")[-1].split(".")[0]
        img_extension = img_dir.split("/")[-1].split(".")[-1]
        right = img.crop((int(img.width / 2), 0, img.width, img.height))
        left = img.crop((0, 0, int(img.width / 2), img.height))
        img.close()
        if self.rtl_check_button.isChecked():
            right.save(f"{save_dir}/{img_name}.1.{img_extension}")
            left.save(f"{save_dir}/{img_name}.2.{img_extension}")
        elif self.ltr_check_button.isChecked():
            left.save(f"{save_dir}/{img_name}.1.{img_extension}")
            right.save(f"{save_dir}/{img_name}.2.{img_extension}")

    def show_dialog(self, title, text):
        pqw.QMessageBox.information(None, title, text)

    def crop_images(self):
        try:
            if self.check_button.isChecked():
                if not os.path.exists(
                        "/".join(
                            self.directory_path_2.text().split("/")[
                            :-1]) + "/" + self.manga_name.text() + " - Cropped"):
                    manga_directory = "/".join(
                        self.directory_path_2.text().split("/")[:-1]) + "/" + self.manga_name.text() + " - Cropped"
                    shutil.copytree(self.directory_path_2.text(), manga_directory)
                else:
                    self.show_dialog("Warning", "\'{0}/{1} - Cropped\' already exists!".format(
                        "/".join(self.directory_path_2.text().split("/")[
                                 :-1]), self.manga_name.text()))
            else:
                manga_directory = self.directory_path_2.text()
            chapters = os.listdir(manga_directory)
            chapters.sort(key=lambda y: float(y.split()[-1]))
            for ch in chapters:
                # widths = []
                pages = os.listdir(f"{manga_directory}/{ch}")
                # Least width calculation algorithm - 01
                lw = Image.open(f"{manga_directory}/{ch}/{pages[0]}").width
                for pg in pages[1:]:
                    cw = Image.open(f"{manga_directory}/{ch}/{pg}").width
                    if cw < lw:
                        lw = cw
                # Least width calculation algorithm - 02
                """for pg in pages:
                    widths.append(Image.open(f"{manga_directory}/{ch}/{pg}").width)
                #ekhane emon ekta logic dewa lagbe je least width ta ber korbe maximum sonkhok jei size"""
                # print(Counter(widths))
                # print(f"least width : {lw}")
                for pg in pages:
                    cp = Image.open(f"{manga_directory}/{ch}/{pg}")
                    if cp.width > (lw * 1.50):
                        # print('')
                        self.crop_action(f"{manga_directory}/{ch}/{pg}")  # need to add ltr or rtl option
                        # print(f"least width : {lw}")
                        # print(f"boro page width : {cp.width}")
                        cp.close()
                        os.remove(f"{manga_directory}/{ch}/{pg}")
            self.show_dialog("Success", "Crop Done")
        except Exception as e:
            self.show_dialog("Warning", f"Could not crop.\n\n{e}")

    def crop_manually(self):
        if self.drag_image.toPlainText() != "\n":
            self.timer.stop()
            dirs = self.drag_image.toPlainText().split("\n")
            for DIR in dirs:
                if DIR:
                    self.crop_action(DIR)
                    os.remove(DIR)
            self.drag_image.setText("")
            self.show_dialog("Success", "Crop Done")
            self.timer.start()
        else:
            self.show_dialog("Warning!", "Please select images properly")

    def browse_volume(self):
        directory = pqw.QFileDialog.getExistingDirectory(directory=self.directory_path_2.text())
        self.volume_directory_2.setText(directory)

    def select_vols(self):
        # https://stackoverflow.com/questions/38252419/how-to-get-qfiledialog-to-select-and-return-multiple-folders
        file_dialog = pqw.QFileDialog()
        file_dialog.setAcceptDrops(True)
        if self.volume_directory_2.text() != "":
            file_dialog.setDirectory(self.directory_path_2.text() + "/vols")
        else:
            file_dialog.setDirectory(self.directory_path_2.text())
        file_dialog.setFileMode(pqw.QFileDialog.DirectoryOnly)
        file_dialog.setOption(pqw.QFileDialog.DontUseNativeDialog, True)
        file_view = file_dialog.findChild(pqw.QListView, 'listView')

        # to make it possible to select multiple directories:
        if file_view:
            file_view.setSelectionMode(pqw.QAbstractItemView.MultiSelection)
        f_tree_view = file_dialog.findChild(pqw.QTreeView)
        if f_tree_view:
            f_tree_view.setSelectionMode(pqw.QAbstractItemView.MultiSelection)

        if file_dialog.exec():
            self.selected_vols = file_dialog.selectedFiles()
            for v in self.selected_vols:
                try:
                    float(v.split("/")[-1].split()[-1])
                except ValueError:
                    self.selected_vols.remove(v)

    def make_pdf(self):
        start = self.starting_vol_number.text()
        try:
            limit = int(self.set_vol_2.text())
            pdf_name = self.manga_name.text().split(" - Cropped")[0]
            extension = self.vol_extension_2.text()
            volumes = self.selected_vols
            volumes.sort(key=lambda y: float(y.split()[-1]))
            while volumes:
                pages = []
                for v in range(limit):
                    try:
                        chapters = os.listdir(volumes[v])
                        chapters.sort(key=lambda y: float(y.split()[-1]))
                        for ch in chapters:
                            pages.extend(Image.open(y).convert('RGB') for y in
                                         [f'{volumes[v]}/{ch}/{x}' for x in
                                          os.listdir(f"{volumes[v]}/{ch}")])
                    except IndexError:
                        pass
                """fsize = Image.open(
                    volumes[0] + "/" + os.listdir(volumes[0])[0] + "/" +
                    [x for x in
                     os.listdir(volumes[0] + "/" + os.listdir(volumes[0])[0])][
                        0]).size"""
                fsize = max([page.size for page in pages])
                pdf_dir = self.directory_path_2.text() + "/" + "pdfs"
                if not os.path.exists(self.directory_path_2.text() + "/" + "pdfs"):
                    os.mkdir(pdf_dir)
                try:
                    int(start)
                    if extension == "" and start == "":
                        name = pdf_name
                    else:
                        name = f"{pdf_name}_{extension}_{start}"
                    start = int(start) + 1
                except:
                    count = volumes[0].split("/")[-1].split()[-1]
                    if extension == "" and start == "":
                        name = pdf_name
                    else:
                        name = f"{pdf_name}_{extension}_{count}"
                pages = [x.resize(fsize, resample=Image.LANCZOS) for x in pages]
                """pages = [x.transform(size=(fsize[0], fsize[1]),
                                     method=Image.EXTENT,
                                     data=(int(-(fsize[0] - x.width) / 2), int(-(fsize[1] - x.height) / 2),
                                           (x.width + int((fsize[0] - x.width) / 2)),
                                           x.height + int((fsize[1] - x.height) / 2)),
                                     fillcolor=(255, 255, 255)) for x in pages]"""
                pages[0].save(f"{pdf_dir}/{name}.pdf", save_all=True, append_images=pages[1:])
                pages.clear()
                for v in range(limit):
                    try:
                        volumes.remove(volumes[0])
                    except IndexError:
                        pass
            self.show_dialog("Success", "PDF DONE")
        except Exception as e:
            self.show_dialog("Warning", f"Error!\n{e}")

        self.selected_vols.clear()

    def add_blank_page(self):
        page_color = (255, 255, 255) if self.blank_page_color.currentText() == "White Page" else (0, 0, 0)
        bp = BlankPage(int(self.blank_page_width.text()),
                       int(self.blank_page_height.text()),
                       page_color,
                       self.blank_page_directory.text(),
                       self.blank_page_name.text(),
                       self.blank_page_extension.currentText().lower()
                       )
        bp.add_page()

    def on_tab_click(self, index):
        if index == 2:
            self.timer.setSingleShot(False)
            self.timer.setInterval(2)  # in milliseconds, so 1000 = 1 seconds
            self.timer.timeout.connect(self.update_drag_image_gui)
            self.timer.start()
        else:
            self.timer.stop()

    def update_drag_image_gui(self):
        if self.drag_image.toPlainText() != "\n":
            self.drag_image_label.setHidden(True)
        else:
            self.drag_image_label.setHidden(False)
        dirs = self.drag_image.toPlainText().split("\n")
        image_dirs = []

        for v in dirs:
            v = v.replace("file:///", "")
            v = v.replace("%23", "#")
            image_dirs.append(v)

        dirs = image_dirs

        for DIR in dirs:
            if ".jpg" in DIR or ".jpeg" in DIR or ".png" in DIR or ".JPG" in DIR or ".JPEG" in DIR or ".PNG" in DIR:
                pass
            else:
                dirs.remove(DIR)
                self.drag_image.setText("\n".join(dirs) + "\n")

    def browse_manual_crop_image(self):
        # https://stackoverflow.com/questions/38252419/how-to-get-qfiledialog-to-select-and-return-multiple-folders
        file_dialog = pqw.QFileDialog()
        file_dialog.setAcceptDrops(True)
        if self.directory_path_2.text() != "":
            file_dialog.setDirectory(self.directory_path_2.text())
        else:
            file_dialog.setDirectory(self.last_opened_directory)
        file_dialog.setOption(pqw.QFileDialog.DontUseNativeDialog, True)
        file_view = file_dialog.findChild(pqw.QListView, 'listView')

        # to make it possible to select multiple directories:
        if file_view:
            file_view.setSelectionMode(pqw.QAbstractItemView.MultiSelection)
        f_tree_view = file_dialog.findChild(pqw.QTreeView)
        if f_tree_view:
            f_tree_view.setSelectionMode(pqw.QAbstractItemView.MultiSelection)

        if file_dialog.exec():
            self.drag_image.setText(f"{self.drag_image.toPlainText()}\n".join(file_dialog.selectedFiles()))

    def clear_button_pressed(self):
        self.drag_image.setText("\n")

    def set_volume_number(self):
        pass


App = pqw.QApplication(sys.argv)
UI_WINDOW = UI()
# this below code closes splash screen after ui has been loaded
# https://shorturl.at/ghlN7
if getattr(sys, "frozen", False):
    pyi_splash.close()
App.exec_()
