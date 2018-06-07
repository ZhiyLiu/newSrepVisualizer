import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
from Lib.legacyTransformer import legacyTransformer as transformer
from Lib import *
import numpy as np
import xml.etree.ElementTree as ET
import math
#
# visualize new srep format
#

class visualizer(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "visualizer"  # TODO make this more human readable by adding spaces
        self.parent.categories = ["Examples"]
        self.parent.dependencies = []
        self.parent.contributors = ["John Doe (AnyWare Corp.)"]  # replace with "Firstname Lastname (Organization)"
        self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    It performs a simple thresholding on the input volume and optionally captures a screenshot.
    """
        self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
"""  # replace with organization, grant and thanks.


#
# visualizerWidget
#

class visualizerWidget(ScriptedLoadableModuleWidget):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)

        # Instantiate and connect widgets ...

        #
        # Parameters Area
        #
        parametersCollapsibleButton = ctk.ctkCollapsibleButton()
        parametersCollapsibleButton.text = "Parameters"
        self.layout.addWidget(parametersCollapsibleButton)

        # Layout within the dummy collapsible button
        parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

        #
        # input volume selector
        #
        # self.inputSelector = slicer.qMRMLNodeComboBox()
        # self.inputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        # self.inputSelector.selectNodeUponCreation = True
        # self.inputSelector.addEnabled = False
        # self.inputSelector.removeEnabled = False
        # self.inputSelector.noneEnabled = False
        # self.inputSelector.showHidden = False
        # self.inputSelector.showChildNodeTypes = False
        # self.inputSelector.setMRMLScene(slicer.mrmlScene)
        # self.inputSelector.setToolTip("Pick the input to the algorithm.")
        # parametersFormLayout.addRow("Input Volume: ", self.inputSelector)

        # set distance of fold curve from interior points
        self.distSlider = slicer.qMRMLSliderWidget()
#        self.distSlider.setMaximum(0.6)
#        self.distSlider.setMinimum(0.0)
        self.distSlider.setProperty('maximum', 0.6)
        self.distSlider.setProperty('minimum', 0.0)
        self.distSlider.setProperty('singleStep', 0.01)
#        self.distSlider.setValue(0.02)

        self.distSlider.setToolTip("Parameter used in transformation from legacy s-rep to new s-rep")
        parametersFormLayout.addRow("Set distance to expand fold curve", self.distSlider)
        
        #
        # Apply Button
        #
        self.applyButton = qt.QPushButton("Select s-rep file")
        self.applyButton.toolTip = "Run the algorithm."
        parametersFormLayout.addRow(self.applyButton)

        self.boundarySurfaceRendering = qt.QCheckBox()
        self.boundarySurfaceRendering.checked = 0
        self.boundarySurfaceRendering.setToolTip("If checked, set the visibility of the boundary mesh")
        parametersFormLayout.addRow("Show Boundary Mesh", self.boundarySurfaceRendering)

        # connections
        self.applyButton.connect('clicked(bool)', self.onApplyButton)
        # Add vertical spacer
        self.layout.addStretch(1)


    def cleanup(self):
        pass

    def onApplyButton(self):
        logic = visualizerLogic()
        flag = self.boundarySurfaceRendering.checked
        dist = self.distSlider.value
        logic.run(flag,dist)


#
# visualizerLogic
#

class visualizerLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
    computation done by your module.  The interface
    should be such that other python code can import
    this class and make use of the functionality without
    requiring an instance of the Widget.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def hasImageData(self, volumeNode):
        """This is an example logic method that
        returns true if the passed in volume
        node has valid image data
        """
        if not volumeNode:
            logging.debug('hasImageData failed: no volume node')
            return False
        if volumeNode.GetImageData() is None:
            logging.debug('hasImageData failed: no image data in volume node')
            return False
        return True

    def takeScreenshot(self, name, description, type=-1):
        # show the message even if not taking a screen shot
        slicer.util.delayDisplay(
            'Take screenshot: ' + description + '.\nResult is available in the Annotations module.', 3000)

        lm = slicer.app.layoutManager()
        # switch on the type to get the requested window
        widget = 0
        if type == slicer.qMRMLScreenShotDialog.FullLayout:
            # full layout
            widget = lm.viewport()
        elif type == slicer.qMRMLScreenShotDialog.ThreeD:
            # just the 3D window
            widget = lm.threeDWidget(0).threeDView()
        elif type == slicer.qMRMLScreenShotDialog.Red:
            # red slice window
            widget = lm.sliceWidget("Red")
        elif type == slicer.qMRMLScreenShotDialog.Yellow:
            # yellow slice window
            widget = lm.sliceWidget("Yellow")
        elif type == slicer.qMRMLScreenShotDialog.Green:
            # green slice window
            widget = lm.sliceWidget("Green")
        else:
            # default to using the full window
            widget = slicer.util.mainWindow()
            # reset the type so that the node is set correctly
            type = slicer.qMRMLScreenShotDialog.FullLayout

        # grab and convert to vtk image data
        qpixMap = qt.QPixmap().grabWidget(widget)
        qimage = qpixMap.toImage()
        imageData = vtk.vtkImageData()
        slicer.qMRMLUtils().qImageToVtkImageData(qimage, imageData)

        annotationLogic = slicer.modules.annotations.logic()
        annotationLogic.CreateSnapShot(name, description, type, 1, imageData)


    def computeIndex(self, i, j, numRows, numCols):
        atomIndex = numCols * i  + j
        numEndAtoms = 0
        numStdAtoms = 0

    def distance(self, p0, p1):
        return math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2 + (p0[2] - p1[2]) ** 2 )

    def visualizeNewSrep(self, filename):
        # 1. parse header file
        tree = ET.parse(filename)
        upFileName = ''
        crestFileName = ''
        downFileName = ''
        nCols = 0
        nRows = 0
        for child in tree.getroot():
            if child.tag == 'upSpoke':
                upFileName = child.text
            elif child.tag == 'downSpoke':
                downFileName = child.text
            elif child.tag == 'crestSpoke':
                crestFileName = child.text
            elif child.tag == 'nRows':
                nRows = (int)(child.text)
            elif child.tag == 'nCols':
                nCols = (int)(child.text)

        reader = vtk.vtkXMLPolyDataReader()
        reader.SetFileName(upFileName)
        reader.Update()

        upSpokes = reader.GetOutput()

        upPointData = upSpokes.GetPointData()
        medial_polyData = upSpokes # this is poly data for skeleton

        scene = slicer.mrmlScene

        # base line of medial sheet
        fidDisplayNode = slicer.vtkMRMLMarkupsDisplayNode()
        scene.AddNode(fidDisplayNode)
        fidNode = slicer.vtkMRMLMarkupsFiducialNode()
        fidDisplayNode.SetGlyphScale(0.01)
        fidDisplayNode.SetSelectedColor(1.0, 1.0, 0.0)
        fidDisplayNode.SetTextScale(0.0)
        scene.AddNode(fidNode)
        fidNode.SetAndObserveDisplayNodeID(fidDisplayNode.GetID())
        # \TODO come up with better name later

        # prepare for arrows for upspokes
        upSpoke_points = vtk.vtkPoints()
        upSpoke_lines = vtk.vtkCellArray()

        arr_length = upPointData.GetArray('spokeLength')
        arr_dirs = upPointData.GetArray('spokeDirection')
        for i in range(upSpokes.GetNumberOfPoints()):
            pt = [0]* 3
            upSpokes.GetPoint(i, pt)
            # base point of up arrows
            id0 = upSpoke_points.InsertNextPoint(pt)

            # head of up arrows
            spoke_length = arr_length.GetValue(i)
            baseIdx = i * 3
            dirX = arr_dirs.GetValue(baseIdx)
            dirY = arr_dirs.GetValue(baseIdx + 1)
            dirZ = arr_dirs.GetValue(baseIdx + 2)
            pt1 = [0] * 3
            pt1[0] = pt[0] + spoke_length * dirX
            pt1[1] = pt[1] + spoke_length * dirY
            pt1[2] = pt[2] + spoke_length * dirZ
            id1 = upSpoke_points.InsertNextPoint(pt1)

            up_arrow = vtk.vtkLine()
            up_arrow.GetPointIds().SetId(0, id0)
            up_arrow.GetPointIds().SetId(1, id1)
            upSpoke_lines.InsertNextCell(up_arrow)

            fidNode.AddFiducial(pt[0], pt[1], pt[2])

        boundary_point_ids = []

        # model node for medial mesh
        medial_model = slicer.vtkMRMLModelNode()
        medial_model.SetScene(scene)
        medial_model.SetName("Medial Mesh")
        medial_model.SetAndObservePolyData(reader.GetOutput())
        # model display node for the medial mesh
        medial_model_display = slicer.vtkMRMLModelDisplayNode()
        medial_model_display.SetColor(0, 0.5, 0)
        medial_model_display.SetScene(scene)
        medial_model_display.SetLineWidth(3.0)
        medial_model_display.SetRepresentation(1)
        medial_model_display.SetBackfaceCulling(0)
        scene.AddNode(medial_model_display)
        medial_model.SetAndObserveDisplayNodeID(medial_model_display.GetID())
        scene.AddNode(medial_model)

        # model node for up spoke (poly data for arrows)
        upSpoke_polyData = vtk.vtkPolyData()
        upSpoke_polyData.SetPoints(upSpoke_points)
        upSpoke_polyData.SetLines(upSpoke_lines)

        upSpoke_model = slicer.vtkMRMLModelNode()
        upSpoke_model.SetScene(scene)
        upSpoke_model.SetName("Top Spoke")
        upSpoke_model.SetAndObservePolyData(upSpoke_polyData)
        # model display node for the top spoke
        # cyan for the top spoke
        upSpoke_model_display = slicer.vtkMRMLModelDisplayNode()
        upSpoke_model_display.SetColor(0, 1, 1)
        upSpoke_model_display.SetScene(scene)
        upSpoke_model_display.SetLineWidth(3.0)
        upSpoke_model_display.SetBackfaceCulling(0)
        scene.AddNode(upSpoke_model_display)
        upSpoke_model.SetAndObserveDisplayNodeID(upSpoke_model_display.GetID())
        scene.AddNode(upSpoke_model)

        # prepare for down spokes
        reader.SetFileName(downFileName)
        reader.Update()
        downSpokes = reader.GetOutput()

        downSpoke_polyData = vtk.vtkPolyData()
        downSpoke_lines = vtk.vtkCellArray()
        downSpoke_points = vtk.vtkPoints()

        downPointData = downSpokes.GetPointData()
        arr_length = downPointData.GetArray('spokeLength')
        arr_dirs = downPointData.GetArray('spokeDirection')
        for i in range(downSpokes.GetNumberOfPoints()):
            # tail of arrows
            pt_tail = [0] * 3
            downSpokes.GetPoint(i, pt_tail)
            id0 = downSpoke_points.InsertNextPoint(pt_tail)

            # head of arrows
            pt_head = [0] * 3
            spoke_length = arr_length.GetValue(i)
            baseIdx = i * 3
            dirX = arr_dirs.GetValue(baseIdx)
            dirY = arr_dirs.GetValue(baseIdx+1)
            dirZ = arr_dirs.GetValue(baseIdx+2)
            pt_head[0] = pt_tail[0] + spoke_length * dirX
            pt_head[1] = pt_tail[1] + spoke_length * dirY
            pt_head[2] = pt_tail[2] + spoke_length * dirZ
            id1 = downSpoke_points.InsertNextPoint(pt_head)

            # connection between head and tail
            con = vtk.vtkLine()
            con.GetPointIds().SetId(0, id0)
            con.GetPointIds().SetId(1, id1)
            downSpoke_lines.InsertNextCell(con)

        downSpoke_polyData.SetPoints(downSpoke_points)
        downSpoke_polyData.SetLines(downSpoke_lines)

        downSpoke_model = slicer.vtkMRMLModelNode()
        downSpoke_model.SetScene(scene)
        downSpoke_model.SetName("Bottom Spoke")
        downSpoke_model.SetAndObservePolyData(downSpoke_polyData)
        # model display node for the down spoke
        downSpoke_model_display = slicer.vtkMRMLModelDisplayNode()
        downSpoke_model_display.SetColor(1, 0, 1)
        downSpoke_model_display.SetScene(scene)
        downSpoke_model_display.SetLineWidth(3.0)
        downSpoke_model_display.SetBackfaceCulling(0)
        scene.AddNode(downSpoke_model_display)
        downSpoke_model.SetAndObserveDisplayNodeID(downSpoke_model_display.GetID())
        scene.AddNode(downSpoke_model)

        # crest spoke
        new_reader = vtk.vtkXMLPolyDataReader()
        new_reader.SetFileName(crestFileName)
        new_reader.Update()
        foldCurve_polyData = new_reader.GetOutput()
        foldPointData = foldCurve_polyData.GetPointData()
        arr_length = foldPointData.GetArray('spokeLength')
        arr_dirs = foldPointData.GetArray('spokeDirection')
        crest_arrows_polydata = vtk.vtkPolyData()
        crest_arrows_points = vtk.vtkPoints()
        crest_arrows_lines = vtk.vtkCellArray()
        for i in range(foldCurve_polyData.GetNumberOfPoints()):
            # tail of crest arrows
            pt_tail = [0] * 3
            foldCurve_polyData.GetPoint(i, pt_tail)
            id0 = crest_arrows_points.InsertNextPoint(pt_tail)

            # head of crest arrows
            pt_head = [0] * 3
            spoke_length = arr_length.GetValue(i)
            baseIdx = i * 3
            dirX = arr_dirs.GetValue(baseIdx)
            dirY = arr_dirs.GetValue(baseIdx + 1)
            dirZ = arr_dirs.GetValue(baseIdx + 2)
            pt_head[0] = pt_tail[0] + spoke_length * dirX
            pt_head[1] = pt_tail[1] + spoke_length * dirY
            pt_head[2] = pt_tail[2] + spoke_length * dirZ
            id1 = crest_arrows_points.InsertNextPoint(pt_head)

            crest_line = vtk.vtkLine()
            crest_line.GetPointIds().SetId(0, id0)
            crest_line.GetPointIds().SetId(1, id1)
            crest_arrows_lines.InsertNextCell(crest_line)

        crest_arrows_polydata.SetPoints(crest_arrows_points)
        crest_arrows_polydata.SetLines(crest_arrows_lines)

        # show crest arrows
        crestSpoke_model = slicer.vtkMRMLModelNode()
        crestSpoke_model.SetScene(scene)
        crestSpoke_model.SetName("Crest Spoke")
        crestSpoke_model.SetAndObservePolyData(crest_arrows_polydata)
        # model display node 
        crestSpoke_model_display = slicer.vtkMRMLModelDisplayNode()
        crestSpoke_model_display.SetColor(1, 1, 0)
        crestSpoke_model_display.SetScene(scene)
        crestSpoke_model_display.SetLineWidth(3.0)
        crestSpoke_model_display.SetBackfaceCulling(0)
        scene.AddNode(crestSpoke_model_display)
        crestSpoke_model.SetAndObserveDisplayNodeID(crestSpoke_model_display.GetID())
        scene.AddNode(crestSpoke_model)

        # show fold curve
        foldCurve_model = slicer.vtkMRMLModelNode()
        foldCurve_model.SetScene(scene)
        foldCurve_model.SetName("Fold Curve")
        foldCurve_model.SetAndObservePolyData(foldCurve_polyData)
        # model display node 
        foldCurve_model_display = slicer.vtkMRMLModelDisplayNode()
        foldCurve_model_display.SetColor(1, 1, 0)
        foldCurve_model_display.SetScene(scene)
        foldCurve_model_display.SetLineWidth(3.0)
        foldCurve_model_display.SetBackfaceCulling(0)
        scene.AddNode(foldCurve_model_display)
        foldCurve_model.SetAndObserveDisplayNodeID(foldCurve_model_display.GetID())
        scene.AddNode(foldCurve_model)

        # show connections to fold curve point from nearby interior points
        # compute the nearest interior point
        connection_polydata = vtk.vtkPolyData()
        connection_points = vtk.vtkPoints()
        connection_lines = vtk.vtkCellArray()
        for i in range(foldCurve_polyData.GetNumberOfPoints()):
            min_dist = 100000.0
            nearest_index = 0
            pt_fold = [0] * 3
            foldCurve_polyData.GetPoint(i, pt_fold)
            id0 = connection_points.InsertNextPoint(pt_fold)
            
            for j in range(upSpokes.GetNumberOfPoints()):
                pt_interior = [0]* 3
                upSpokes.GetPoint(j, pt_interior)
                dist = math.sqrt((pt_fold[0] - pt_interior[0]) ** 2 + (pt_fold[1] - pt_interior[1]) ** 2 + (pt_fold[2] - pt_interior[2]) ** 2 )
                if dist < min_dist:
                    min_dist = dist
                    nearest_index = j

            pt_nearest_interior = upSpokes.GetPoint(nearest_index)
            id1 = connection_points.InsertNextPoint(pt_nearest_interior)
            line = vtk.vtkLine()

            line.GetPointIds().SetId(0, id0)
            line.GetPointIds().SetId(1, id1)

            connection_lines.InsertNextCell(line)

        connection_polydata.SetPoints(connection_points)
        connection_polydata.SetLines(connection_lines)
        connection_model = slicer.vtkMRMLModelNode()
        connection_model.SetScene(scene)
        connection_model.SetName("Connection to Fold Curve")
        connection_model.SetAndObservePolyData(connection_polydata)
        # model display node 
        connection_model_display = slicer.vtkMRMLModelDisplayNode()
        connection_model_display.SetColor(0, 0, 0)
        connection_model_display.SetScene(scene)
        connection_model_display.SetLineWidth(3.0)
        connection_model_display.SetBackfaceCulling(0)
        scene.AddNode(connection_model_display)
        connection_model.SetAndObserveDisplayNodeID(connection_model_display.GetID())
        scene.AddNode(connection_model)

    def run(self,renderFlag, dist):

        logging.info("distance:"+ str(dist))
        """
        Run the actual algorithm
        """
        filename = qt.QFileDialog.getOpenFileName()
        if filename == '':
            logging.error('Input file name is empty')
            return False
        
        logging.info('Processing started')
        if filename.endswith('.m3d'):
            if dist == 0.0:
                qt.QMessageBox.information(slicer.util.mainWindow(), 'S-rep information', 'The input is legacy s-rep. Please set a positive distance for it.')
                return True
            newSrepFile = self.transformLegacySrep(filename, dist)
            self.visualizeNewSrep(newSrepFile)
        elif filename.endswith('.xml'):
            logging.info('The input is new s-rep')
            self.visualizeNewSrep(filename)
        else:
            logging.error('Need legacy s-rep(*.m3d) or new s-rep files.')
            return False
            
        logging.info('Processing completed')
        return True
    def transformLegacySrep(self, filename, dist):
        logging.info('The input is legacy s-rep, now converting to new s-rep')
        outputPrefix = os.getcwd() + '/tmp/'
        transformer().transformLegacySrep(filename, outputPrefix, dist)
        return outputPrefix + 'header.xml'


class visualizerTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """ Do whatever is needed to reset the state - typically a scene clear will be enough.
        """
        slicer.mrmlScene.Clear(0)

    def runTest(self):
        """Run as few or as many tests as needed here.
        """
        self.setUp()
        self.test_visualizer1()

    def test_visualizer1(self):
        """ Ideally you should have several levels of tests.  At the lowest level
        tests should exercise the functionality of the logic with different inputs
        (both valid and invalid).  At higher levels your tests should emulate the
        way the user would interact with your code and confirm that it still works
        the way you intended.
        One of the most important features of the tests is that it should alert other
        developers when their changes will have an impact on the behavior of your
        module.  For example, if a developer removes a feature that you depend on,
        your test should break so they know that the feature is needed.
        """

        self.delayDisplay("Starting the test")
        #
        # first, get some data
        #
        volumeNode = slicer.util.getNode(pattern="FA")
        logic = visualizerLogic()
        self.assertIsNotNone(logic.hasImageData(volumeNode))
        self.delayDisplay('Test passed!')
