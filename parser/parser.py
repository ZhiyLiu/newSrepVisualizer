import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
from Lib import *
import numpy as np


#
# parser
#

class parser(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "parser"  # TODO make this more human readable by adding spaces
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
# parserWidget
#

class parserWidget(ScriptedLoadableModuleWidget):
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
        self.inputSelector = slicer.qMRMLNodeComboBox()
        self.inputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.inputSelector.selectNodeUponCreation = True
        self.inputSelector.addEnabled = False
        self.inputSelector.removeEnabled = False
        self.inputSelector.noneEnabled = False
        self.inputSelector.showHidden = False
        self.inputSelector.showChildNodeTypes = False
        self.inputSelector.setMRMLScene(slicer.mrmlScene)
        self.inputSelector.setToolTip("Pick the input to the algorithm.")
        parametersFormLayout.addRow("Input Volume: ", self.inputSelector)

        #
        # Apply Button
        #
        self.applyButton = qt.QPushButton("Select M3D File")
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
        logic = parserLogic()
        flag = self.boundarySurfaceRendering.checked
        logic.run(flag)


#
# parserLogic
#

class parserLogic(ScriptedLoadableModuleLogic):
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


    def run(self,renderFlag):

        """
        Run the actual algorithm
        """
        filename = qt.QFileDialog.getOpenFileName()
        s = srep.srep()
        s.readSrepFromM3D(filename)
        logging.info('Processing started')


        scene = slicer.mrmlScene

        # medial surface
        medial_points = vtk.vtkPoints()
        medial_polyData = vtk.vtkPolyData()
        medial_polyData.SetPoints(medial_points)
        medial_poly = vtk.vtkCellArray()
        medial_polyData.SetPolys(medial_poly)

        # up spoke
        upSpoke_points = vtk.vtkPoints()
        upSpoke_lines = vtk.vtkCellArray()

        # down spoke
        downSpoke_points = vtk.vtkPoints()
        downSpoke_lines = vtk.vtkCellArray()

        # crest spoke
        crestSpoke_points = vtk.vtkPoints()
        crestSpoke_lines = vtk.vtkCellArray()

        # surface points
        boundary_surface_points = vtk.vtkPoints()
        boundary_surface_poly = vtk.vtkCellArray()

        nCols = s.fig.numCols
        nRows = s.fig.numRows

        fidDisplayNode = slicer.vtkMRMLMarkupsDisplayNode()
        scene.AddNode(fidDisplayNode)
        fidNode = slicer.vtkMRMLMarkupsFiducialNode()
        fidDisplayNode.SetGlyphScale(0.01)
        fidDisplayNode.SetSelectedColor(1.0, 1.0, 0.0)
        fidDisplayNode.SetTextScale(0.0)
        scene.AddNode(fidNode)
        fidNode.SetAndObserveDisplayNodeID(fidDisplayNode.GetID())
        # \TODO come up with better name later

        boundary_point_ids = []

        for r in range(nRows):
            for c in range(nCols):
                current_boundary_point_id = []
                current_atom = s.fig.atoms[r, c]
                current_point = current_atom.hub.P
                current_id = medial_points.InsertNextPoint(current_point)
                fidNode.AddFiducial(current_point[0], current_point[1], current_point[2])

                if r < nRows - 1 and c < nCols - 1:
                    quad = vtk.vtkQuad()
                    quad.GetPointIds().SetId(0, current_id)
                    quad.GetPointIds().SetId(1, current_id + nCols)
                    quad.GetPointIds().SetId(2, current_id + nCols + 1)
                    quad.GetPointIds().SetId(3, current_id + 1)
                    medial_poly.InsertNextCell(quad)

                # \TODO: refactor repeated code as a function
                current_upSpoke = current_atom.topSpoke
                current_upPoint = current_point + current_upSpoke.r * current_upSpoke.U
                bp_id = boundary_surface_points.InsertNextPoint(current_upPoint)
                current_boundary_point_id.append(bp_id)

                id0 = upSpoke_points.InsertNextPoint(current_point)
                id1 = upSpoke_points.InsertNextPoint(current_upPoint)
                current_up_line = vtk.vtkLine()
                current_up_line.GetPointIds().SetId(0, id0)
                current_up_line.GetPointIds().SetId(1, id1)
                upSpoke_lines.InsertNextCell(current_up_line)

                current_downSpoke = current_atom.botSpoke
                current_downPoint = current_point + current_downSpoke.r * current_downSpoke.U
                bp_id = boundary_surface_points.InsertNextPoint(current_downPoint)
                current_boundary_point_id.append(bp_id)

                id0 = downSpoke_points.InsertNextPoint(current_point)
                id1 = downSpoke_points.InsertNextPoint(current_downPoint)
                current_down_line = vtk.vtkLine()
                current_down_line.GetPointIds().SetId(0, id0)
                current_down_line.GetPointIds().SetId(1, id1)
                downSpoke_lines.InsertNextCell(current_down_line)

                if current_atom.isCrest():
                    current_crestSpoke = current_atom.crestSpoke
                    current_crestPoint = current_point + current_crestSpoke.r * current_crestSpoke.U
                    bp_id = boundary_surface_points.InsertNextPoint(current_crestPoint)
                    current_boundary_point_id.append(bp_id)

                    id0 = crestSpoke_points.InsertNextPoint(current_point)
                    id1 = crestSpoke_points.InsertNextPoint(current_crestPoint)
                    current_crest_line = vtk.vtkLine()
                    current_crest_line.GetPointIds().SetId(0, id0)
                    current_crest_line.GetPointIds().SetId(1, id1)
                    crestSpoke_lines.InsertNextCell(current_crest_line)

                boundary_point_ids.append(current_boundary_point_id)

        for i in range(nRows):
            for j in range(nCols):
                if (i == 0) or (i == nRows-1) or (j == 0) or (j == nCols-1):
                    atomType = 1
                else:
                    atomType = 0
                atomIndex = nCols * i + j
                if atomType == 1:
                    if (i == 0 and j < nCols - 1) or (i == nRows-1 and j < nCols -1):
                        # horizontal
                        crest_quad_up = vtk.vtkQuad()
                        crest_quad_up.GetPointIds().SetId(0, boundary_point_ids[atomIndex][2])
                        crest_quad_up.GetPointIds().SetId(1, boundary_point_ids[atomIndex + 1][2])
                        crest_quad_up.GetPointIds().SetId(2, boundary_point_ids[atomIndex + 1][0])
                        crest_quad_up.GetPointIds().SetId(3, boundary_point_ids[atomIndex][0])
                        boundary_surface_poly.InsertNextCell(crest_quad_up)

                        crest_quad_down = vtk.vtkQuad()
                        crest_quad_down.GetPointIds().SetId(0, boundary_point_ids[atomIndex][2])
                        crest_quad_down.GetPointIds().SetId(1, boundary_point_ids[atomIndex + 1][2])
                        crest_quad_down.GetPointIds().SetId(2, boundary_point_ids[atomIndex + 1][1])
                        crest_quad_down.GetPointIds().SetId(3, boundary_point_ids[atomIndex][1])
                        boundary_surface_poly.InsertNextCell(crest_quad_down)

                    if (j == 0 and i < nRows - 1) or (j == nCols-1 and i < nRows - 1):
                        # vertical
                        crest_quad_up = vtk.vtkQuad()
                        crest_quad_up.GetPointIds().SetId(0, boundary_point_ids[atomIndex][2])
                        crest_quad_up.GetPointIds().SetId(1, boundary_point_ids[atomIndex + nCols][2])
                        crest_quad_up.GetPointIds().SetId(2, boundary_point_ids[atomIndex + nCols][0])
                        crest_quad_up.GetPointIds().SetId(3, boundary_point_ids[atomIndex][0])
                        boundary_surface_poly.InsertNextCell(crest_quad_up)

                        crest_quad_down = vtk.vtkQuad()
                        crest_quad_down.GetPointIds().SetId(0, boundary_point_ids[atomIndex][2])
                        crest_quad_down.GetPointIds().SetId(1, boundary_point_ids[atomIndex + nCols][2])
                        crest_quad_down.GetPointIds().SetId(2, boundary_point_ids[atomIndex + nCols][1])
                        crest_quad_down.GetPointIds().SetId(3, boundary_point_ids[atomIndex][1])
                        boundary_surface_poly.InsertNextCell(crest_quad_down)

                if i < nRows - 1 and j < nCols - 1:
                    # up quad first
                    up_quad = vtk.vtkQuad()
                    up_quad.GetPointIds().SetId(0, boundary_point_ids[atomIndex][0])
                    up_quad.GetPointIds().SetId(1, boundary_point_ids[atomIndex + nCols][0])
                    up_quad.GetPointIds().SetId(2, boundary_point_ids[atomIndex + nCols + 1][0])
                    up_quad.GetPointIds().SetId(3, boundary_point_ids[atomIndex + 1][0])
                    boundary_surface_poly.InsertNextCell(up_quad)

                    down_quad = vtk.vtkQuad()
                    down_quad.GetPointIds().SetId(0, boundary_point_ids[atomIndex][1])
                    down_quad.GetPointIds().SetId(1, boundary_point_ids[atomIndex + nCols][1])
                    down_quad.GetPointIds().SetId(2, boundary_point_ids[atomIndex + nCols + 1][1])
                    down_quad.GetPointIds().SetId(3, boundary_point_ids[atomIndex + 1][1])
                    boundary_surface_poly.InsertNextCell(down_quad)



        # model node for medial mesh
        medial_model = slicer.vtkMRMLModelNode()
        medial_model.SetScene(scene)
        medial_model.SetName("Medial Mesh")
        medial_model.SetAndObservePolyData(medial_polyData)
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

        # model node for boundary mesh
        boundary_surface_polyData = vtk.vtkPolyData()
        boundary_surface_polyData.SetPoints(boundary_surface_points)
        boundary_surface_polyData.SetPolys(boundary_surface_poly)
        boundary_surface_model = slicer.vtkMRMLModelNode()
        boundary_surface_model.SetScene(scene)
        boundary_surface_model.SetName("Boundary Model")
        boundary_surface_model.SetAndObservePolyData(boundary_surface_polyData)
        # boundary display
        boundary_surface_model_display = slicer.vtkMRMLModelDisplayNode()
        boundary_surface_model_display.SetColor(0,0,0.5)
        boundary_surface_model_display.SetBackfaceCulling(0)
        boundary_surface_model_display.SetScene(scene)
        scene.AddNode(boundary_surface_model_display)
        boundary_surface_model.SetAndObserveDisplayNodeID(boundary_surface_model_display.GetID())
        scene.AddNode(boundary_surface_model)

        # model node for up spoke
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

        # down spoke
        downSpoke_polyData = vtk.vtkPolyData()
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
        crestSpoke_polyData = vtk.vtkPolyData()
        crestSpoke_polyData.SetPoints(crestSpoke_points)
        crestSpoke_polyData.SetLines(crestSpoke_lines)

        crestSpoke_model = slicer.vtkMRMLModelNode()
        crestSpoke_model.SetScene(scene)
        crestSpoke_model.SetName("Crest Spoke")
        crestSpoke_model.SetAndObservePolyData(crestSpoke_polyData)
        # model display node for the down spoke
        crestSpoke_model_display = slicer.vtkMRMLModelDisplayNode()
        crestSpoke_model_display.SetColor(1, 0, 0)
        crestSpoke_model_display.SetScene(scene)
        crestSpoke_model_display.SetLineWidth(3.0)
        crestSpoke_model_display.SetBackfaceCulling(0)
        scene.AddNode(crestSpoke_model_display)
        crestSpoke_model.SetAndObserveDisplayNodeID(crestSpoke_model_display.GetID())
        scene.AddNode(crestSpoke_model)
        #

        logging.info('Processing completed')
        return True


class parserTest(ScriptedLoadableModuleTest):
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
        self.test_parser1()

    def test_parser1(self):
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
        logic = parserLogic()
        self.assertIsNotNone(logic.hasImageData(volumeNode))
        self.delayDisplay('Test passed!')
