#
# @authors Andrei Novikov (pyclustering@yandex.ru)
# @date 2014-2020
# @copyright GNU Public License
#
# GNU_PUBLIC_LICENSE
#   pyclustering is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyclustering is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


# Tools
CC = g++ -c
LD = g++
RM = rm -rf
MKDIR = mkdir -p


# C++ standard depending on operating system
UNAME = $(shell uname -s | tr '[:upper:]' '[:lower:]')
ifeq ($(findstring cygwin, $(UNAME)), cygwin)
	CPLUS_STANDARD = gnu++14
	PIC_FLAG = 
else
	CPLUS_STANDARD = c++14
	PIC_FLAG = -fPIC
endif


# Warnings.
WARNING_FLAGS = -Wall -Wpedantic


# Toolchain arguments
ifeq ($(CONFIG), valgrind)
	CFLAGS = -MMD -MP -std=$(CPLUS_STANDARD) $(PIC_FLAG) -g
	LFLAGS = -pthread
else ifeq ($(CONFIG), debug)
	CFLAGS = -Og -MMD -MP -std=$(CPLUS_STANDARD) $(PIC_FLAG) -g3 -ggdb3
	LFLAGS = -pthread
else
	CFLAGS = -O2 -MMD -MP -std=$(CPLUS_STANDARD) $(PIC_FLAG) -fprofile-arcs -ftest-coverage $(WARNING_FLAGS)
	LFLAGS = -pthread -fprofile-arcs -ftest-coverage
endif


# Build specific flags (VALGRIND_ANALYSIS_SHOCK - for valgrind shock checking)
ifeq ($(BUILD_VERSION), valgrind_shock)
	CFLAGS += -DVALGRIND_ANALYSIS_SHOCK
endif


# Output name of executable file
EXECUTABLE_DIRECTORY = tst
EXECUTABLE = $(EXECUTABLE_DIRECTORY)/utcore.exe


# Environment
PROJECT_DIRECTORY = .
INCLUDE_DIRECTORY = $(PROJECT_DIRECTORY)/include/
SOURCES_DIRECTORY = src
UTEST_DIRECTORY = tst
EXTERNAL_INCLUDE_DIRECTORY = external/include


# Project sources
SOURCES_MODULES = . cluster container differential interface nnet parallel utils
UTEST_MODULES = .
GTEST_MODULES = gtest

SOURCES_DIRECTORIES = $(addprefix $(SOURCES_DIRECTORY)/, $(SOURCES_MODULES))
SOURCES_DIRECTORIES += $(addprefix $(UTEST_DIRECTORY)/, $(UTEST_MODULES))
SOURCES_DIRECTORIES += $(addprefix $(EXTERNAL_INCLUDE_DIRECTORY)/, $(GTEST_MODULES))

SOURCES = $(foreach SUBDIR, $(SOURCES_DIRECTORIES), $(wildcard $(SUBDIR)/*.cpp))

INCLUDES = -I$(INCLUDE_DIRECTORY) -I$(UTEST_DIRECTORY) -I$(EXTERNAL_INCLUDE_DIRECTORY)


# Project objects
OBJECTS_DIRECTORY = obj/ut

OBJECTS_DIRECTORIES = $(addprefix $(OBJECTS_DIRECTORY)/$(SOURCES_DIRECTORY)/, $(SOURCES_MODULES))
OBJECTS_DIRECTORIES += $(addprefix $(OBJECTS_DIRECTORY)/$(UTEST_DIRECTORY)/, $(UTEST_MODULES))
OBJECTS_DIRECTORIES += $(addprefix $(OBJECTS_DIRECTORY)/$(EXTERNAL_INCLUDE_DIRECTORY)/, $(GTEST_MODULES))

OBJECTS = $(patsubst %.cpp, $(OBJECTS_DIRECTORY)/%.o, $(SOURCES)) 


# The dependency file names
DEPENDENCIES = $(OBJECTS:.o=.d)


# Targets
.PHONY: ut
ut: mkdirs $(EXECUTABLE)


.PHONY: mkdirs
mkdirs: $(OBJECTS_DIRECTORIES)


.PHONY: clean
clean:
	$(RM) $(EXECUTABLE) $(OBJECTS_DIRECTORY)


# Build targets
$(EXECUTABLE): $(OBJECTS)
	$(LD) $(LFLAGS) $^ -o $@


$(OBJECTS_DIRECTORIES):
	$(MKDIR) $@


vpath %.cpp $(SOURCES_DIRECTORIES)


define make-objects
$1/%.o: %.cpp
	$(CC) $(CFLAGS) $(INCLUDES) $$< -o $$@
endef


$(foreach OBJDIR, $(OBJECTS_DIRECTORIES), $(eval $(call make-objects, $(OBJDIR))))


# Include dependencies
-include $(DEPENDENCIES)

