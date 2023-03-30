# Makefile by Matheus Souza (github.com/mfbsouza)

# project name
PROJECT  := app

# paths
BUILDDIR := ./target
DBGDIR   := $(BUILDDIR)/debug
RELDIR   := $(BUILDDIR)/release
INCDIR   := ./include

# compiler and binutils
PREFIX :=
CC     := $(PREFIX)gcc
AS     := $(PREFIX)nasm
CXX    := $(PREFIX)g++
OD     := $(PREFIX)objdump

# flags
CFLAGS   := -Wall -I $(INCDIR) -MMD -MP
CXXFLAGS := -Wall -I $(INCDIR) -MMD -MP
ASMFLAGS := -f elf
LDFLAGS  :=

ifeq ($(DEBUG),1)
	BINDIR    := $(DBGDIR)
	OBJDIR    := $(DBGDIR)/obj
	CFLAGS    += -g -O0 -DDEBUG
	CXXFLAGS  += -g -O0 -DDEBUG
else
	BINDIR    := $(RELDIR)
	OBJDIR    := $(RELDIR)/obj
	CFLAGS    += -g -O3 -DNDEBUG
	CXXFLAGS  += -g -O3 -DNDEBUG
endif

# sources to compile
ALLCSRCS   += $(shell find ./src -type f -name *.c)
ALLCXXSRCS += $(shell find ./src -type f -name *.cpp)
ALLASMSRCS += $(shell find ./src -type f -name *.asm)

# set the linker to g++ if there is any c++ source code
ifeq ($(ALLCXXSRCS),)
        LD := $(PREFIX)gcc
else
        LD := $(PREFIX)g++
endif

# objects settings
COBJS   := $(addprefix $(OBJDIR)/, $(notdir $(ALLCSRCS:.c=.o)))
CXXOBJS := $(addprefix $(OBJDIR)/, $(notdir $(ALLCXXSRCS:.cpp=.o)))
ASMOBJS := $(addprefix $(OBJDIR)/, $(notdir $(ALLASMSRCS:.asm=.o)))
OBJS    := $(COBJS) $(CXXOBJS) $(ASMOBJS)
DEPS    := $(OBJS:.o=.d)

# paths where to search for sources
SRCPATHS := $(sort $(dir $(ALLCSRCS)) $(dir $(ALLCXXSRCS)) $(dir $(ALLASMSRCS)))
VPATH     = $(SRCPATHS)

# output
OUTFILES := $(BINDIR)/$(PROJECT) $(BUILDDIR)/$(PROJECT).lst

# targets
.PHONY: all clean

all: $(OBJDIR) $(BINDIR) $(OBJS) $(OUTFILES)

# targets for the dirs
$(OBJDIR):
	@mkdir -p $(OBJDIR)

$(BINDIR):
	@mkdir -p $(BINDIR)

# target for c objects
$(COBJS) : $(OBJDIR)/%.o : %.c
ifeq ($(VERBOSE),1)
	$(CC) -c $(CFLAGS) $< -o $@
else
	@echo -n "[CC] \t$<\n"
	@$(CC) -c $(CFLAGS) $< -o $@
endif

# target for cpp objects
$(CXXOBJS) : $(OBJDIR)/%.o : %.cpp
ifeq ($(VERBOSE),1)
	$(CXX) -c $(CXXFLAGS) $< -o $@
else
	@echo -n "[CXX]\t$<\n"
	@$(CXX) -c $(CXXFLAGS) $< -o $@
endif

# target for asm objects
$(ASMOBJS) : $(OBJDIR)/%.o : %.asm
ifeq ($(VERBOSE),1)
	$(AS) $(ASMFLAGS) $< -o $@
else
	@echo -n "[AS] \t$<\n"
	@$(AS) $(ASMFLAGS) $< -o $@
endif

# target for ELF file
$(BINDIR)/$(PROJECT): $(OBJS)
ifeq ($(VERBOSE),1)
	$(LD) $(LDFLAGS) $(OBJS) -o $@
else
	@echo -n "[LD] \t./$@\n"
	@$(LD) $(LDFLAGS) $(OBJS) -o $@
endif

# target for disassembly and sections header info
$(BUILDDIR)/$(PROJECT).lst: $(BINDIR)/$(PROJECT)
ifeq ($(VERBOSE),1)
	$(OD) -h -S $< > $@
else
	@echo -n "[OD] \t./$@\n"
	@$(OD) -h -S $< > $@
endif

# target for cleaning files
clean:
	rm -rf $(BUILDDIR)

# include the dependency files, should be the last of the makefile
-include $(DEPS)
