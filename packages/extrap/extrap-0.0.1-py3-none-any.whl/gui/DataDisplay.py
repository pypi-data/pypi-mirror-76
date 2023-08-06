"""
This file is part of the Extra-P software (http://www.scalasca.org/software/extra-p)

Copyright (c) 2020,
Technische Universitaet Darmstadt, Germany
 
This software may be modified and distributed under the terms of
a BSD-style license.  See the COPYING file in the package base
directory for details.
"""


try:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
except ImportError:
    from PyQt5.QtGui import *  # @UnusedWildImport
    from PyQt5.QtCore import *  # @UnusedWildImport
    from PyQt5.QtWidgets import *  # @UnusedWildImport

from gui.GraphWidget import GraphWidget
from gui.HeatMapGraphWidget import HeatMapGraphWidget
from gui.IsolinesDisplayWidget import IsolinesDisplayWidget
from gui.InterpolatedContourDisplayWidget import InterpolatedContourDisplayWidget
from gui.MeasurementPointsPlotWidget import MeasurementPointsPlotWidget
from gui.AllFunctionsAsOneSurfacePlotWidget import AllFunctionsAsOneSurfacePlotWidget
from gui.AllFunctionsAsDifferentSurfacePlotWidget import AllFunctionsAsDifferentSurfacePlotWidget
from gui.DominatingFunctionsAsSingleScatterPlotWidget import DominatingFunctionsAsSingleScatterPlotWidget
from gui.MaxZAsSingleSurfacePlotWidget import MaxZAsSingleSurfacePlotWidget
from entities.parameter import Parameter


#####################################################################
class AxisSelection(QWidget):
    ''' This class is a helper class for the class DataDisplay.
        It represents one parameter in the data display which
        shown on one of the graph axis. It allows to set the maximum
        value for the axis in the graph.
    '''
#####################################################################

    max_x = 10
    max_y = 10
    max_y = 10

    def __init__(self, manager, parent, index, parameters):
        super(AxisSelection, self).__init__(parent)
        self.manager = manager
        self.index = index
        self.initUI(parameters)
        self.updateDisplay()

    def initUI(self, parameters):
        self.grid = QGridLayout(self)
        if self.index == 0:
            label1 = QLabel("X-axis")
            #label1.setMinimumWidth( 50 )
            #label1.setMinimumHeight( 75 )
        elif self.index == 1:
            label1 = QLabel("Y-axis")
        elif self.index == 2:
            label1 = QLabel("Z-axis")
        else:
            label1 = QLabel("Axis " + str(self.index))

        self.combo_box = QComboBox(self)
        #self.combo_box.setMinimumWidth( 75 )
        self.combo_box.setMinimumHeight(20)
        for i in range(0, len(parameters)):
            self.combo_box.addItem(parameters[i].get_name())
        self.combo_box.setCurrentIndex(self.index)
        self.old_name = self.combo_box.currentText()
        self.combo_box.currentIndexChanged.connect(self.parameter_selected)

        label2 = QLabel("           max.")
        self.max_edit = QSpinBox()
        self.max_edit.setMinimum(1)
        self.max_edit.setMinimumHeight(20)
        self.max_edit.setMaximum(10000000)
        if self.index == 0:
            self.max_edit.setValue(AxisSelection.max_x)
        elif self.index == 1:
            self.max_edit.setValue(AxisSelection.max_y)
        elif self.index == 2:
            self.max_edit.setValue(AxisSelection.max_z)
        else:
            self.max_edit.setValue(10)
        #self.max_edit.setValue( 10 )
        self.max_edit.valueChanged.connect(self.max_changed)

        self.grid.addWidget(label1, 0, 0)
        self.grid.addWidget(self.combo_box, 0, 1)
        self.grid.addWidget(label2, 0, 2)
        self.grid.addWidget(self.max_edit, 0, 3)

        self.setLayout(self.grid)
        self.setMaximumHeight(40)
        self.show()

    def updateDisplay(self):
        display = self.manager.display_widget.currentWidget()
        display.setMax(self.index, float(self.max_edit.text()))

    def max_changed(self):
        ''' This function should only be called from the connected event
            when the user has entered a new value.
            Otherwise use maxChanged() which does not update the graph drawing.
            This is to avoid multiple updates of the graph.
        '''
        self.maxChanged()
        display = self.manager.display_widget.currentWidget()
        if isinstance(display, GraphWidget):
            display.update()
        else:
            display.drawGraph()
            display.update()

    def maxChanged(self):
        ''' This function updates the max value without redrawing the graph.
            Use this function from external calls to avoid multiple redraws
            of the graph.
        '''
        display = self.manager.display_widget.currentWidget()

        if self.index == 0:
            AxisSelection.max_x = float(self.max_edit.text())
        elif self.index == 1:
            AxisSelection.max_y = float(self.max_edit.text())
        elif self.index == 2:
            AxisSelection.max_z = float(self.max_edit.text())

        display.setMax(self.index, float(self.max_edit.text()))

    def clearAxisLayout(self):
        if self.grid is not None:
            while self.grid.count():
                item = self.grid.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def setMax(self, axis, maxValue):

        if axis == 0:
            self.max_x = maxValue
            self.max_edit.setValue(self.max_x)
        elif axis == 1:
            self.max_y = maxValue
            self.max_edit.setValue(self.max_y)
        elif axis == 2:
            self.max_z = maxValue
            self.max_edit.setValue(self.max_z)

    def getParameter(self):
        return Parameter(self.combo_box.currentText())

    def parameter_selected(self):
        new_name = self.combo_box.currentText()
        self.manager.parameterSelected(self.index,
                                       new_name,
                                       self.old_name)
        self.old_name = self.combo_box.currentText()

    def getValue(self):
        return float(self.max_edit.text())

    def switchParameter(self, newParam):
        i = self.combo_box.findText(newParam, Qt.MatchExactly)
        self.combo_box.setCurrentIndex(i)


#####################################################################
class ValueSelection(QWidget):
    ''' This class represents a Parameter in the data display that
        is not shown of one of the axis. It allows to select a value
        for this parameter.
        It is a helper class for the class DataDisplay.
    '''
#####################################################################

    def __init__(self, manager, parent, parameter):
        super(ValueSelection, self).__init__(parent)
        self.manager = manager
        self.parameter = parameter
        self.initUI()
        self.show()

    def initUI(self):
        self.grid = QGridLayout(self)

        label0 = QLabel("Parameter:")
        label0.setMinimumWidth(100)
        self.parameter_label = QLabel(self.parameter)
        self.parameter_label.setMinimumWidth(100)
        label2 = QLabel("Value: ")
        label2.setMinimumWidth(50)

        self.value_edit = QSpinBox()
        self.value_edit.setMinimum(1)
        self.value_edit.setMaximum(10000000)
        self.value_edit.setValue(10)

        self.grid.addWidget(label0, 0, 0)
        self.grid.addWidget(self.parameter_label, 0, 1)
        self.grid.addWidget(label2, 0, 2)
        self.grid.addWidget(self.value_edit, 0, 3)
        self.setLayout(self.grid)
        self.setMaximumHeight(30)

    def getValue(self):
        return float(self.value_edit.text())

    def setValue(self, value):
        self.value_edit.setValue(value)

    def setName(self, name):
        self.parameter = name
        self.parameter_label.setText(name)

    def clearRowLayout(self):
        if self.grid is not None:
            while self.grid.count():
                item = self.grid.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())


#####################################################################
class DataDisplayManager(QWidget):
    """ This class manages the different data views and display
        options.
        To add a new display:
        1. It must be a class derived from QWidget.
        2. It must implement a function getNumAxis() that returns
           the number of free parameters of the display
        3. It must implement a function setMax( axis, value ) where
           axis is the index of the axis that is changed. 0 is the X-axis
           1 is the Y-axis, 2 is the Z-axis. And value is the new max value.
        4. Add it to self.display_widget via addTab()
        5. For evaluation of functions retrieve the value if fixed parameters
           with getValues()
    """
#####################################################################

    def __init__(self, main_widget, parent):
        super(DataDisplayManager, self).__init__(parent)
        self.main_widget = main_widget
        self.axis_selections = list()
        self.value_selections = list()
        self.initUI()

    def initUI(self):
        grid = QGridLayout(self)
        splitter = QSplitter(Qt.Vertical, self)
        grid.addWidget(splitter, 0, 0)
        self.display_widget = QTabWidget(splitter)
        self.display_widget.setMovable(True)
        self.display_widget.setTabsClosable(True)
        self.display_widget.tabCloseRequested.connect(self.closeTab)

        # loading this tab as default view (Line graph)
        self.reloadTabs([0])

        self.display_widget.tabsClosable()
        self.display_widget.currentChanged.connect(self.experimentChange)
        widget = QWidget(splitter)
        self.grid = QGridLayout(widget)
        splitter.setSizes([1000, 40])
        self.show()

    def closeTab(self, currentIndex):
        self.display_widget.removeTab(currentIndex)

    def ifTabAlreadyOpened(self, text):
        tabStatus = False
        tabCount = self.display_widget.count()
        for index in range(0, (tabCount)):
            if (text == self.display_widget.tabText(index)):
                tabStatus = True

        return tabStatus

    def reloadTabs(self, selectedCheckBoxesIndex):
        # 0: Line Graph,
        # 1: AllFunctionsAsOneSurfacePlotWidget,
        # 2 :AllFunctionsAsDifferentSurfacePlotWidget
        # 3: DominatingFunctionsAsSingleScatterPlotWidget,
        # 4: MaxZAsSingleSurfacePlotWidget
        # 5: HeatMapGraphWidget,
        # 6: IsolinesDisplayWidget
        # 7: InterpolatedContourDisplayWidget
        # 8: Measurement Points

        if (0 in selectedCheckBoxesIndex):
            labelText = "Line graph"
            tabStatus = self.ifTabAlreadyOpened(labelText)
            if tabStatus is False:
                graph = GraphWidget(self.main_widget, self)
                self.display_widget.addTab(graph, labelText)

        if (1 in selectedCheckBoxesIndex):
            labelText = "SurfacePlot_All"
            tabStatus = self.ifTabAlreadyOpened(labelText)
            if tabStatus is False:
                allFunctionsAsOneSurfacePlotGraph = AllFunctionsAsOneSurfacePlotWidget(
                    self.main_widget, self)
                self.display_widget.addTab(
                    allFunctionsAsOneSurfacePlotGraph, labelText)

        if (2 in selectedCheckBoxesIndex):
            labelText = "SurfacePlot_Single"
            tabStatus = self.ifTabAlreadyOpened(labelText)
            if tabStatus is False:
                allFunctionsAsDifferntSurfacePlotGraph = AllFunctionsAsDifferentSurfacePlotWidget(
                    self.main_widget, self)
                self.display_widget.addTab(
                    allFunctionsAsDifferntSurfacePlotGraph, labelText)

        if (3 in selectedCheckBoxesIndex):
            labelText = "ScatterPlot_Dominating"
            tabStatus = self.ifTabAlreadyOpened(labelText)
            if tabStatus is False:
                dominatingFunctionsAsSingleScatterPlotWidget = DominatingFunctionsAsSingleScatterPlotWidget(
                    self.main_widget, self)
                self.display_widget.addTab(
                    dominatingFunctionsAsSingleScatterPlotWidget, labelText)

        if (4 in selectedCheckBoxesIndex):
            labelText = "SurfacePlot_MaxZ"
            tabStatus = self.ifTabAlreadyOpened(labelText)
            if tabStatus is False:
                maxZAsSingleSurfacePlotWidget = MaxZAsSingleSurfacePlotWidget(
                    self.main_widget, self)
                self.display_widget.addTab(
                    maxZAsSingleSurfacePlotWidget, labelText)

        if (5 in selectedCheckBoxesIndex):
            labelText = "Heat Map"
            tabStatus = self.ifTabAlreadyOpened(labelText)
            if tabStatus is False:
                heatMapGraph = HeatMapGraphWidget(self.main_widget, self)
                self.display_widget.addTab(heatMapGraph, labelText)

        if (6 in selectedCheckBoxesIndex):
            labelText = "Contour Plot"
            tabStatus = self.ifTabAlreadyOpened(labelText)
            if tabStatus is False:
                isolinesGraph = IsolinesDisplayWidget(self.main_widget, self)
                self.display_widget.addTab(isolinesGraph, labelText)

        if (7 in selectedCheckBoxesIndex):
            labelText = "Interpolated Contour"
            tabStatus = self.ifTabAlreadyOpened(labelText)
            if tabStatus is False:
                interpolatedContourGraph = InterpolatedContourDisplayWidget(
                    self.main_widget, self)
                self.display_widget.addTab(interpolatedContourGraph, labelText)

        if (8 in selectedCheckBoxesIndex):
            labelText = "Measurement Points"
            tabStatus = self.ifTabAlreadyOpened(labelText)
            if tabStatus is False:
                measurementPointGraph = MeasurementPointsPlotWidget(
                    self.main_widget, self)
                self.display_widget.addTab(measurementPointGraph, labelText)

    def generateSelections(self, parameters):

        if not self.display_widget.currentWidget():
            return

        num_axis = self.display_widget.currentWidget().getNumAxis()
        for axis in self.axis_selections:
            axis.clearAxisLayout()
        del self.axis_selections[:]

        for v in self.value_selections:
            v.clearRowLayout()
        del self.value_selections[:]

        for i in range(0, num_axis):
            axis_selection = AxisSelection(self, self, i, parameters)
            self.axis_selections.append(axis_selection)
            self.grid.addWidget(axis_selection, i, 0)
        num_param = len(parameters)
        for i in range(num_axis, num_param):
            value_selection = ValueSelection(self, self,
                                             parameters[i].getName())
            self.value_selections.append(value_selection)
            self.grid.addWidget(value_selection, i, 0)

    def experimentChange(self):
        experiment = self.main_widget.getExperiment()
        if experiment == None:
            return
        parameters = experiment.get_parameters()
        self.generateSelections(parameters)
        self.updateWidget()

    def setMaxValue(self, index, value):
        if index < len(self.axis_selections):
            self.axis_selections[index].max_edit.setValue(value)

    # TODO: fix this
    #def getValues(self):
    #    pv_list = EXTRAP.ParameterValueList()
    #    for i in self.value_selections:
    #        pv_list[EXTRAP.Parameter(i.parameter)] = i.getValue()
    #    return pv_list

    def getAxisParameter(self, index):
        return self.axis_selections[index].getParameter()

    def parameterSelected(self, index, newName, oldName):
        old_value = self.axis_selections[index].getValue()
        for i in self.axis_selections:
            if i.index != index:
                if i.getParameter().getName() == newName:
                    self.setMaxValue(index, i.getValue())
                    self.setMaxValue(i.index, old_value)
                    i.switchParameter(oldName)
                    i.maxChanged()
                    self.axis_selections[index].maxChanged()
                    self.updateWidget()
                    return
        for i in self.value_selections:
            if i.parameter == newName:
                i.setName(oldName)
                self.setMaxValue(index, i.getValue())
                i.setValue(old_value)
                self.axis_selections[index].maxChanged()
                self.updateWidget()
                return

    def updateWidget(self):
        display = self.display_widget.currentWidget()
        if not display:
            return
        if isinstance(display, GraphWidget):
            display.update()
        else:
            display.drawGraph()
