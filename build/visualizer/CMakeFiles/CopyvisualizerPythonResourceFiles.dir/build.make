# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.8

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /playpen/software/cmake-3.8.2-Linux-x86_64/bin/cmake

# The command to remove a file.
RM = /playpen/software/cmake-3.8.2-Linux-x86_64/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /playpen/workspace/ra_job/newSrepVisualizer

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /playpen/workspace/ra_job/newSrepVisualizer/build

# Utility rule file for CopyvisualizerPythonResourceFiles.

# Include the progress variables for this target.
include visualizer/CMakeFiles/CopyvisualizerPythonResourceFiles.dir/progress.make

visualizer/CMakeFiles/CopyvisualizerPythonResourceFiles: lib/Slicer-4.9/qt-scripted-modules/Resources/Icons/visualizer.png
visualizer/CMakeFiles/CopyvisualizerPythonResourceFiles: lib/Slicer-4.9/qt-scripted-modules/Lib/__init__.py
visualizer/CMakeFiles/CopyvisualizerPythonResourceFiles: lib/Slicer-4.9/qt-scripted-modules/Lib/srep.py


lib/Slicer-4.9/qt-scripted-modules/Resources/Icons/visualizer.png: ../visualizer/Resources/Icons/visualizer.png
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/playpen/workspace/ra_job/newSrepVisualizer/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Copying python Resource: Resources/Icons/visualizer.png"
	cd /playpen/workspace/ra_job/newSrepVisualizer/build/visualizer && /playpen/software/cmake-3.8.2-Linux-x86_64/bin/cmake -E copy /playpen/workspace/ra_job/newSrepVisualizer/visualizer/Resources/Icons/visualizer.png /playpen/workspace/ra_job/newSrepVisualizer/build/lib/Slicer-4.9/qt-scripted-modules/Resources/Icons/visualizer.png

lib/Slicer-4.9/qt-scripted-modules/Lib/__init__.py: ../visualizer/Lib/__init__.py
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/playpen/workspace/ra_job/newSrepVisualizer/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Copying python Resource: Lib/__init__.py"
	cd /playpen/workspace/ra_job/newSrepVisualizer/build/visualizer && /playpen/software/cmake-3.8.2-Linux-x86_64/bin/cmake -E copy /playpen/workspace/ra_job/newSrepVisualizer/visualizer/Lib/__init__.py /playpen/workspace/ra_job/newSrepVisualizer/build/lib/Slicer-4.9/qt-scripted-modules/Lib/__init__.py

lib/Slicer-4.9/qt-scripted-modules/Lib/srep.py: ../visualizer/Lib/srep.py
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/playpen/workspace/ra_job/newSrepVisualizer/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Copying python Resource: Lib/srep.py"
	cd /playpen/workspace/ra_job/newSrepVisualizer/build/visualizer && /playpen/software/cmake-3.8.2-Linux-x86_64/bin/cmake -E copy /playpen/workspace/ra_job/newSrepVisualizer/visualizer/Lib/srep.py /playpen/workspace/ra_job/newSrepVisualizer/build/lib/Slicer-4.9/qt-scripted-modules/Lib/srep.py

CopyvisualizerPythonResourceFiles: visualizer/CMakeFiles/CopyvisualizerPythonResourceFiles
CopyvisualizerPythonResourceFiles: lib/Slicer-4.9/qt-scripted-modules/Resources/Icons/visualizer.png
CopyvisualizerPythonResourceFiles: lib/Slicer-4.9/qt-scripted-modules/Lib/__init__.py
CopyvisualizerPythonResourceFiles: lib/Slicer-4.9/qt-scripted-modules/Lib/srep.py
CopyvisualizerPythonResourceFiles: visualizer/CMakeFiles/CopyvisualizerPythonResourceFiles.dir/build.make

.PHONY : CopyvisualizerPythonResourceFiles

# Rule to build all files generated by this target.
visualizer/CMakeFiles/CopyvisualizerPythonResourceFiles.dir/build: CopyvisualizerPythonResourceFiles

.PHONY : visualizer/CMakeFiles/CopyvisualizerPythonResourceFiles.dir/build

visualizer/CMakeFiles/CopyvisualizerPythonResourceFiles.dir/clean:
	cd /playpen/workspace/ra_job/newSrepVisualizer/build/visualizer && $(CMAKE_COMMAND) -P CMakeFiles/CopyvisualizerPythonResourceFiles.dir/cmake_clean.cmake
.PHONY : visualizer/CMakeFiles/CopyvisualizerPythonResourceFiles.dir/clean

visualizer/CMakeFiles/CopyvisualizerPythonResourceFiles.dir/depend:
	cd /playpen/workspace/ra_job/newSrepVisualizer/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /playpen/workspace/ra_job/newSrepVisualizer /playpen/workspace/ra_job/newSrepVisualizer/visualizer /playpen/workspace/ra_job/newSrepVisualizer/build /playpen/workspace/ra_job/newSrepVisualizer/build/visualizer /playpen/workspace/ra_job/newSrepVisualizer/build/visualizer/CMakeFiles/CopyvisualizerPythonResourceFiles.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : visualizer/CMakeFiles/CopyvisualizerPythonResourceFiles.dir/depend
