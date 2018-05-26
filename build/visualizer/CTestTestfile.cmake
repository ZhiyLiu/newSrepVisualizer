# CMake generated Testfile for 
# Source directory: /playpen/workspace/ra_job/newSrepVisualizer/visualizer
# Build directory: /playpen/workspace/ra_job/newSrepVisualizer/build/visualizer
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(py_nomainwindow_qSlicervisualizerModuleGenericTest "/playpen/software/Slicer-SuperBuild-Debug/Slicer-build/Slicer" "--no-splash" "--testing" "--launcher-additional-settings" "/playpen/workspace/ra_job/newSrepVisualizer/build/AdditionalLauncherSettings.ini" "--no-main-window" "--disable-cli-modules" "--additional-module-path" "/playpen/workspace/ra_job/newSrepVisualizer/build/lib/Slicer-4.9/qt-scripted-modules" "--additional-module-paths" "/playpen/workspace/ra_job/newSrepVisualizer/build/lib/Slicer-4.9/qt-scripted-modules" "/playpen/workspace/ra_job/newSrepVisualizer/build/lib/Slicer-4.9/cli-modules" "/playpen/workspace/ra_job/newSrepVisualizer/build/lib/Slicer-4.9/qt-loadable-modules" "--python-code" "import slicer.testing; slicer.testing.runUnitTest(['/playpen/workspace/ra_job/newSrepVisualizer/build/visualizer', '/playpen/workspace/ra_job/newSrepVisualizer/visualizer'], 'qSlicervisualizerModuleGenericTest')")
set_tests_properties(py_nomainwindow_qSlicervisualizerModuleGenericTest PROPERTIES  RUN_SERIAL "TRUE")
add_test(py_visualizer "/playpen/software/Slicer-SuperBuild-Debug/Slicer-build/Slicer" "--no-splash" "--testing" "--launcher-additional-settings" "/playpen/workspace/ra_job/newSrepVisualizer/build/AdditionalLauncherSettings.ini" "--additional-module-paths" "/playpen/workspace/ra_job/newSrepVisualizer/build/lib/Slicer-4.9/qt-scripted-modules" "/playpen/workspace/ra_job/newSrepVisualizer/build/lib/Slicer-4.9/cli-modules" "/playpen/workspace/ra_job/newSrepVisualizer/build/lib/Slicer-4.9/qt-loadable-modules" "--python-code" "import slicer.testing; slicer.testing.runUnitTest(['/playpen/workspace/ra_job/newSrepVisualizer/build/visualizer', '/playpen/workspace/ra_job/newSrepVisualizer/visualizer'], 'visualizer')")
set_tests_properties(py_visualizer PROPERTIES  RUN_SERIAL "TRUE")
subdirs("Testing")
