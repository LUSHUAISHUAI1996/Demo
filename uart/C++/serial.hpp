#ifndef __SERIAL_HPP__
#define __SERIAL_HPP__

#include <stdio.h>      /*标准输入输出定义*/
#include <stdlib.h>     /*标准函数库定义*/

#include <unistd.h>     /*Unix 标准函数定义*/
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>      /*文件控制定义*/
#include <termios.h>    /*PPSIX 终端控制定义*/
#include <errno.h>      /*错误号定义*/
#include <stdint.h>
using namespace std;
class serial
{

public:
  serial();
  bool SerOpen(const char * dev);
  int SerInit(int speed,int flow_ctrl,int databits,int stopbits,int parity);
  int SerRead(uint8_t * buffer,int size);
  int SerWrite(uint8_t * buffer,int size);
  void SerClose();

private:
  int fd;//串口文件描述符
  struct termios Opt;
  int speed_arr[12] = {B300,B600,B1200,B2400,B4800,B9600,B19200,B38400,B57600,B921600,B115200,B230400};
  int name_arr[12] = {300,600,1200,2400,4800,9600,19200,38400,57600,921600,115200,230400};
};

#endif
