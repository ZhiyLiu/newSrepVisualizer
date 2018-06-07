# This file will be configured to contain variables for CPack. These variables
# should be set in the CMake list file of the project before CPack module is
# included. The list of available CPACK_xxx variables and their associated
# documentation may be obtained using
#  cpack --help-variable-list
#
# Some variables are common to all generators (e.g. CPACK_PACKAGE_NAME)
# and some are specific to a generator
# (e.g. CPACK_NSIS_EXTRA_INSTALL_COMMANDS). The generator specific variables
# usually begin with CPACK_<GENNAME>_xxxx.


SET(CPACK_BINARY_7Z "")
SET(CPACK_BINARY_BUNDLE "")
SET(CPACK_BINARY_CYGWIN "")
SET(CPACK_BINARY_DEB "")
SET(CPACK_BINARY_DRAGNDROP "")
SET(CPACK_BINARY_IFW "")
SET(CPACK_BINARY_NSIS "")
SET(CPACK_BINARY_OSXX11 "")
SET(CPACK_BINARY_PACKAGEMAKER "")
SET(CPACK_BINARY_PRODUCTBUILD "")
SET(CPACK_BINARY_RPM "")
SET(CPACK_BINARY_STGZ "")
SET(CPACK_BINARY_TBZ2 "")
SET(CPACK_BINARY_TGZ "")
SET(CPACK_BINARY_TXZ "")
SET(CPACK_BINARY_TZ "")
SET(CPACK_BINARY_WIX "")
SET(CPACK_BINARY_ZIP "")
SET(CPACK_BUILD_SOURCE_DIRS "/playpen/workspace/ra_job/newSrepVisualizer;/playpen/workspace/ra_job/newSrepVisualizer/build")
SET(CPACK_CMAKE_GENERATOR "Unix Makefiles")
SET(CPACK_COMPONENT_UNSPECIFIED_HIDDEN "TRUE")
SET(CPACK_COMPONENT_UNSPECIFIED_REQUIRED "TRUE")
SET(CPACK_GENERATOR "TGZ")
SET(CPACK_INSTALL_CMAKE_PROJECTS "/playpen/workspace/ra_job/newSrepVisualizer/build;newSrepVisualizer;ALL;/")
SET(CPACK_INSTALL_PREFIX "/usr/local")
SET(CPACK_MODULE_PATH "/playpen/software/Slicer-SuperBuild-Debug/SlicerExecutionModel-build/CMake;/playpen/software/Slicer-SuperBuild-Debug/SlicerExecutionModel-build/CMake;/playpen/software/Slicer-SuperBuild-Debug/SlicerExecutionModel-build/CMake;/playpen/software/Slicer-SuperBuild-Debug/SlicerExecutionModel-build/CMake;/playpen/software/Slicer-SuperBuild-Debug/SlicerExecutionModel-build/CMake;/playpen/software/Slicer-SuperBuild-Debug/CTKAPPLAUNCHER/CMake;/playpen/software/Slicer-SuperBuild-Debug/VTKv9/CMake;/playpen/software/Slicer-SuperBuild-Debug/ITKv4/CMake;/playpen/software/Slicer-SuperBuild-Debug/CTKAppLauncherLib-build/CMake;/playpen/software/Slicer-SuperBuild-Debug/CTK/Utilities/CMake;/playpen/software/Slicer-SuperBuild-Debug/CTK/CMake;/playpen/software/Slicer-SuperBuild-Debug/ITKv4/Modules/ThirdParty/DCMTK/CMake;/playpen/software/Slicer-SuperBuild-Debug/CTK/Utilities/CMake;/playpen/software/Slicer/CMake;/playpen/software/Slicer/Extensions/CMake;/playpen/software/Slicer-SuperBuild-Debug/VTKv9/CMake")
SET(CPACK_MONOLITHIC_INSTALL "ON")
SET(CPACK_NSIS_DISPLAY_NAME "newSrepVisualizer 0.1.1")
SET(CPACK_NSIS_INSTALLER_ICON_CODE "")
SET(CPACK_NSIS_INSTALLER_MUI_ICON_CODE "")
SET(CPACK_NSIS_INSTALL_ROOT "$PROGRAMFILES")
SET(CPACK_NSIS_MODIFY_PATH "OFF")
SET(CPACK_NSIS_PACKAGE_NAME "newSrepVisualizer 0.1.1")
SET(CPACK_OUTPUT_CONFIG_FILE "/playpen/workspace/ra_job/newSrepVisualizer/build/CPackConfig.cmake")
SET(CPACK_PACKAGE_DEFAULT_LOCATION "/")
SET(CPACK_PACKAGE_DESCRIPTION_FILE "/playpen/software/Slicer/README.txt")
SET(CPACK_PACKAGE_DESCRIPTION_SUMMARY "This is an example of a simple extension")
SET(CPACK_PACKAGE_FILE_NAME "27193-linux-amd64-newSrepVisualizer-git1ae1973-2018-05-26")
SET(CPACK_PACKAGE_INSTALL_DIRECTORY "newSrepVisualizer 0.1.1")
SET(CPACK_PACKAGE_INSTALL_REGISTRY_KEY "newSrepVisualizer 0.1.1")
SET(CPACK_PACKAGE_NAME "newSrepVisualizer")
SET(CPACK_PACKAGE_RELOCATABLE "true")
SET(CPACK_PACKAGE_VENDOR "NA-MIC")
SET(CPACK_PACKAGE_VERSION "0.1.1")
SET(CPACK_PACKAGE_VERSION_MAJOR "0")
SET(CPACK_PACKAGE_VERSION_MINOR "1")
SET(CPACK_PACKAGE_VERSION_PATCH "1")
SET(CPACK_RESOURCE_FILE_LICENSE "/playpen/software/Slicer/License.txt")
SET(CPACK_RESOURCE_FILE_README "/playpen/software/cmake-3.8.2-Linux-x86_64/share/cmake-3.8/Templates/CPack.GenericDescription.txt")
SET(CPACK_RESOURCE_FILE_WELCOME "/playpen/software/cmake-3.8.2-Linux-x86_64/share/cmake-3.8/Templates/CPack.GenericWelcome.txt")
SET(CPACK_SET_DESTDIR "OFF")
SET(CPACK_SOURCE_7Z "")
SET(CPACK_SOURCE_CYGWIN "")
SET(CPACK_SOURCE_GENERATOR "TGZ;TXZ")
SET(CPACK_SOURCE_OUTPUT_CONFIG_FILE "/playpen/workspace/ra_job/newSrepVisualizer/build/CPackSourceConfig.cmake")
SET(CPACK_SOURCE_RPM "OFF")
SET(CPACK_SOURCE_TBZ2 "OFF")
SET(CPACK_SOURCE_TGZ "ON")
SET(CPACK_SOURCE_TXZ "ON")
SET(CPACK_SOURCE_TZ "OFF")
SET(CPACK_SOURCE_ZIP "OFF")
SET(CPACK_SYSTEM_NAME "Linux")
SET(CPACK_TOPLEVEL_TAG "Linux")
SET(CPACK_WIX_SIZEOF_VOID_P "8")

if(NOT CPACK_PROPERTIES_FILE)
  set(CPACK_PROPERTIES_FILE "/playpen/workspace/ra_job/newSrepVisualizer/build/CPackProperties.cmake")
endif()

if(EXISTS ${CPACK_PROPERTIES_FILE})
  include(${CPACK_PROPERTIES_FILE})
endif()
