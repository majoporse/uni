# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

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
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /mnt/c/pb071_cviko/seminar-08

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /mnt/c/pb071_cviko/seminar-08/cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/list.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/list.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/list.dir/flags.make

CMakeFiles/list.dir/list.c.o: CMakeFiles/list.dir/flags.make
CMakeFiles/list.dir/list.c.o: ../list.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/mnt/c/pb071_cviko/seminar-08/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/list.dir/list.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/list.dir/list.c.o   -c /mnt/c/pb071_cviko/seminar-08/list.c

CMakeFiles/list.dir/list.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/list.dir/list.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /mnt/c/pb071_cviko/seminar-08/list.c > CMakeFiles/list.dir/list.c.i

CMakeFiles/list.dir/list.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/list.dir/list.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /mnt/c/pb071_cviko/seminar-08/list.c -o CMakeFiles/list.dir/list.c.s

CMakeFiles/list.dir/list_utils.c.o: CMakeFiles/list.dir/flags.make
CMakeFiles/list.dir/list_utils.c.o: ../list_utils.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/mnt/c/pb071_cviko/seminar-08/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building C object CMakeFiles/list.dir/list_utils.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/list.dir/list_utils.c.o   -c /mnt/c/pb071_cviko/seminar-08/list_utils.c

CMakeFiles/list.dir/list_utils.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/list.dir/list_utils.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /mnt/c/pb071_cviko/seminar-08/list_utils.c > CMakeFiles/list.dir/list_utils.c.i

CMakeFiles/list.dir/list_utils.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/list.dir/list_utils.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /mnt/c/pb071_cviko/seminar-08/list_utils.c -o CMakeFiles/list.dir/list_utils.c.s

# Object files for target list
list_OBJECTS = \
"CMakeFiles/list.dir/list.c.o" \
"CMakeFiles/list.dir/list_utils.c.o"

# External object files for target list
list_EXTERNAL_OBJECTS =

liblist.a: CMakeFiles/list.dir/list.c.o
liblist.a: CMakeFiles/list.dir/list_utils.c.o
liblist.a: CMakeFiles/list.dir/build.make
liblist.a: CMakeFiles/list.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/mnt/c/pb071_cviko/seminar-08/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking C static library liblist.a"
	$(CMAKE_COMMAND) -P CMakeFiles/list.dir/cmake_clean_target.cmake
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/list.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/list.dir/build: liblist.a

.PHONY : CMakeFiles/list.dir/build

CMakeFiles/list.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/list.dir/cmake_clean.cmake
.PHONY : CMakeFiles/list.dir/clean

CMakeFiles/list.dir/depend:
	cd /mnt/c/pb071_cviko/seminar-08/cmake-build-debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /mnt/c/pb071_cviko/seminar-08 /mnt/c/pb071_cviko/seminar-08 /mnt/c/pb071_cviko/seminar-08/cmake-build-debug /mnt/c/pb071_cviko/seminar-08/cmake-build-debug /mnt/c/pb071_cviko/seminar-08/cmake-build-debug/CMakeFiles/list.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/list.dir/depend
