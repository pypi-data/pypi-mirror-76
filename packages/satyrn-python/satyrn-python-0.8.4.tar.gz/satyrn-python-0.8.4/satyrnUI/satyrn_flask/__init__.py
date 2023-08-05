import os, random, string, json, sys, contextlib, threading

from flask import Flask, send_from_directory, render_template, request
from contextlib import redirect_stdout
from io import StringIO

import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk

global exec_vars
exec_vars = {}


"""
Structure Guide

Cells, sometimes referred to as nodes, are data points that either hold markdown data or code. They also have names.

The Graph is a collection of Cells. We use networkx as a backend for basic graph operations and add in methods to
provide functionality specific to our needs.

The Interpreter is the 'frontend' of the application, and provides a text-based interface for users to interact with
the graph and individual nodes.

TextIO is just a handy way of taking multi-line input from users and displaying text back to them.
"""


class TextIO:

    def __init__(self):
        # Root tkinter window
        self.root = None
        self.user_input = ""

    def get_text_from_widget(self, widget):
        """
        :param widget: Widget to pull text from
        """
        self.user_input = widget.get("1.0", "end")
        self.root.quit()

    def text_input(self, existing_text=None):
        self.root = tk.Tk()
        self.root.wm_title("Satyrn Text Editor")
        # Open text input window and return the text
        text = tk.Text(self.root)
        if existing_text:
            text.insert(1.0, existing_text)
        text.pack()

        save_close = tk.Button(self.root,
                               text="Save and Close",
                               command=lambda: self.get_text_from_widget(text))
        save_close.pack()

        self.root.mainloop()
        self.root.destroy()

        return self.user_input


class Cell():

    def __init__(self,
                 name_,
                 content_type_="python",
                 content_=" ",
                 stdout="internal"):
        """
        :param name_: The cell's name
        :param graph_: The cell's parent graph
        :param content_type_: The type of content in the cell (markdown or python)
        :param content_: The contents of the cell, either markdown or python code
        """
        self.name = name_
        self.content_type = content_type_
        self.content = content_
        self.stdout = stdout
        self.output = ""

    def get_copy(self):
        return Cell(self.name, self.content_type, self.content, self.stdout)

    """
    @contextlib.contextmanager
    def stdoutIO(self, stdout=None):
        old = sys.stdout
        if stdout is None:
            stdout = StringIO.StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old
    """

    def execute(self):
        # Execute this cell's content

        if not self.content_type == "python":
            return

        global exec_vars
        ex_vars_copy = exec_vars.copy()

        if self.stdout == "internal":
            try:
                exec(self.content, ex_vars_copy)
            except Exception as e:
                print("Exception occurred in cell " + self.name)
                print(e)
        elif self.stdout == "external":
            try:
                print("<" + self.name + ">")
                exec(self.content, ex_vars_copy)
            except Exception as e:
                print("Exception occurred in cell " + self.name)
                print(e)
        else:
            print("stdout setting \"" + self.stdout + "\" not recognized. Please use internal/external.")

        exec_vars.update(ex_vars_copy)

    def __str__(self):
        return self.name + "\n\n" + "```\n" + self.content + "```\n"


class Graph:

    def __init__(self, parent):
        # Networkx Directed graph
        self.graph = nx.DiGraph()
        self.parent = parent
        # Dict to keep track of cell names vs networkx node names
        self.names_to_indeces = {}
        # Dictionaries for variables created by cells
        global exec_vars
        exec_vars = {}
        # TextIO object
        self.ti = TextIO()

        self.executing = False

    def get_lookup_table(self):
        return {idx: moniker for moniker, idx in
                zip(list(self.names_to_indeces.keys()), list(self.names_to_indeces.values()))}

    def update_vars(self, new_globals, new_locals):
        self.exec_globals.update(new_globals)
        self.exec_locals.update(new_locals)

    def name_to_idx(self, cell_name):
        """
        :param cell_name: Name of cell
        :return: Corresponding index of provided cell name
        """
        cell_name = cell_name.strip()
        if cell_name not in self.get_all_cells_edges()[0]:
            print("Cell \"" + cell_name + "\" does not exist")
            return -1
        else:
            return self.names_to_indeces[cell_name]

    def get_cell(self, cell_name, cell_index=None):
        """
        :param cell_name: Name of desired cell
        :param cell_index: If this is set, it'll retrieve the cell at this index
        :return: Cell object
        """
        cells = list(nx.get_node_attributes(self.graph, 'data').values())

        if cell_index is not None:
            output = cells[cell_index]
            return output

        for cell in cells:
            if cell.name == cell_name:
                return cell

    def add_cell(self, new_cell: Cell):
        """
        :param new_cell: Cell object to be added to graph
        """
        if new_cell.name in list(self.names_to_indeces.keys()):
            print(new_cell.name)
            print("All cells must have unique names")
            return
        else:
            self.graph.add_node(len(self.graph.nodes), data=new_cell, name=new_cell.name)

        self.names_to_indeces.update({new_cell.name: len(self.names_to_indeces)})

    def remove_cell(self, cell_name, cell_index=None):
        """
        :param cell_name: Name of cell to be removed
        :param cell_index: If this is set, it'll remove the cell at this index
        """
        if cell_index:
            cell_name = self.get_cell("", cell_index).name

            self.graph.remove_node(cell_index)
            del self.names_to_indeces[cell_name]
        elif self.get_cell(cell_name):
            idx = self.name_to_idx(cell_name)

            self.graph.remove_node(idx)
            del self.names_to_indeces[cell_name]
        else:
            print("Cell \"" + cell_name + "\" does not exist.")
            return -1

    def connect_cells(self, idx1, idx2):
        """
        :param idx1: Index of first cell
        :param idx2: Index of second cell
        """
        self.graph.add_edge(idx1, idx2)

    def sever_cells(self, idx1, idx2):
        """
        :param idx1: Index of first cell
        :param idx2: Index of second cell
        """
        self.graph.remove_edge(idx1, idx2)

    def swap_cells(self, name1, name2):

        old_cell1 = self.get_cell(name1)
        old_cell2 = self.get_cell(name2)

        cell1 = Cell(name2, old_cell2.content_type, old_cell2.content)
        cell2 = Cell(name1, old_cell1.content_type, old_cell1.content)

        idx1 = self.name_to_idx(name1)
        idx2 = self.name_to_idx(name2)

        self.graph.nodes[idx1]["data"] = cell1
        self.graph.nodes[idx1]["name"] = name2

        self.graph.nodes[idx2]["data"] = cell2
        self.graph.nodes[idx2]["name"] = name1

        self.names_to_indeces[name1] = idx2
        self.names_to_indeces[name2] = idx1

    def merge_cells(self, idx1, idx2, new_name):
        if not self.graph.has_edge(idx1, idx2):
            print("To merge, cells must be adjacent")
            return

        c1 = self.get_cell("", idx1)
        c2 = self.get_cell("", idx2)

        glb = c1.self_globals
        lcl = c1.self_locals

        glb.update(c2.self_globals)
        lcl.update(c2.self_locals)

        # make new cell
        new_cell = Cell(new_name, content_type_=self.get_cell("", idx1).content_type)
        new_content = self.get_cell("", idx1).content + "\n# merge point\n" + self.get_cell("", idx2).content
        new_cell.content = new_content
        self.names_to_indeces[new_name] = self.names_to_indeces[self.get_cell("", idx1).name]
        del self.names_to_indeces[self.get_cell("", idx1).name]
        self.graph.nodes[idx1]["data"] = new_cell
        self.graph.nodes[idx1]["name"] = new_name

        # in -> (1 + 2 merged) -> out
        out_edges = list(self.graph.out_edges(idx2))

        self.remove_cell("", idx2)

        for edge in out_edges:
            out_node = edge[1]
            self.connect_cells(idx1, out_node)

    def update_reverse_lookup_table(self):
        cell_names, _, _2 = self.get_all_cells_edges()
        cell_indeces = list(self.graph.nodes)
        self.names_to_indeces = {name: idx for name, idx in zip(cell_names, cell_indeces)}

    def display(self):
        # Display graph in matplotlib
        pos = nx.spring_layout(self.graph)

        self.update_reverse_lookup_table()
        labels = self.get_lookup_table()

        nx.draw_networkx_nodes(self.graph, pos)
        nx.draw_networkx_edges(self.graph, pos)
        nx.draw_networkx_labels(self.graph, pos, labels)

        plt.show()

    def get_all_cells_edges(self):
        lookup_table = self.get_lookup_table()
        return list(nx.get_node_attributes(self.graph, 'name').values()), list(self.graph.edges), \
               [(lookup_table[idx1], lookup_table[idx2]) for idx1, idx2 in list(self.graph.edges)]

    def get_in_out_edges(self, cell_name, cell_index=None):
        if not cell_index:
            cell_index = self.name_to_idx(cell_name)

        lookup_table = self.get_lookup_table()

        in_edges = []
        in_edges_idx = self.graph.in_edges(cell_index)
        for edge in in_edges_idx:
            idx_1 = edge[0]
            idx_2 = edge[1]
            str_edge = "" + str(lookup_table[idx_1]) + " -> " + str(lookup_table[idx_2])
            in_edges.append(str_edge)

        out_edges = []
        out_edges_idx = self.graph.out_edges(cell_index)
        for edge in out_edges_idx:
            idx_1 = edge[0]
            idx_2 = edge[1]
            str_edge = "" + str(lookup_table[idx_1]) + " -> " + str(lookup_table[idx_2])
            out_edges.append(str_edge)

        return in_edges, out_edges

    def execute_linear_list_of_cells(self, cells_list, stdout="internal", output_filename="stdout.txt"):
        std_file_out = ""

        for cell_name in cells_list:
            cell = self.get_cell(cell_name)

            cell.stdout = stdout

            p = threading.Thread(target=cell.execute)

            if cell.content_type == "python":
                p.start()
                p.join()

            std_file_out += cell.output

        if stdout == "external":
            with open(output_filename, 'w') as txt:
                txt.write(std_file_out)

    def bfs_traversal_execute(self, stdout="external", output_filename="stdout.txt"):
        import time
        if len(self.get_all_cells_edges()[0]) == 0:
            return

        std_file_out = "<root>"

        self.executing = True

        root_cell = self.get_cell("", 0)
        root_cell.stdout = stdout

        root = threading.Thread(target=root_cell.execute)

        root.start()
        root.join()

        time.sleep(.05)

        std_file_out += root_cell.output

        n_ = self.graph.neighbors(0)
        neighbors = [n for n in n_]

        while neighbors:
            new_neighbors = []
            processes = []
            for n in neighbors:
                neighbor_cell = self.get_cell(self.get_lookup_table()[n].strip())
                neighbor_cell.stdout = stdout

                neighbor = threading.Thread(target=neighbor_cell.execute)

                neighbor.start()
                processes.append(neighbor)

                new_neighbors.extend([i for i in self.graph.neighbors(n)])

            [proc.join() for proc in processes]

            for n in neighbors:
                time.sleep(.05)
                neighbor = self.get_cell(self.get_lookup_table()[n])
                std_file_out += "<" + neighbor.name + ">\n"
                std_file_out += neighbor.output

            neighbors = new_neighbors

        self.executing = False

    def save_graph(self, filename):
        txtout = ""

        filename = filename.replace("\"", "")

        lookup_table = self.get_lookup_table()
        cell_names, edges, _ = self.get_all_cells_edges()
        cells = [self.get_cell(cn) for cn in cell_names]

        for c in cells:
            if c.content:
                fill_with_code = "y:\n"
            else:
                fill_with_code = "n\n"
            temp_text = "cell " + c.name + " " + c.content_type + " " + fill_with_code
            if fill_with_code == "y:\n":
                temp_text += c.content + "\n;\n"

            txtout += temp_text

        for e in edges:
            name1 = lookup_table[e[0]]
            name2 = lookup_table[e[1]]
            txtout += "link " + name1 + " " + name2 + "\n"

        with open(filename, "w+") as file:
            file.write(txtout)

    def get_satx_as_txt(self):
        txtout = ""

        lookup_table = self.get_lookup_table()
        cell_names, edges, _ = self.get_all_cells_edges()
        cells = [self.get_cell(cn) for cn in cell_names]

        for c in cells:
            if c.content:
                fill_with_code = "y:\n"
            else:
                fill_with_code = "n\n"
            temp_text = "cell " + c.name + " " + c.content_type + " " + fill_with_code
            if fill_with_code == "y:\n":
                temp_text += c.content + "\n;\n"

            txtout += temp_text

        for e in edges:
            name1 = lookup_table[e[0]]
            name2 = lookup_table[e[1]]
            txtout += "link " + name1 + " " + name2 + "\n"

        if self.parent.std_capture.getvalue():
            txtout += "<!--SATYRN_DCO_START-->\n"
            txtout += self.parent.std_capture.getvalue()
            txtout += "<execution complete>\n<!--SATYRN_DCO_END-->"

        return txtout

    def get_py_file(self):
        txtout = ""

        lookup_table = self.get_lookup_table()
        cell_names, edges, _ = self.get_all_cells_edges()
        cells = [self.get_cell(cn) for cn in cell_names]

        for c in cells:
            txtout += "# <" + c.name + ">\n"
            if c.content_type == "python":
                txtout += c.content + "\n"
            else:
                txtout += "\"\"\"\n" + c.content + "\n\"\"\"\n"

        txtout += "# <EOF>"

        return txtout


class Interpreter:

    def __init__(self):
        # Graph object
        self.graph = Graph(self)
        # Assume live input first
        self.input_type = "file"
        # This will be set if the user executes a .satx file
        self.file = None
        # This determines whether or not stdout gets sent to an external textbox
        self.stdout = "external"
        self.stdout_filename = "stdout.txt"
        # Start loop
        self.std_capture = StringIO()

    def run_file(self, command):
        """
        :param command: command to be executed
        """
        try:
            openfile = open(command[0], "r")
            self.file = openfile.readlines()
            self.input_type = "file"
        except Exception as e:
            print(e)

    def run_string(self, content):
        self.file = content
        self.input_type = "file"

        reading_dco_output = False

        while len(content) > 0:
            command = content.pop(0).split(" ")
            print(command)

            if "<!--SATYRN_DCO_START-->" in command[0]:
                reading_dco_output = True
                continue
            if "<!--SATYRN_DCO_END-->" in command[0]:
                reading_dco_output = False
                continue

            if reading_dco_output:
                self.std_capture.write(" ".join(command) + "\n")
                continue

            if len(command) == 0 or command == '':
                continue

            elif command[0] == "help":
                print(self.help_menu())

            elif command[0] == "quit":
                break

            elif command[0] == "cell":
                self.create_cell(command)

            elif command[0] == "edit":
                self.edit_cell(command)

            elif command[0] == "rename":
                self.rename_cell(command)

            elif command[0] == "remove":
                self.remove_cell(command)

            elif command[0] == "link":
                self.link(command)

            elif command[0] == "sever":
                self.sever(command)

            elif command[0] == "merge":
                self.merge(command)

            elif command[0] == "swap":
                self.swap(command)

            elif command[0] == "execute":
                self.execute(command)

            elif command[0] == "display":
                self.display(command)

            elif command[0] == "list":
                self.list_cells()

            elif command[0] == "stdout":
                self.set_stdout(command)

            elif command[0] == "reset_runtime":
                self.reset_runtime()

            elif command[0] == "reset_graph":
                self.reset_graph()

            elif command[0] == "save":
                self.save_graph(command)

            elif ".satx" in command[0]:
                self.run_file(command)

            elif command[0]:
                print("Syntax error: command \"" + command[0] + "\" not recognized.")

    def read_input(self):
        # Read input from stdin or external file. Returns list of command params.
        if self.input_type == "live" or len(self.file) == 0:
            usr = input("♄: ").strip()
            self.input_type = "live"
        else:
            usr = self.file.pop(0).strip()
            print("♄: " + usr)

        usr = usr.lower()
        return usr.split()

    @staticmethod
    def help_menu():
        help_menu = {
            "cell [cell_name] [content_type](python/markdown) [add_content](y/n)": "Creates a cell with the specified "
                                                                                   "parameters",
            "remove [cell_name_1] [cell_name_2] ...": "Removes all listed cells",
            "edit [cell_name]": "Edit contents of cell with specified name",
            "link [first_cell_name] [second_cell_name]": "Creates link from first_cell to second_cell",
            "sever [first_cell_name] [second_cell_name]": "Removes link between first_cell and second_cell",
            "merge [first_cell_name] [second_cell_name]": "Merges the two cells if they are adjacent",
            "swap [first_cell_name] [second_cell_name]": "Swaps name, content type, and contents of specified cells",
            "execute [cell_name_1] [cell_name_2] ... >> (filename)": "Executes graph. If no cell names are provided, "
                                                                     "all will be executed. \n\t\tIf '>> filename' is "
                                                                     "included, stdout will be saved to the specified "
                                                                     "file in plain text format ",
            "display [cell_name]": "Displays graph. If cell_name defined, that cell's details will be printed out",
            "list": "Prints out names of all cells in graph",
            "reset_runtime": "Deletes all variables created within cells",
            "reset_graph": "Deletes all variables and cells. Equivalent to restarting satyrn_python session",
            "save [filename].satx": "Saves graph to .satx file",
            "[filename].satx": "Executes satyrn_python code in specified file. File must have .satx extension. "
                               "\n\t\tExamples of "
                               "syntax can be seen at https://github.com/CharlesAverill/satyrn/tree/master/examples ",
            "quit": "Exits satyrn_python session"
        }
        output = ("------------------------------------------------------------------------\n"
                  "Hi, and welcome to Satyrn.\n"
                  "Satyrn is an experimental application that extends typical notebook functionality.\n"
                  "Satyrn provides the same functionality as a typical notebook, but allows for branching.\n"
                  "Therefore, cells can run in parallel. Please type \'help\' for a list of commands. Thank you!\n"
                  "------------------------------------------------------------------------\n\n")
        help_list = [(command, description) for command, description in
                     zip(list(help_menu.keys()), list(help_menu.values()))]
        for item in help_list:
            output += "\t" + item[0] + " :\n\t\t" + item[1] + "\n\n"
        return output

    def create_cell(self, command):
        """
        :param command: command to be executed
        """
        keywords = ["help", "quit", "cell", "link", "sever",
                    "execute", "display", "remove", "reset_runtime",
                    "edit", "swap", "list", "reset_graph", "merge", "save"]

        if len(command) != 4:
            print("create_cell takes 3 arguments: [name] [content_type] [add_content]")
            return

        name = command[1]
        if name in keywords:
            print("\"" + name + "\" is a restricted keyword and cannot be used for a cell name.")
            return

        if ".satx" in name:
            print("Cell names cannot include \".satx\"")
            return

        content_type = command[2]
        content = ""

        if "y" in command[3]:
            if self.input_type == "file":
                temp = ""
                while ";" not in temp:
                    content += temp
                    temp = self.file.pop(0) + "\n"
            else:
                ti = TextIO()
                content = ti.text_input().strip()

        self.graph.add_cell(Cell(name, content_type, content))

    def edit_cell(self, command):
        """
        :param command: command to be executed
        """
        if len(command) != 2:
            print("edit takes 1 argument: [cell_name]")
            return

        target_cell = self.graph.get_cell(command[1])
        old_content = target_cell.content

        ti = TextIO()
        new_content = ti.text_input(old_content).strip()

        target_cell.content = new_content

    def set_cell_contents(self, command):
        target_cell = self.graph.get_cell(command[1])
        target_cell.content = command[2]

    def rename_cell(self, command):
        """
        :param command: command to be executed
        """
        if len(command) != 3:
            print("link takes 2 arguments: [original_cell_name] [new_cell_name]")
            return

        index = self.graph.names_to_indeces[command[1]]
        og_name = self.graph.get_cell(command[1]).name

        self.graph.get_cell(og_name).name = command[2]
        self.graph.names_to_indeces.update({command[2]: index})
        del self.graph.names_to_indeces[og_name]

        for node, data in self.graph.graph.nodes(data=True):
            if data['name'] == command[1]:
                data['name'] = command[2]
                break

    def remove_cell(self, command):
        """
        :param command: command to be executed
        """
        to_remove = command[1:]
        for cell in to_remove:
            i = self.graph.remove_cell(cell)
            if i == -1:
                return -1

    def link(self, command):
        """
        :param command: command to be executed
        """
        if len(command) != 3:
            print("link takes 2 arguments: [cell_1] [cell_2]")
            return

        idx1 = self.graph.name_to_idx(command[1])
        idx2 = self.graph.name_to_idx(command[2])
        """
        if idx2 == 0:
            confirm = input("WARNING: You are attempting to connect a node to your root node. This could cause unwanted"
                            " recursive behavior. Are you sure? (y/n) ")
            if "y" in confirm.lower():
                self.graph.connect_cells(idx1, idx2)
        else:
        """
        self.graph.connect_cells(idx1, idx2)

    def sever(self, command):
        """
        :param command: command to be executed
        """
        if len(command) != 3:
            print("sever takes 2 arguments: [cell_1] [cell_2]")
            return

        name_1 = self.graph.name_to_idx(command[1])
        name_2 = self.graph.name_to_idx(command[2])

        self.graph.sever_cells(name_1, name_2)

    def swap(self, command):
        """
        :param command: command to be executed
        """
        if len(command) != 3:
            print("swap takes 2 arguments: [cell_1] [cell_2]")
            return
        self.graph.swap_cells(command[1], command[2])

    def merge(self, command):
        """
        :param command: command to be executed
        """
        if not (2 < len(command) < 4):
            print("merge takes 2-3 arguments: [cell_1] [cell_2] (new_name)")
            return

        name_1 = self.graph.name_to_idx(command[1])
        name_2 = self.graph.name_to_idx(command[2])

        if len(command) >= 4:
            newname = command[3]
        else:
            newname = command[1] + "_merged"

        self.graph.merge_cells(name_1, name_2, newname)

    def execute(self, command):
        """
        :param command: command to be executed
        """
        if ">>" in command:
            cells_list = command[1:-2]
            self.stdout_filename = command[-1]
        else:
            cells_list = command[1:]
        if len(cells_list) >= 1:
            try:
                self.graph.execute_linear_list_of_cells(cells_list, self.stdout, self.stdout_filename)
            except Exception as e:
                print("There was an error executing one of the cells")
                print(e)
        else:
            self.graph.bfs_traversal_execute(self.stdout, self.stdout_filename)

    def display(self, command):
        """
        :param command: command to be executed
        """
        if len(command) == 1:
            self.graph.display()
        else:
            if len(command) != 2:
                print("display takes 0 or 1 arguments: [name_of_cell_to_print]")
                return
            else:
                if not self.graph.get_cell(command[1]):
                    print("Cell " + command[1] + " does not exist")
                    return
                code = self.graph.get_cell(command[1]).content.strip()
                if code:
                    print("\n```\n" + code + "\n```\n")
                in_edges, out_edges = self.graph.get_in_out_edges(command[1])
                if len(in_edges) > 0:
                    print("In Edges:")
                    for e in in_edges:
                        print(e)
                print()
                if len(out_edges) > 0:
                    print("Out Edges:")
                    for e in out_edges:
                        print(e)
                    print()

    def list_cells(self):
        nodes, _, edge_names = self.graph.get_all_cells_edges()
        print("Cells:", nodes)
        print("Edges:", edge_names)

    def set_stdout(self, command):
        """
        :param command: command to be executed
        """
        if len(command) != 2 or (not command[1] == "internal" and not command[1] == "external"):
            print("stdout takes 1 arguments: (internal/external)")
            return
        self.stdout = command[1]

    def reset_runtime(self):
        # Delete all runtime variables
        global exec_vars
        exec_vars = {}

    def reset_graph(self, ask=True):
        if (ask):
            confirm = input(
                "Are you sure you want to reset the graph? This will delete all nodes and variables. (y/n) ")
            if "y" in confirm:
                self.graph = Graph(self)
                self.reset_runtime()
                self.std_capture = StringIO()
        else:
            self.graph = Graph(self)
            self.reset_runtime()
            self.std_capture = StringIO()

    def save_graph(self, command):
        """
        :param command: command to be executed
        """
        if len(command) != 2:
            print("save takes 1 argument1: [filename]")
            return
        self.graph.save_graph(command[1])


interpreter = Interpreter()


def new_name():
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(5)))
    return result_str


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.root_path = os.path.dirname(os.path.abspath(__file__))
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    interpreter.create_cell(["create_cell", "root", "python", "n"])

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/canvas.html")
    def canvas():
        return render_template("canvas.html")

    @app.route("/index_style.css")
    def index_style():
        return render_template("index_style.css")

    @app.route("/rubyblue.css")
    def rubyblue():
        return render_template("rubyblue.css")

    @app.route("/canvas_style.css")
    def canvas_style():
        return render_template("canvas_style.css")

    @app.route("/bootstrap.min.css")
    def bootstrap_style():
        return render_template("bootstrap.min.css")

    @app.route("/gh-buttons.css")
    def gh_buttons():
        return render_template("gh-buttons.css")

    @app.route("/static/css/bootstrap.min.css.map")
    def bootstrap_map():
        return "idk why this is here but this hides an error"

    @app.route("/script.js")
    def script_js():
        return render_template("script.js")

    @app.route("/jquery-1.12.4.js")
    def jquery_js():
        return render_template("jquery-1.12.4.js")

    @app.route("/jquery-ui.js")
    def jquery_ui_js():
        return render_template("jquery-ui.js")

    @app.route("/jquery-ui.css")
    def jquery_ui_css():
        return render_template("jquery-ui.css")

    @app.route("/panzoom.min.js")
    def panzoom_js():
        return render_template("panzoom.min.js")

    @app.route("/codemirror.css")
    def codemirror_css():
        return render_template("codemirror.css")

    @app.route("/codemirror/lib/codemirror.js")
    def codemirror_js():
        return render_template("codemirror/lib/codemirror.js")

    @app.route("/python.js")
    def py_js():
        return render_template("python.js")

    @app.route("/markdown.js")
    def md_js():
        return render_template("markdown.js")

    @app.route("/create_cell/", methods=["GET"])
    def create_cell():
        name = new_name()
        interpreter.create_cell(["create_cell", name, "python", "n"])
        return name

    @app.route("/destroy_cell/", methods=["POST"])
    def destroy_cell():
        cell_name = request.get_json().strip()

        cell = interpreter.graph.get_cell(cell_name)

        initial_length = len(interpreter.graph.graph.nodes())

        output = interpreter.remove_cell(["remove", cell_name])

        success = "false"
        if not initial_length == len(interpreter.graph.graph.nodes()):
            success = "true"

        return {'success': success,
                'name': cell.name,
                'content': cell.content,
                'content_type': cell.content_type}

    @app.route("/edit_cell/", methods=["POST"])
    def edit_cell():
        data = request.get_json()
        cell_name = data['name'].strip()
        content = data['content'].strip()

        interpreter.set_cell_contents(['edit_cell', cell_name, content])

        return "true"

    @app.route("/rename_cell/", methods=["POST"])
    def rename_cell():
        data = request.get_json()
        old_name = data['old_name'].strip()
        new_name = data['new_name'].strip()

        if new_name in interpreter.graph.get_all_cells_edges()[0]:
            return "false"

        interpreter.rename_cell(['edit_cell', old_name, new_name])

        return "true"

    @app.route("/recursion_check/", methods=["POST"])
    def recursion_check():
        data = request.get_json()
        cell_name = data['cell_name'].strip()

        nodes, _, edge_names = interpreter.graph.get_all_cells_edges()

        for e in edge_names:
            if e[0] == cell_name:
                return "warning"

        return "safe"

    @app.route("/root_has_outputs/", methods=["POST"])
    def root_output_check():
        c = 0

        nodes, _, edge_names = interpreter.graph.get_all_cells_edges()
        for e in edge_names:
            if e[0] == "root":
                c += 1

        if c > 0:
            return "safe"
        return "warning"

    @app.route("/link_cells/", methods=["POST"])
    def link_cells():
        data = request.get_json()
        first = data['first'].strip()
        second = data['second'].strip()

        if (first == second):
            return "false"

        interpreter.link(['link', first, second])

        return "true"

    @app.route("/bfs_execute/", methods=["POST"])
    def bfs_execute():
        interpreter.std_capture = StringIO()
        with redirect_stdout(interpreter.std_capture):
            interpreter.execute(["execute"])
        return "true"

    @app.route("/shutdown/", methods=["POST"])
    def shutdown():
        raise KeyboardInterrupt

    @app.route("/get_satx_text/", methods=["POST"])
    def get_satx_text():
        satx_txt = interpreter.graph.get_satx_as_txt()
        return satx_txt

    @app.route("/reset_runtime/", methods=["POST"])
    def reset_runtime():
        interpreter.reset_runtime()
        return "done"

    @app.route("/dupe_cell/", methods=["POST"])
    def dupe_cell():
        data = request.get_json()
        cell_name = data['cell_name'].strip()

        og_cell = interpreter.graph.get_cell(cell_name)

        new_cell = Cell(og_cell.name + "-copy", og_cell.content_type, og_cell.content, og_cell.stdout)
        interpreter.graph.add_cell(new_cell)

        return {'cell_name': new_cell.name,
                'content': new_cell.content,
                'content_type': new_cell.content_type}

    @app.route("/graph_has_name/", methods=["POST"])
    def check_for_graph_has_name():
        cell_name = request.get_json().strip()

        if cell_name in interpreter.graph.get_all_cells_edges()[0]:
            return "true"
        return "false"

    @app.route("/dynamic_cell_output/", methods=["GET"])
    def get_dynamic_cell_output():
        if interpreter.graph.executing:
            return interpreter.std_capture.getvalue()
        return "<!--SATYRN_DONE_EXECUTING-->" + interpreter.std_capture.getvalue() + (
            "<execution complete>" if len(interpreter.std_capture.getvalue()) > 0 else "")

    @app.route("/load_graph/", methods=["POST"])
    def load_graph():
        if request.get_json()['load_from_file']:
            interpreter.reset_graph(False)
            raw = request.get_json()['file_contents']
            content = raw.split("\n")
            interpreter.run_string(content)

        cell_names = interpreter.graph.get_all_cells_edges()[0]
        links = interpreter.graph.get_all_cells_edges()[1]

        names = []
        contents = []
        content_types = []
        outputs = []

        for cn in cell_names:
            cell = interpreter.graph.get_cell(cn)
            names.append(cn)
            contents.append(cell.content)
            content_types.append(cell.content_type)
            outputs.append(cell.output)

        return {'names': names,
                'contents': contents,
                'content_types': content_types,
                'links': links}

    @app.route("/set_as_md/", methods=["POST"])
    def set_as_md():
        cell_name = request.get_json()['cell_name']
        interpreter.graph.get_cell(cell_name).content_type = "markdown"

        return "true"

    @app.route("/set_as_py/", methods=["POST"])
    def set_as_py():
        cell_name = request.get_json()['cell_name']
        interpreter.graph.get_cell(cell_name).content_type = "python"

        return "true"

    @app.route("/reset_graph/", methods=["POST"])
    def reset_graph():
        interpreter.reset_graph(False)
        interpreter.create_cell(["create_cell", "root", "python", "n"])
        return "true"

    @app.route("/child_cell/", methods=["POST"])
    def add_child():
        parent_name = request.get_json()['parent_name'].strip()
        child_name = new_name()

        interpreter.create_cell(["create_cell", child_name, "python", "n"])
        interpreter.link(['link', parent_name, child_name])

        return child_name

    @app.route("/individual_execute/", methods=["POST"])
    def individual_execute():
        cell_name = request.get_json()['cell_name'].strip()
        with redirect_stdout(interpreter.std_capture):
            interpreter.execute(["execute", cell_name])

        return "true"

    @app.route("/clear_output/", methods=["POST"])
    def clear_dco():
        interpreter.std_capture = StringIO()

        return "true"

    @app.route("/get_py_text/", methods=["POST"])
    def get_py_text():
        py_txt = interpreter.graph.get_py_file()
        return py_txt

    return app
