from PySide6.QtWidgets import *
from DB.database import session
from DB.descriptions import *


class TransitionsTableDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super(TransitionsTableDelegate, self).createEditor(parent, option, index)
        if index.column() in (0, 1):
            editor = QSpinBox(parent)
        else:
            editor = QDoubleSpinBox(parent)
        return editor

    def setEditorData(self, editor, index):
        if index.column() in (0, 1):
            Session = session()
            length = 1
            for row in Session.query(descriptions):
                length = length + 1
            if length == 1:
                m = 1
                M = length
            else:
                m = 1
                M = length -1
        else:
            m = 1
            M = 999
        if hasattr(m, 'toPyObject'):
            m = m.toPyObject()
        if hasattr(M, 'toPyObject'):
            M = M.toPyObject()
        editor.setMinimum(m)
        editor.setMaximum(M)
        super(TransitionsTableDelegate, self).setEditorData(editor, index)
