#modified from
#https://github.com/TheNetAdmin/Makefile-Templates/blob/master/SmallProject/Template/Makefile

APP_NAME := main #CHANGE

# path macros
BIN_PATH := bin
OBJ_PATH := obj
DBG_PATH := debug
TEST_PATH := test

SRC_PATH := src
INCL_PATH := include
VENDOR_PATH := ../vendor
TEST_VENDOR := minunit

# tool macros
CC := cc# FILL: the compiler
CCFLAGS := -Wall -I$(VENDOR_PATH)/$(TEST_VENDOR)/ -I$(INCL_PATH)/ -std=c99 #-DTEST# FILL: compile flags
DBGFLAGS := -g
TESTFLAGS := -I$(VENDOR_PATH)/$(TEST_VENDOR)/
CCOBJFLAGS := $(CCFLAGS) -c

# compile macros
TARGET_NAME := $(APP_NAME) # FILL: target name
ifeq ($(OS),Windows_NT)
	TARGET_NAME := $(addsuffix .exe,$(TARGET_NAME))
endif

# make sure these dont resolve to the same name!!

TARGET := $(BIN_PATH)/$(TARGET_NAME)
TARGET_DEBUG := $(BIN_PATH)/debug_$(TARGET_NAME) #DBG_PATH
TARGET_TEST := $(BIN_PATH)/test_$(TARGET_NAME)

# src files & obj files
SRC := $(foreach x, $(SRC_PATH), $(wildcard $(addprefix $(x)/*,.c*)))
TEST := $(foreach x, $(TEST_PATH), $(wildcard $(addprefix $(x)/*,.c*)))

OBJ := $(addprefix $(OBJ_PATH)/, $(addsuffix .o, $(notdir $(basename $(SRC)))))
OBJ_DEBUG := $(addprefix $(DBG_PATH)/, $(addsuffix .o, $(notdir $(basename $(SRC)))))
OBJ_TEST  := $(addprefix $(TEST_PATH)/, $(addsuffix .o, $(notdir $(basename $(TEST)))))
OBJ_TEST_SRC := $(addprefix $(TEST_PATH)/, $(addsuffix .o, $(notdir $(basename $(SRC)))))

# clean files list
DISTCLEAN_LIST := $(OBJ) \
                  $(OBJ_DEBUG) \
				  $(OBJ_TEST) \
				  $(OBJ_TEST_SRC)

CLEAN_LIST := $(TARGET) \
			  $(TARGET_DEBUG) \
			  $(TARGET_TEST) \
			  $(DISTCLEAN_LIST)

# default rule
default: makedir all debug test

# non-phony targets

$(TARGET): $(OBJ) $(INCL_PATH)/*.h
	$(CC) $(CCFLAGS) -o $@ $(OBJ)

$(OBJ_PATH)/%.o: $(SRC_PATH)/%.c* $(INCL_PATH)/*.h
	$(CC) $(CCOBJFLAGS) -o $@ $<

$(DBG_PATH)/%.o: $(SRC_PATH)/%.c* $(INCL_PATH)/*.h
	$(CC) $(CCOBJFLAGS) $(DBGFLAGS) -o $@ $<

$(TARGET_DEBUG): $(OBJ_DEBUG) $(INCL_PATH)/*.h
	$(CC) $(CCFLAGS) $(DBGFLAGS) $(OBJ_DEBUG) -o $@

$(TARGET_TEST): $(OBJ_TEST_SRC) $(OBJ_TEST) $(INCL_PATH)/*.h $(VENDOR_PATH)/$(TEST_VENDOR)/*.h
	$(CC) $(CCFLAGS) -o $@ $(OBJ_TEST_SRC) $(OBJ_TEST) 

$(TEST_PATH)/%.o: $(SRC_PATH)/%.c* $(INCL_PATH)/*.h 
	$(CC) -DTEST $(CCOBJFLAGS) -o $@ $<

$(TEST_PATH)/%.o: $(SRC_PATH)/%.c* $(TEST_PATH)/%.c* $(INCL_PATH)/*.h $(VENDOR_PATH)/$(TEST_VENDOR)/*.h
	$(CC) -DTEST $(CCOBJFLAGS) -o $@ $<

# phony rules
.PHONY: makedir
makedir:
	@mkdir -p $(BIN_PATH) $(OBJ_PATH) $(DBG_PATH)

.PHONY: all
all: $(TARGET)

.PHONY: debug
debug: $(TARGET_DEBUG)

.PHONY: test
test: $(TARGET_TEST)

.PHONY: clean
clean:
	@echo CLEAN $(CLEAN_LIST)
	@rm -f $(CLEAN_LIST)

.PHONY: distclean
distclean:
	@echo CLEAN $(DISTCLEAN_LIST)
	@rm -f $(DISTCLEAN_LIST)