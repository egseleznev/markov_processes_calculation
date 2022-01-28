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
        
    def serialize(self, path: str):
        with open(path,'wb') as outfile:
            data = DBFunctions.selectdescription(self)+['#######']+DBFunctions.selecttransition(self)
            pickle.dump(data, outfile)

    def deserialize(self, path: str):
            with open(path, 'rb') as infile:
                data = pickle.load(infile)
            for i in range(len(data[:data.index('#######')])):
                DBFunctions.insertdescription(self, (str(data[:data.index('#######')][i]).split("~~")[0]),(str(data[:data.index('#######')][i]).split("~~")[1]))
            for i in range(len(data[data.index('#######')+1:])):
                DBFunctions.inserttransition(self, str(data[data.index('#######')+1:][i])[0], str(data[data.index('#######')+1:][i])[2],str(data[data.index('#######')+1:][i])[4])

    def drawgraph(self):
        vertex_union = []
        from_vertex = list([])
        to_vertex = list([])
        weights_vertex = list([])
        data=DBFunctions.selecttransition(self)
        for i in range(len(data)):
            from_vertex.append(str(data[i])[0])
            to_vertex.append(str(data[i])[2])
            weights_vertex.append(str(data[i])[4])
        vertex_union = []
        for i in range(len(from_vertex)):
            vertex_union.append([from_vertex[i], to_vertex[i], weights_vertex[i]])
        Graph = nx.DiGraph()
        Graph.add_weighted_edges_from(vertex_union)
        labels = nx.get_edge_attributes(Graph, 'weight')
        pos = nx.planar_layout(Graph)
        nx.draw_networkx_nodes(Graph, pos, node_size=300)
        nx.draw_networkx_edges(Graph, pos, edgelist=Graph.edges(), edge_color='black')
        nx.draw_networkx_edge_labels(Graph, pos, edge_labels=labels)
        nx.draw_networkx_labels(Graph, pos)
        nx.draw
        plt.savefig("graph.png", dpi=125)
        plt.clf()
        from_vertex.clear()
        to_vertex.clear()
        weights_vertex.clear()

    def calculate(self):
        global kolmagorov_coefs_pdf
        global normalization_pdf
        global result_pdf
        from_vertex = list([])
        to_vertex = list([])
        weights_vertex = list([])
        data = DBFunctions.selecttransition(self)
        for i in range(len(data)):
            from_vertex.append(int(str(data[i])[0]))
            to_vertex.append(int(str(data[i])[2]))
            weights_vertex.append(int(str(data[i])[4]))
        concat = np.hstack((to_vertex, from_vertex))
        unique_numbers = list(set(concat))
        kolmagorov_coefs = np.zeros((len(unique_numbers), len(unique_numbers)))
        for i in range(len(unique_numbers)):
            for j in range(len(from_vertex)):
                if from_vertex[j] == unique_numbers[i]:
                    kolmagorov_coefs[i, from_vertex[j] - 1] = kolmagorov_coefs[i, from_vertex[j] - 1] - weights_vertex[
                        j]
            for k in range(len(to_vertex)):
                if to_vertex[k] == unique_numbers[i]:
                    kolmagorov_coefs[i, from_vertex[k] - 1] = kolmagorov_coefs[i, from_vertex[k] - 1] + weights_vertex[
                        k]
        kolmagorov_coefs[len(kolmagorov_coefs) - 1, :] = 1
        kolmagorov_coefs_pdf=kolmagorov_coefs
        normalization = np.zeros((len(unique_numbers)))
        normalization[len(unique_numbers) - 1] = 1
        result = np.linalg.solve(kolmagorov_coefs, normalization)
        return result

    def printpdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('DeJaVu','','DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', size=16)
        pdf.image('graph.png', x=30, y=95, w=150)
        col_width = pdf.w / 5
        row_height = pdf.font_size
        pdf.cell(200, 7, txt="Результаты расчета марковского процесса", ln=1, align="C")
        pdf.set_font('DejaVu', size=14)
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
        pdf.cell(100, 15, txt="Коэффициенты системы уравнений Колмогорова-Чепмена:", ln=6, align="L")
        pdf.set_font('DejaVu', size=12)
        for i in kolmagorov_coefs_pdf:
            k=1
            for j in i:
                pdf.cell(col_width,row_height,txt=(str(j)+" x"+str(k)))
                k=k+1
            pdf.ln(row_height)

        pdf.set_font('DejaVu', size=14)
        pdf.cell(100, 15, txt="Результат:", ln=7, align="L")
        col_width = pdf.w / 3
        pdf.set_font('DejaVu', size=12)
        pdf.cell(col_width, row_height, txt="Состояние")
        pdf.cell(col_width, row_height, txt="Вероятность")
        pdf.ln(row_height)
        pdf.set_font('DejaVu', size=11)
        for i in range(self.ui.result_table.rowCount()):
            for j in range(self.ui.result_table.columnCount()):
                pdf.cell(col_width,row_height,txt=(self.ui.result_table.item(i, j).text()),border=1)
            pdf.ln(row_height)

        pdf.set_font('DejaVu', size=16)
        sortlist=[]
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
        pdf.cell(100,75,txt="Расчеты произведены в приложении «Калькулятор марковских процессов» v1.0.1",ln=10,align="C")
        path = tkinter.filedialog.askopenfilename()
        pdf.output(path)
