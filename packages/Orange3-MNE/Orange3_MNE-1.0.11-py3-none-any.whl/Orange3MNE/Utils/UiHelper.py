from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton, QSizePolicy, QLineEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QComboBox, \
    QLabel, QSpinBox, QDoubleSpinBox, QCheckBox


class UiHelper():
    """
    Styles for buttons based on the Bootstrap 4 theme
    """
    BUTTON_STYLES = dict()
    BUTTON_STYLES[
        'btn_primary'] = "QPushButton{ color: #fff; background-color: #007bff; text-align:center; vertical-align:middle; " \
                         "font-size: 2 rem; border-radius: 2px; border: 1px solid #007bff; padding: 1 rem }" \
                         "QPushButton:hover { background-color: #0069d9; }" \
                         "QPushButton:disabled { background-color: #6c757d; color: #FFF; border: 1px solid #6c757d}"
    BUTTON_STYLES[
        'btn_danger'] = "QPushButton{ color: #fff; background-color: #d9534f; text-align:center; vertical-align:middle; " \
                        "font-size: 2 rem; border-radius: 2px; border: 1px solid #d9534f; padding: 1 rem }" \
                        "QPushButton:hover { background-color: #c82333; }" \
                        "QPushButton:disabled { background-color: #6c757d; color: #FFF; border: 1px solid #6c757d}"
    BUTTON_STYLES[
        'btn_warning'] = "QPushButton{ color: #212529; background-color: #ffc107; text-align:center; " \
                         "vertical-align:middle; " \
                         "font-size: 2 rem; border-radius: 2px; border: 1px solid #ffc107; padding: 1 rem }" \
                         "QPushButton:hover { background-color: #e0a800; }" \
                         "QPushButton:disabled { background-color: #6c757d; color: #FFF; border: 1px solid #6c757d}"
    BUTTON_STYLES[
        'btn_success'] = "QPushButton{ color: #fff; background-color: #28a745; text-align:center; vertical-align:middle; " \
                         "font-size: 2 rem; border-radius: 2px; border: 1px solid #28a745; padding: 1 rem }" \
                         "QPushButton:hover { background-color: #218838; }" \
                         "QPushButton:disabled { background-color: #6c757d; color: #FFF; border: 1px solid #6c757d}"

    INPUT_ROUNDED_CORNER = "border-radius: 2px; border: 1px solid #343a40;"

    LABEL_SECONDARY = "QLabel{color: #6c757d;}"

    @staticmethod
    def file_dialog(extensions=None, multiple: bool = False, all_files_extension: bool = False, is_save_dialog=False):
        """
        Creates a file picker dialog
        :param is_save_dialog:
        :param all_files_extension: if set to true, adds filter (*.* All files) at the and of the allowed extensions
        :param multiple: if multiple is True, returns list of selected files
        :param extensions: array of allowed file extensions
        :return: absolute path to a file, or array of selected files
        """
        all_files_string = "All files (*.*)";

        if all_files_extension and extensions is not None:
            extensions.append(all_files_string)

        if extensions is None:
            extensions = [all_files_string]

        dialog = QFileDialog()

        if multiple:
            dialog.setFileMode(QFileDialog.ExistingFiles)
        else:
            dialog.setFileMode(QFileDialog.ExistingFile)

        dialog.setNameFilters(extensions)

        if is_save_dialog:
            dialog.setAcceptMode(QFileDialog.AcceptSave)
        else:
            dialog.setAcceptMode(QFileDialog.AcceptOpen)

        if dialog.exec_():
            if multiple:
                return dialog.selectedFiles()
            else:
                file_name = dialog.selectedFiles()[0]
        else:
            file_name = ""

        return file_name

    @staticmethod
    def create_button(text: str = "",
                      callback=None,
                      size: QSize = QSize(100, 21),
                      stylesheet: str = BUTTON_STYLES['btn_primary']):
        """
        Creates new Push Button
        :param text: text of the button
        :param callback: callback function
        :param size: size of the button
        :param stylesheet: optional stylesheet
        :return: QPushButton
        """
        button = QPushButton(text)

        if size is not None:
            button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
            button.setMinimumSize(size)

        if stylesheet is not None:
            button.setStyleSheet(stylesheet)

        button.clicked.connect(callback)

        return button

    @staticmethod
    def create_line_edit(text: str = "",
                         size: QSize = None,
                         stylesheet: str = INPUT_ROUNDED_CORNER,
                         placeholder: str = None,
                         read_only: bool = False,
                         name: str = None):
        """
        Creates input for text
        :param read_only: is the input read only?
        :param placeholder: input placeholder
        :param text: value of the line edit
        :param size: minimum size of the input
        :param stylesheet: stylesheet for the input
        :return: QLineEdit
        """
        line_edit = QLineEdit(text)

        if size is not None:
            line_edit.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
            line_edit.setMinimumSize(size)
        else:
            line_edit.setMinimumHeight(21)

        if placeholder is not None:
            line_edit.setPlaceholderText(placeholder)

        if stylesheet is not None:
            line_edit.setStyleSheet(stylesheet)

        line_edit.setReadOnly(read_only)
        line_edit.setObjectName(name)

        return line_edit

    @staticmethod
    def create_combo_box(items: [] = None, name=None):
        """
        Creates a QT combo box
        :param items: array of available values
        :return: QComboBox
        """
        combo_box = QComboBox()

        if items is None:
            items = []

        combo_box.addItems(items)
        combo_box.setObjectName(name)

        return combo_box

    @staticmethod
    def create_label(text: str = None, stylesheet: str = None):
        """
        Creates a label
        :param text: text of the label
        :param stylesheet:
        :return: QLabel
        """
        label = QLabel(text)

        if stylesheet is not None:
            label.setStyleSheet(stylesheet)

        return label

    @staticmethod
    def create_vertical_layout():
        """
        Creates vertical layout
        :return: QVBoxLayout
        """
        layout = QVBoxLayout()
        return layout

    @staticmethod
    def create_horizontal_layout():
        """
        Creates horizontal layout
        :return: QHBoxLayout
        """
        layout = QHBoxLayout()
        return layout

    @staticmethod
    def create_spin_box(minimum: int = None, maximum: int = None, is_double: bool = False, value=None):
        if not is_double:
            spin_box = QSpinBox()
        else:
            spin_box = QDoubleSpinBox()

        if minimum is not None:
            spin_box.setMinimum(minimum)

        if maximum is not None:
            spin_box.setMaximum(maximum)

        if value is not None:
            spin_box.setValue(value)

        return spin_box

    @staticmethod
    def create_line():
        pass

    @staticmethod
    def create_checkbox(text: str = None, name: str = None):
        checkbox = QCheckBox(text)
        checkbox.setObjectName(name)
        return checkbox
