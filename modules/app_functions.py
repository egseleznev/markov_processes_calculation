from main import *
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from .db_functions import *
import pickle
from fpdf import FPDF

kolmagorov_coefs_pdf=[]

class AppFunctions(MainWindow):
    def setThemeHack(self):
        Settings.BTN_LEFT_BOX_COLOR = "background-color:rgb(168, 166, 255)"
        Settings.BTN_RIGHT_BOX_COLOR = "background-color:rgb(168, 166, 255)"
        Settings.MENU_SELECTED_STYLESHEET = MENU_SELECTED_STYLESHEET = """
        border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgb(168, 166, 255), stop:0.5 rgb(168, 166, 255));
        background-color: rgb(168, 166, 255);
        """

    def drawgraph(self):
        data = DBFunctions.selecttransition(self)
        vertex_union = []
        for i in range(len(data)):
            if str(data[i])[0] == "#" or str(data[i])[2] == "#":
                raise ValueError()
            vertex_union.append([str(data[i]).split(" ")[0],str(data[i]).split(" ")[1], str(data[i]).split(" ")[2]])
        Graph = nx.DiGraph()
        Graph.add_weighted_edges_from(vertex_union)
        pos = nx.planar_layout(Graph)
        nx.draw(Graph, pos, with_labels=False, node_color='#A8A6FF', edge_color='white')
        edge_weight = nx.get_edge_attributes(Graph, 'weight')
        nx.draw_networkx_edge_labels(Graph, pos, edge_labels=edge_weight)
        nx.draw_networkx_labels(Graph, pos, font_color="white")
        if Settings.CHANGE_THEME:
            plt.savefig("graph.png", facecolor="#282C34", dpi=125)
        else:
            plt.savefig("graph.png", facecolor="white", dpi=125)
        nx.draw(Graph, pos, with_labels=False, node_color='#A8A6FF', edge_color='#475161')
        plt.savefig("graph_pdf.png", facecolor="white", dpi=125)
        plt.clf()
        vertex_union.clear()





    def calculate(self):
        global kolmagorov_coefs_pdf
        from_vertex = list([])
        to_vertex = list([])
        weights_vertex = list([])
        data = DBFunctions.selecttransition(self)
        for i in range(len(data)):
            from_vertex.append(int(str(data[i]).split(" ")[0]))
            to_vertex.append(int(str(data[i]).split(" ")[1]))
            weights_vertex.append(float(str(data[i]).split(" ")[2]))
        concat = np.hstack((to_vertex, from_vertex))
        unique_numbers = list(set(concat))
        kolmagorov_coefs = np.zeros((len(unique_numbers), len(unique_numbers)))
        for i in range(len(unique_numbers)):
            for j in range(len(from_vertex)):
                if from_vertex[j] == unique_numbers[i]:
                    kolmagorov_coefs[i, from_vertex[j] - 1] = kolmagorov_coefs[i, from_vertex[j] - 1] - weights_vertex[j]
            for k in range(len(to_vertex)):
                if to_vertex[k] == unique_numbers[i]:
                    kolmagorov_coefs[i, from_vertex[k] - 1] = kolmagorov_coefs[i, from_vertex[k] - 1] + weights_vertex[k]
        kolmagorov_coefs[len(kolmagorov_coefs) - 1, :] = 1
        kolmagorov_coefs_pdf=kolmagorov_coefs
        normalization = np.zeros((len(unique_numbers)))
        normalization[len(unique_numbers) - 1] = 1
        result = np.linalg.solve(kolmagorov_coefs, normalization)
        return result

    def serialize(self, path: str):
        with open(path, 'wb') as outfile:
            data = DBFunctions.selectdescription(self)+['#######']+DBFunctions.selecttransition(self)
            pickle.dump(data, outfile)

    def deserialize(self, path: str):
        with open(path, 'rb') as infile:
            data = pickle.load(infile)
        for i in range(len(data[:data.index('#######')])):
            DBFunctions.insertdescription(self, str(data[:data.index('#######')][i]).split("~~")[0], str(data[:data.index('#######')][i]).split("~~")[1])
        for i in range(len(data[data.index('#######')+1:])):
            DBFunctions.inserttransition(self, str(data[data.index('#######')+1:][i]).split(" ")[0], str(data[data.index('#######')+1:][i]).split(" ")[1], str(data[data.index('#######')+1:][i]).split(" ")[2])

    def printpdf(self, flag: bool):
        if flag:
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font('DeJaVu','','DejaVuSansCondensed.ttf', uni=True)
            pdf.set_font('DejaVu', size=16)
            col_width = pdf.w / 5
            row_height = pdf.font_size
            pdf.cell(200, 7, txt="Результаты расчета марковского процесса", ln=1, align="C")
            pdf.set_font('DejaVu', size=14)
            pdf.cell(200, 7, txt="с дискретными состояниями и непрерывным временем", ln=2, align="C")
            pdf.set_font('DejaVu', size=10)
            pdf.cell(200, 5, txt="(при t → ∞)", ln=3, align="C")
            pdf.set_font('DejaVu', size=11)
            pdf.ln(18)
            pdf.cell(col_width, row_height, txt="Состояние",border=1)
            pdf.cell(col_width, row_height, txt="Описание",border=1)
            pdf.ln(row_height)
            pdf.set_font('DejaVu', size=10)
            for i in range(self.ui.input_table_2.rowCount()):
                for j in range(self.ui.input_table_2.columnCount()):
                    pdf.cell(col_width, row_height, txt=(self.ui.input_table_2.item(i, j).text()))
                pdf.ln(row_height)
            pdf.set_font('DejaVu', size=11)
            pdf.ln(15)
            pdf.cell(col_width, row_height, txt="Исходное состояние",border=1)
            pdf.cell(col_width, row_height, txt="Состояние перехода",border=1)
            pdf.cell(col_width+10, row_height, txt="Интенсивность перехода",border=1)
            pdf.ln(row_height)
            pdf.set_font('DejaVu', size=10)
            for i in range(self.ui.input_table.rowCount()):
                for j in range(self.ui.input_table.columnCount()):
                    pdf.cell(col_width, row_height, txt=(self.ui.input_table.item(i, j).text()))
                pdf.ln(row_height)

            pdf.set_font('DejaVu', size=12)
            pdf.cell(100, 30, txt="Граф состояний:", ln=5, align="L")
            if( self.ui.input_table.rowCount()> 11):
                pdf.add_page()
                pdf.image('graph_pdf.png', x=30, y=pdf.get_y() + 10, w=150)
            else:
                pdf.image('graph_pdf.png', x=30, y=pdf.get_y() - 10, w=150)
            if (self.ui.input_table.rowCount() < 12):
                pdf.set_y(pdf.get_y()+170)
            else:
                pdf.ln(130)
            pdf.cell(100, 15, txt="Коэффициенты системы уравнений Колмогорова:", ln=6, align="L")
            pdf.set_font('DejaVu', size=10)
            for i in kolmagorov_coefs_pdf:
                k=1
                for j in i:
                    pdf.cell(col_width-10,row_height,txt=(str(j)+" x"+str(k)))
                    k=k+1
                pdf.ln(row_height)

            pdf.set_font('DejaVu', size=12)
            pdf.cell(100, 15, txt="Результат:", ln=7, align="L")
            col_width = pdf.w / 3
            pdf.set_font('DejaVu', size=11)
            pdf.cell(col_width, row_height, txt="Состояние")
            pdf.cell(col_width, row_height, txt="Вероятность")
            pdf.ln(row_height)
            pdf.set_font('DejaVu', size=10)
            for i in range(self.ui.result_table.rowCount()):
                for j in range(self.ui.result_table.columnCount()):
                    pdf.cell(col_width,row_height,txt=(self.ui.result_table.item(i, j).text()),border=1)
                pdf.ln(row_height)

            pdf.set_font('DejaVu', size=16)
            sortlist = []
            buffer = ''
            for i in range(self.ui.result_table.rowCount()):
                    sortlist.append(float(self.ui.result_table.item(i, 1).text()))
            sortlist.sort(reverse=True)
            for i in range(self.ui.result_table.rowCount()):
                    if sortlist[0]== float(self.ui.result_table.item(i, 1).text()):
                        buffer = self.ui.result_table.item(i, 0).text()

            pdf.set_font('DejaVu', size=16)
            pdf.cell(200, 30, txt="Вероятнее всего система окажется в состоянии: ", ln=8, align="C")
            pdf.set_font('DejaVu', size=15)
            pdf.cell(200, -5, txt=buffer, ln=9, align="C")

            pdf.set_font('DejaVu', size=10)
            pdf.set_x(55)
            pdf.cell(100,75,txt="Расчеты произведены в приложении «Калькулятор марковских процессов» v1.0.1", ln=10, align="C")


            path = tkinter.filedialog.asksaveasfilename(initialfile='report.pdf')
            pdf.output(path)
        else:
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font('DeJaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
            pdf.set_font('DejaVu', size=16)
            pdf.image('graph_pdf.png', x=30, y=95, w=150)
            col_width = pdf.w / 5
            row_height = pdf.font_size
            pdf.cell(200, 7, txt="Граф состояний марковского процесса", ln=1, align="C")
            pdf.cell(200, 7, txt="с дискретными состояниями и непрерывным временем", ln=2, align="C")
            pdf.set_font('DejaVu', size=10)
            pdf.cell(200, 5, txt="(при t → ∞)", ln=3, align="C")
            pdf.set_font('DejaVu', size=12)
            pdf.ln(18)
            pdf.cell(col_width, row_height, txt="Состояние")
            pdf.cell(col_width, row_height, txt="Описание")
            pdf.ln(row_height)
            pdf.set_font('DejaVu', size=11)
            for i in range(self.ui.input_table_2.rowCount()):
                for j in range(self.ui.input_table_2.columnCount()):
                    pdf.cell(col_width, row_height, txt=(self.ui.input_table_2.item(i, j).text()))
                pdf.ln(row_height)
            pdf.set_font('DejaVu', size=14)
            pdf.cell(100, 30, txt="Граф состояний:", ln=5, align="L")
            pdf.set_y(200)
            pdf.set_font('DejaVu', size=10)
            pdf.set_x(55)
            pdf.cell(100, 75, txt="Построение графа произведено в приложении «Калькулятор марковских процессов» v1.0.1", ln=10,
                     align="C")
            path = tkinter.filedialog.asksaveasfilename(initialfile='graph.pdf')
            pdf.output(path)