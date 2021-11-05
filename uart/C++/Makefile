CC = g++

CFLAGS = -Wall -std=c++11

TARGET = Test_Ultra

SRCS := $(wildcard *.cpp)

OBJS := $(patsubst %cpp, %o, $(SRCS))

all: $(TARGET)

$(TARGET):$(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

%.o:%.cpp
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f *.o $(TARGET)
