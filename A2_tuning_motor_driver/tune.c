#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "fbida.h"

int main(void)
{
  int nRet, dnum, cnum;
  DASMPLCHREQ DaSmplChReq[1];
  unsigned short Data[1];
  system("clear");

  dnum = 1;
  //printf("Enter the device number.: ");
  //scanf("%d", &dnum);
  // Open a device.
  nRet = DaOpen(dnum);
  if(nRet != DA_ERROR_SUCCESS){
	printf("Open error: ret=%Xh\n", nRet);
	exit(EXIT_FAILURE);
  }

  DaSmplChReq[0].ulChNo = 1;
  DaSmplChReq[0].ulRange = DA_10V;

  while(1){

	printf("\n\n## Menu ##\n\n");
	printf("[0]  ... DA   0.0 Voltage\n");
	printf("[1]  ... DA  +2.0 Voltage\n");
	printf("[2]  ... DA  +4.0 Voltage\n");
	printf("[3]  ... DA  +6.0 Voltage\n");
	printf("[4]  ... DA  +8.0 Voltage\n");
	printf("[5]  ... DA +10.0 Voltage\n");
	printf("[11] ... DA  -2.0 Voltage\n");
	printf("[22] ... DA  -4.0 Voltage\n");
	printf("[33] ... DA  -6.0 Voltage\n");
	printf("[44] ... DA  -8.0 Voltage\n");
	printf("[55] ... DA -10.0 Voltage\n");
	printf("[-1] ... exit\n\n");
	printf("Press number.: ");
	scanf("%d", &cnum);

	if(0==cnum || -1==cnum ) Data[0] = 0x0800; // Output data of CH1 (2048 for 0 Voltage)

	if(1==cnum) Data[0] = 0x099A; // (2458 = 2048 + 410  for +2  Voltage)
	if(2==cnum) Data[0] = 0x0B33; // (2867 = 2048 + 819  for +4  Voltage)
	if(3==cnum) Data[0] = 0x0CCD; // (3277 = 2048 + 1229 for +6  Voltage)
	if(4==cnum) Data[0] = 0x0E66; // (3686 = 2048 + 1638 for +8  Voltage)
	if(5==cnum) Data[0] = 0x0FFF; // (4096 = 2048 + 2048 for +10 Voltage)

	if(11==cnum) Data[0] = 0x0666; // (1638 = 2048 - 410  for -2  Voltage)
	if(22==cnum) Data[0] = 0x04CD; // (1229 = 2048 - 819  for -4  Voltage)
	if(33==cnum) Data[0] = 0x0333; // ( 819 = 2048 - 1229 for -6  Voltage)
	if(44==cnum) Data[0] = 0x019A; // ( 410 = 2048 - 1638 for -8  Voltage)
	if(55==cnum) Data[0] = 0x0000; // (   0 = 2048 - 2048 for -10 Voltage)

	nRet = DaOutputDA( dnum, 1, &DaSmplChReq[0], &Data[0] );

	if(-1==cnum) break;
	if(nRet != DA_ERROR_SUCCESS){
		printf("DaOutputDA Error\n");
		DaClose(dnum);
		return -1;
	}
        sleep(3);
  }
  nRet = DaClose(dnum);
  printf("finish\n");
  return 0;
}

