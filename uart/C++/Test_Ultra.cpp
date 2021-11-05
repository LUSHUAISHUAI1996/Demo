#include "serial.hpp"
#include <iostream>
#include <iomanip>

bool CheckData(uint8_t recvbuff[])
{
        if((recvbuff[0]==0xff &&recvbuff[1]==0xfe && recvbuff[2] == 0x75)&&(recvbuff[13]==(recvbuff[3]^recvbuff[4]^recvbuff[5]^recvbuff[6]^recvbuff[7]^recvbuff[8]^recvbuff[9]^recvbuff[10]^recvbuff[11]^recvbuff[12])))
        {
                return true;
        }
        return false;
}

void EncodeDistance(uint8_t recvbuff[],float distance[])
{
        uint16_t temp = 0;
        for(int i =0; i <5; i++)
        {
                temp = recvbuff[2*i+3];
                distance[i] = (temp<<8|recvbuff[2*i+4])/1000.;
        }
}

int main() 
{
	
        uint8_t sendbuff[3]={0xff,0xfe,0x75};
        uint8_t recvbuff[14];
        float distance[5];
        string direction[5] ={"L","FL","FC","FR","R"};
        const char *dev  = "/dev/ttyUSB0";
        serial myserial;
        cout<<"serial Test"<<endl;
        myserial.SerOpen(dev);
        myserial.SerInit(230400,0,8,1,'N');

        while (true)
        {
                myserial.SerWrite(sendbuff, 3);
                myserial.SerRead(recvbuff, 14);
                if(CheckData(recvbuff))
                {
                        EncodeDistance(recvbuff,distance);
                        cout<<"Recv Data:"<<endl;
                        for(int i = 0; i<14; i++)
                        {
                                std::cout << std::hex << static_cast<int>(recvbuff[i])<<" ";
                        }
                        cout<<endl;
                        for(int i = 0; i<5; i++)
                        {
                          cout<<direction[i]<<" :";
                          cout << setprecision(4) << distance[i]<<" ";
                        }
                        cout<<endl;
                }
                usleep(200);
        }
}
