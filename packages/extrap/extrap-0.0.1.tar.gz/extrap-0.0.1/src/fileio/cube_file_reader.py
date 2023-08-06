"""
This file is part of the Extra-P software (https://github.com/MeaParvitas/Extra-P)

Copyright (c) 2020,
Technische Universitaet Darmstadt, Germany
 
This software may be modified and distributed under the terms of
a BSD-style license. See the LICENSE file in the base
directory for details.
"""


from entities.parameter import Parameter
from entities.measurement import Measurement
from entities.coordinate import Coordinate
from entities.callpath import Callpath
from entities.metric import Metric
from entities.experiment import Experiment
from util.shared_library_interface import load_cube_interface
from fileio.io_helper import create_call_tree
from ctypes import *  # @UnusedWildImport
import os
import logging


class Data(Structure):
    _fields_ = [("num_metrics", c_int),("num_callpaths", c_int),("num_parameters", c_int),("num_coordinates", c_int),("mean", c_int)]


class ParameterValue():
    def __init__(self, parameter, value):
        self.parameter = parameter
        self.value = value
    def out(self):
        print(self.parameter+""+str(self.value))


def configure_prefix(dir_name):
    prefix = os.listdir(dir_name)[0]
    pos = prefix.find(".")
    prefix = prefix[:pos]
    return prefix


def configure_nr_parameters(dir_name):
    path = os.listdir(dir_name)[0]
    pos = path.find(".")
    path = path[pos+1:]
    pos = path.find(".r")
    parameter_values = path[:pos]
    parameter_values_list = parameter_values.split(sep=".")
    if len(parameter_values_list) == 1:
        return 1
    else:
        return len(parameter_values_list)


def configure_displayed_names(dir_name):
    displayed_names = os.listdir(dir_name)[0]
    pos = displayed_names.find(".")
    displayed_names = displayed_names[pos+1:]
    pos = displayed_names.find(".r")
    displayed_names = displayed_names[:pos]
    displayed_names = "".join([i for i in displayed_names if not i.isdigit()])
    pos = displayed_names.find(".")
    if pos != -1:
        displayed_names = displayed_names.replace(".", ",")
    if displayed_names[len(displayed_names)-1] == ",":
        displayed_names = displayed_names[:-1]
    return displayed_names
   
    
def configure_names(dir_name):
    configure_names = os.listdir(dir_name)[0]
    pos = configure_names.find(".")
    configure_names = configure_names[pos+1:]
    pos = configure_names.find(".r")
    configure_names = configure_names[:pos]
    configure_names = "".join([i for i in configure_names if not i.isdigit()])
    configure_names = "."+configure_names
    configure_names = configure_names.replace(".", ",#")
    configure_names = configure_names.replace("#", ".")
    configure_names = configure_names[1:]
    if configure_names[len(configure_names)-1] == ",":
        configure_names = configure_names[:-1]
    return configure_names


def configure_repetitions(dir_name):
    paths = os.listdir(dir_name)
    parameter_value_list = []
    for i in range(len(paths)):
        coordinate_string = paths[i]
        pos = coordinate_string.find(".")
        coordinate_string = coordinate_string[pos+1:]
        pos = coordinate_string.find(".r")
        coordinate_string = coordinate_string[:pos]
        if (parameter_value_list)==0:
            parameter_value_list.append(coordinate_string)
        else:
            in_list = False
            for j in range(len(parameter_value_list)):
                parameter_value_element = parameter_value_list[j]
                if coordinate_string == parameter_value_element:
                    in_list = True
                    break
            if in_list == False:
                parameter_value_list.append(coordinate_string)
    rep_map = {}
    for i in range(len(parameter_value_list)):
        item = parameter_value_list[i]
        rep_map[item] = 0
    for i in range(len(paths)):
        coordinate_string = paths[i]
        pos = coordinate_string.find(".")
        coordinate_string = coordinate_string[pos+1:]
        pos = coordinate_string.find(".r")
        coordinate_string = coordinate_string[:pos]
        rep_map[coordinate_string] += 1
    repetitions = rep_map[parameter_value_list[0]]
    return repetitions


def configure_parameter_values(dir_name, num_params):
    paths = os.listdir(dir_name)
    parameter_value_list = []
    coordinate_list = []
    for _ in range(num_params):
        coordinate_list.append([])
    for i in range(len(paths)):
        coordinate_string = paths[i]
        pos = coordinate_string.find(".")
        coordinate_string = coordinate_string[pos+1:]
        pos = coordinate_string.find(".r")
        coordinate_string = coordinate_string[:pos]
        parameter_value_list = coordinate_string.split(".")
        for i in range(num_params):
            if len(coordinate_list[i]) == 0:
                coordinate_list[i].append(parameter_value_list[i])
            else:
                in_list = False
                for j in range(len(coordinate_list[i])):
                    if parameter_value_list[i] == coordinate_list[i][j]:
                        in_list = True
                        break
                if in_list == False:
                    coordinate_list[i].append(parameter_value_list[i])
    coordinate_object_list = []
    for j in range(num_params):
        param_value_list = []
        for i in range(len(coordinate_list[j])):
            item = coordinate_list[j][i]
            parameter_name = "".join([i for i in item if not i.isdigit()])
            parameter_value = item.replace(",", ".")
            parameter_value = "".join([i for i in parameter_value if i.isdigit() or i == "."])
            parameter_value = float(parameter_value)
            param_value = ParameterValue(parameter_name, parameter_value)
            param_value_list.append(param_value)
        param_value_list.sort(key=lambda ParameterValue: ParameterValue.value, reverse=False)
        coordinate_object_list.append(param_value_list)
    parameter_value_string = ""
    for j in range(num_params):
        for i in range(len(coordinate_object_list[j])):
            item = coordinate_object_list[j][i]
            parameter_value_string += str(item.value) + ","
        parameter_value_string = parameter_value_string[:-1]
        parameter_value_string += ";"
    parameter_value_string = parameter_value_string[:-1]
    return parameter_value_string


def read_cube_file(dir_name, scaling_type):

    # set configuration for loading the cube files
    prefix = configure_prefix(dir_name)
    num_params = configure_nr_parameters(dir_name)
    postfix = ""
    filename = "profile.cubex"
    displayed_names = configure_displayed_names(dir_name)
    names = configure_names(dir_name)
    repetitions = configure_repetitions(dir_name)
    parameter_values = configure_parameter_values(dir_name, num_params)

    if scaling_type == 0:
        logging.debug("scaling type: weak")
    else:
        logging.debug("scaling type: strong")
        
    logging.debug("dir name: "+str(dir_name))
    logging.debug("prefix: "+str(prefix))
    logging.debug("post fix: "+str(postfix))
    logging.debug("filename: "+str(filename))
    logging.debug("repetitions: "+str(repetitions))
    logging.debug("num params: "+str(num_params))
    logging.debug("displayed names: "+str(displayed_names))
    logging.debug("names: "+str(names))
    logging.debug("parameter values: "+str(parameter_values))

    cube_interface = load_cube_interface()

    # encode string so they can be read by the c code as char*
    b_dir_name = dir_name.encode('utf-8')
    b_prefix = prefix.encode('utf-8')
    b_postfix = postfix.encode('utf-8')
    b_filename = filename.encode('utf-8')
    b_displayed_names = displayed_names.encode('utf-8')
    b_names = names.encode('utf-8')
    b_parameter_values = parameter_values.encode('utf-8')

    # pointer object for c++ data structure
    data_pointer = POINTER(Data)
    exposed_function = cube_interface.exposed_function
    exposed_function.restype = data_pointer

    # number of parameters
    getNumParameters = cube_interface.getNumParameters
    getNumParameters.restype = c_int

    # number of chars for one paramater
    getNumCharsParameters = cube_interface.getNumCharsParameters
    getNumCharsParameters.restype = c_int

    # parameters char
    getParameterChar = cube_interface.getParameterChar
    getParameterChar.restype = c_char

    # number of coordinates
    getNumCoordinates = cube_interface.getNumCoordinates
    getNumCoordinates.restype = c_int

    # number of chars for one coordinate
    getNumCharsCoordinates = cube_interface.getNumCharsCoordinates
    getNumCharsCoordinates.restype = c_int

    # coordinate char
    getCoordinateChar = cube_interface.getCoordinateChar
    getCoordinateChar.restype = c_char

    # callpaths char
    getCallpathChar = cube_interface.getCallpathChar
    getCallpathChar.restype = c_char
    
    # number of callpaths
    getNumCallpaths = cube_interface.getNumCallpaths
    getNumCallpaths.restype = c_int

    # number of chars for one callpath
    getNumCharsCallpath = cube_interface.getNumCharsCallpath
    getNumCharsCallpath.restype = c_int

    # number of metrics
    getNumMetrics = cube_interface.getNumMetrics
    getNumMetrics.restype = c_int

    # number of chars for one metric
    getNumCharsMetrics = cube_interface.getNumCharsMetrics
    getNumCharsMetrics.restype = c_int

    # metrics char
    getMetricChar = cube_interface.getMetricChar
    getMetricChar.restype = c_char

    # data point values
    getDataPointValue = cube_interface.getDataPointValue
    getDataPointValue.restype = c_double

    # get pointer to c++ data object for mean values
    dp = data_pointer()  # @UnusedVariable
    dp = exposed_function(scaling_type, b_dir_name, b_prefix, b_postfix, b_filename, repetitions, num_params, b_displayed_names, b_names, b_parameter_values, 1)
    
    # get pointer to c++ data object for median values
    dp2 = data_pointer()  # @UnusedVariable
    dp2 = exposed_function(scaling_type, b_dir_name, b_prefix, b_postfix, b_filename, repetitions, num_params, b_displayed_names, b_names, b_parameter_values, 0)
    
    # create an experiment object to save the date loaded from the cube file
    experiment = Experiment()

    number_parameters = getNumParameters(dp)
    
    if number_parameters >=1 and number_parameters <= 3:
        
        # get the parameters
        for element_id in range(number_parameters):
            num_chars = getNumCharsParameters(dp, element_id)
            parameter_string = ""
            for char_id in range(num_chars):
                byte_parameter = getParameterChar(dp, element_id, char_id)
                parameter_string += byte_parameter.decode('utf-8')
            logging.debug("Parameter "+str(element_id+1)+": "+parameter_string)
            # save the parameter in the experiment object
            parameter = Parameter(parameter_string)
            experiment.add_parameter(parameter)
    
        # get the coordinates
        number_coordinates = getNumCoordinates(dp)
        for element_id in range(number_coordinates):
            num_chars = getNumCharsCoordinates(dp, element_id)
            coordinate_string = ""
            for char_id in range(num_chars):
                byte_coordinate = getCoordinateChar(dp, element_id, char_id)
                coordinate_string += byte_coordinate.decode('utf-8')
            logging.debug("Coordinate "+str(element_id+1)+": "+coordinate_string)
            # save the coordinate in the experiment object
            coordinate = Coordinate()
            
            # if there is only a single parameter
            if number_parameters == 1:
                coordinate_string = coordinate_string[1:]
                coordinate_string = coordinate_string[:-1]
                pos = coordinate_string.find(",")
                parameter_name = coordinate_string[:pos]
                parameter_value = coordinate_string[pos+1:]
                parameter_value = float(parameter_value)
                parameter_id = experiment.get_parameter_id(parameter_name)
                parameter = experiment.get_parameter(parameter_id)
                coordinate.add_parameter_value(parameter, parameter_value)
            
            # when there are several parameters
            else:
                coordinate_string = coordinate_string[1:]
                coordinate_string = coordinate_string[:-1]
                coordinate_string = coordinate_string.replace(")(", ";")
                elements = coordinate_string.split(";")
                for element_id in range(len(elements)):
                    element = elements[element_id]
                    parts = element.split(",")
                    parameter_name = parts[0]
                    parameter_value = parts[1]
                    parameter_value = float(parameter_value)
                    parameter_id = experiment.get_parameter_id(parameter_name)
                    parameter = experiment.get_parameter(parameter_id)
                    coordinate.add_parameter_value(parameter, parameter_value)
                    
            experiment.add_coordinate(coordinate)
    
        # get the callpaths
        number_callpaths = getNumCallpaths(dp)
        for element_id in range(number_callpaths):
            num_chars = getNumCharsCallpath(dp, element_id)
            callpath_string = ""
            for char_id in range(num_chars):
                byte_callpath = getCallpathChar(dp, element_id, char_id)
                callpath_string += byte_callpath.decode('utf-8')
            logging.debug("Callpath "+str(element_id+1)+": "+callpath_string)
            # save the callpath in the experiment object
            callpath = Callpath(callpath_string)
            experiment.add_callpath(callpath)
            
        # create the call tree and add it to the experiment
        callpaths = experiment.get_callpaths()
        call_tree = create_call_tree(callpaths)
        experiment.add_call_tree(call_tree)
        
        # get the metrics
        number_metrics = getNumMetrics(dp)
        for element_id in range(number_metrics):
            num_chars = getNumCharsMetrics(dp, element_id)
            metric_string = ""
            for char_id in range(num_chars):
                byte_metric = getMetricChar(dp, element_id, char_id)
                metric_string += byte_metric.decode('utf-8')
            logging.debug("Metric "+str(element_id+1)+": "+metric_string)
            # save the metric in the experiment object
            metric = Metric(metric_string)
            experiment.add_metric(metric)
    
        # get the measurements per metric, callpath, coordinate (no repetitions, value is mean or median computed cube)  
        for metric_id in range(number_metrics):
            for callpath_id in range(number_callpaths):
                for coordinate_id in range(number_coordinates):
                    value_mean = getDataPointValue(dp, metric_id, callpath_id, coordinate_id)
                    value_mean = float(value_mean)
                    value_median = getDataPointValue(dp2, metric_id, callpath_id, coordinate_id)
                    value_median = float(value_median)
                    # save the measurement in the experiment object
                    measurement = Measurement(coordinate_id, callpath_id, metric_id, value_mean, value_median)
                    experiment.add_measurement(measurement)
                    logging.debug("Measurement: "+experiment.get_metric(metric_id).get_name()+", "+experiment.get_callpath(callpath_id).get_name()+", "+experiment.get_coordinate(coordinate_id).get_as_string()+": "+str(value_mean)+" (mean), "+str(value_median)+" (median)")
      
    else:
        logging.critical("This input format supports a maximum of 3 parameters.")
    
    return experiment

