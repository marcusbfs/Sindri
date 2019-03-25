import numpy as np
import matplotlib.pyplot as plt
from units import conv_unit


class VLEBinaryMixturePlot:
    def __init__(self, diagtype, var, x, y, varunit, title, plottype="both"):

        self.diagtype = diagtype
        self.var = var
        self.x = x
        self.y = y
        self.varunit = varunit
        self.title = title
        self.plottype = plottype

        self.fig, self.ax = plt.subplots()

        if self.diagtype == "isothermal":
            self.x_var_label = "Bubble pressure (x)"
            self.y_var_label = "Dew pressure (y)"
            self.var_paramater = "P"
        else:
            self.x_var_label = "Bubble temperature (x)"
            self.y_var_label = "Dew temperature (y)"
            self.var_paramater = "T"

        self.setGrid()
        self.setTitle(self.title)
        # self.ax.set_axisbelow(True)
        err = 0
        self.ax.set_xlim([-err, 1 + err])
        self.ax.set_ylabel("{} [{}]".format(self.var_paramater, self.varunit))

        self.selPlot(self.plottype)

    def setGrid(self):
        self.ax.grid()

    def setLegends(self):
        self.ax.legend()

    def setTitle(self, t):
        self.ax.set_title(t)

    def plot(self):
        plt.show()

    def selPlot(self, type):

        if type == "x":
            self.ax.plot(self.x, self.var, label=self.x_var_label, zorder=0)
            self.ax.set_xlabel("x1")
        elif type == "y":
            self.ax.plot(self.y, self.var, label=self.y_var_label, zorder=0)
            self.ax.set_xlabel("y1")
        else:
            self.ax.plot(self.x, self.var, label=self.x_var_label, zorder=0)
            self.ax.plot(self.y, self.var, label=self.y_var_label, zorder=0)
            self.ax.set_xlabel("x1, y1")
        self.setLegends()

    def expPlot(self, expfilename):
        import os

        type = self.plottype

        if os.path.exists(expfilename):
            import shlex

            with open(expfilename, "r") as file:
                try:
                    content = [line.rstrip("\n") for line in file if line != "\n"]
                    n_exp = len(content) - 1
                    var_exp = np.empty(n_exp, dtype=np.float64)
                    x_exp = np.empty(n_exp, dtype=np.float64)
                    y_exp = np.empty(n_exp, dtype=np.float64)
                    var_exp_unit = shlex.split(content[0])[0]

                    for i in range(n_exp):
                        ret3 = shlex.split(content[1 + i])
                        var_exp[i] = conv_unit(
                            float(ret3[0]), var_exp_unit, self.varunit
                        )
                        x_exp[i] = float(ret3[1])
                        y_exp[i] = float(ret3[2])

                except Exception as e:
                    raise ValueError("Error in experimental data\n" + str(e))

            x_exp_var_label = "Exp. data"
            y_exp_var_label = "Exp. data"

            color = "k"
            lw = 1.0
            zorder = 1
            fc = "none"

            if type == "x":
                self.ax.scatter(
                    x_exp,
                    var_exp,
                    label=x_exp_var_label,
                    color=color,
                    linewidths=lw,
                    zorder=zorder,
                    facecolors=fc,
                    edgecolors=color,
                )
            elif type == "y":
                self.ax.scatter(
                    y_exp,
                    var_exp,
                    label=y_exp_var_label,
                    color=color,
                    linewidths=lw,
                    zorder=zorder,
                    facecolors=fc,
                    edgecolors=color,
                )
            else:
                self.ax.scatter(
                    x_exp,
                    var_exp,
                    label=x_exp_var_label,
                    color=color,
                    linewidths=lw,
                    zorder=zorder,
                    facecolors=fc,
                    edgecolors=color,
                )
                self.ax.scatter(
                    y_exp,
                    var_exp,
                    label=y_exp_var_label,
                    color=color,
                    linewidths=lw,
                    zorder=zorder,
                    facecolors=fc,
                    edgecolors=color,
                )
            self.setLegends()
        else:
            raise ValueError("Invalid file")
