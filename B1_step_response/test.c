#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/mman.h>
#include <sched.h>
#include <time.h>
#ifndef NSEC_PER_SEC
#define NSEC_PER_SEC 1000000000L
#endif
#include <math.h>

#define DA_FLAG
#define ENC_FLAG


// Conditions 
#define SAMPLING_TIME_US         (       1*1000 ) // micro second, 1000 micro = 1 mili
#define TOTAL_TIME_LENGTH_US     (  8*1000*1000 ) // micro second
#define ZEROINPUT_TIME_LENGTH_US (  2*1000*1000 ) // micro second

#define INPUT_MAGNITUDE  (2.3) // voltage

#define FILE_NAME_DATA      "./step_responce.dat"
#define FILE_NAME_CONDITION "./condition.txt"
#define TOTAL_DATA_LENGTH (TOTAL_TIME_LENGTH_US/SAMPLING_TIME_US)
#define ZERO_DATA_LENGTH (ZEROINPUT_TIME_LENGTH_US/SAMPLING_TIME_US)

#define ENCODER_RESOLUTION (1000)
#define REDUCTION_RATIO (50)
#define ENCODER_MULTIPLICATION (4)
#define OVERALL_RESOLUTION (ENCODER_RESOLUTION*REDUCTION_RATIO*ENCODER_MULTIPLICATION)

#define VELOCITY_LIMITER (120*2.*M_PI/60)

#ifdef DA_FLAG
#include <unistd.h>
#include "fbida.h"
#endif

#ifdef ENC_FLAG
#include <unistd.h>
#include "fbipenc.h"
#endif

// functions for real-time control
// ref https://sites.google.com/site/roboticstools/HOME/RTM/RealTimeRTM/LinuxStandard/source?tmpl=%2Fsystem%2Fapp%2Ftemplates%2Fprint%2F&showPrintDialog=1
static void timespec_add_ns(struct timespec *a, unsigned int ns)
{
    ns += a->tv_nsec;
    while(ns >= NSEC_PER_SEC) {
        ns -= NSEC_PER_SEC;
        a->tv_sec++;
    }
    a->tv_nsec = ns;
}
static int timespec_compare(const struct timespec *lhs, const struct timespec *rhs) {
    if (lhs->tv_sec < rhs->tv_sec)
        return -1;
    if (lhs->tv_sec > rhs->tv_sec)
        return 1;
    return lhs->tv_nsec - rhs->tv_nsec;
}


//---------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------
int main()
{
  FILE *fp;
  double input_data [TOTAL_DATA_LENGTH];
  double output_data[TOTAL_DATA_LENGTH];
  double velocity[TOTAL_DATA_LENGTH];
  int da_i;
  int i;

  // scheduling for real time
  struct sched_param param;
  int policy = SCHED_FIFO;
  struct timespec tsperiod, tsnow;
  unsigned int control_period_ns = SAMPLING_TIME_US*1000; // nano sec

  // DA
  int nRet;
  unsigned short DaData[1];
  double max_voltage=10.;
#ifdef DA_FLAG
  int dnum, cnum;
  DASMPLCHREQ DaSmplChReq[1];
#endif

  //ENC
  unsigned long dwCounter;
#ifdef ENC_FLAG
  int nDevice, nChannel;
  double angle;
#endif


  // ------------------------------------ 1 ------------------------------------------ open
  printf("\n## STEP RESPONSE ##\n\n");  
  printf("SAMPLING_TIME         = %f [s]\n",SAMPLING_TIME_US/1000000.);
  printf("TOTAL_TIME_LENGTH     = %f [s]\n",TOTAL_TIME_LENGTH_US/1000000.);
  printf("ZEROINPUT_TIME_LENGTH = %f [s]\n",ZEROINPUT_TIME_LENGTH_US/1000000.);

  fp=fopen(FILE_NAME_CONDITION, "w");
  if(fp==NULL){
    printf("FILE cannot be opened!\n");
    exit(EXIT_FAILURE);
  }
  fprintf(fp,"STEP RESPONSE\n\n");  
  //common
  fprintf(fp,"SAMPLING_TIME_US = %d\n",SAMPLING_TIME_US);
  fprintf(fp,"TOTAL_TIME_LENGTH_US = %d\n",TOTAL_TIME_LENGTH_US);
  fprintf(fp,"ZEROINPUT_TIME_LENGTH_US = %d\n",ZEROINPUT_TIME_LENGTH_US);
  fprintf(fp,"TOTAL_DATA_LENGTH = %d\n\n",TOTAL_DATA_LENGTH);
  fprintf(fp,"ENCODER_RESOLUTION = %d\n",ENCODER_RESOLUTION);
  fprintf(fp,"REDUCTION_RATIO = %d\n",REDUCTION_RATIO);
  fprintf(fp,"ENCODER_MULTIPLICATION = %d\n",ENCODER_MULTIPLICATION);
  fprintf(fp,"OVERALL_RESOLUTION = %d\n\n",OVERALL_RESOLUTION);
  fprintf(fp,"VELOCITY_LIMITER = %f\n\n",VELOCITY_LIMITER);
  //step
  fprintf(fp,"INPUT_MAGNITUDE = %f\n",INPUT_MAGNITUDE);
  fclose(fp);
  

#ifdef DA_FLAG
  system("clear");
  dnum = 1;
  nRet = DaOpen(dnum);
  if(nRet != DA_ERROR_SUCCESS){
    printf("Da error: ret=%Xh\n", nRet);
    exit(EXIT_FAILURE);
  }

  DaSmplChReq[0].ulChNo = 1;
  DaSmplChReq[0].ulRange = DA_10V; // DA range
  DaData[0] = 2048; // (2048 for 0 Voltage) = 0x0800;
  nRet = DaOutputDA( dnum, 1, &DaSmplChReq[0], &DaData[0] );
  if(nRet != DA_ERROR_SUCCESS){
    printf("Da error: ret=%Xh\n", nRet);
    exit(EXIT_FAILURE);
  }
  if      ( DaSmplChReq[0].ulRange == DA_10V ) max_voltage=10.;
  else if ( DaSmplChReq[0].ulRange == DA_5V  ) max_voltage=5.;
  else{
    printf("Da range error\n");
    exit(EXIT_FAILURE);
  }
#endif

#ifdef ENC_FLAG
  nDevice = 1;
  nRet = PencOpen(nDevice, PENC_FLAG_SHARE);
  if (nRet != PENC_ERROR_SUCCESS) {
    printf("Enc error: ret=%Xh\n", nRet);
    exit(EXIT_FAILURE);
  }

  nChannel = 1;
  nRet = PencSetMode(nDevice, nChannel, 0x06, 0, 1, 0);
  if (nRet != PENC_ERROR_SUCCESS) {
    printf("Enc error: ret=%Xh\n", nRet);
    PencClose(nDevice);
    exit(EXIT_FAILURE);
  }

  nRet = PencGetCounter(nDevice, nChannel, &dwCounter);
  if (nRet != PENC_ERROR_SUCCESS) {
    printf("Enc error: ret=%Xh\n", nRet);
    PencClose(nDevice);
    if (nRet != PENC_ERROR_SUCCESS) exit(EXIT_FAILURE);
  }
#endif
  
  
  // real time setting
  // if not using real time computing, comment out here.
  ///* 
  memset(&param, 0, sizeof(param));
  param.sched_priority = sched_get_priority_max(policy);
  if (sched_setscheduler(0, policy, &param) < 0) {
    printf("sched_setscheduler: %s\n", strerror(errno));
    printf("Please check you are setting /etc/security/limits.conf\n");
    exit (EXIT_FAILURE);
  }
  if (mlockall(MCL_CURRENT|MCL_FUTURE) < 0) {
    printf("mlockall: %s\n", strerror(errno));
    exit (EXIT_FAILURE);
  }
  //*/ 

  // ---------------------------------- 2 ---------------------------------------   real time loop
  printf("\nnow executing...\n");
  clock_gettime(CLOCK_MONOTONIC, &tsperiod);
  for(i=0;i<TOTAL_DATA_LENGTH;i++){

    clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &tsperiod,0); 

    // read enc
#ifdef ENC_FLAG
    nRet = PencGetCounter(nDevice, nChannel, &dwCounter);
#else
    dwCounter=0;
#endif
    //output_data[i] = (((double)dwCounter)*2.*M_PI)/OVERALL_RESOLUTION;
    if (dwCounter<0x800000) output_data[i] = ((dwCounter)*2.*M_PI)/OVERALL_RESOLUTION;
    else output_data[i] = -((0xFFFFFF - dwCounter - 1)*2.*M_PI)/OVERALL_RESOLUTION;

    if(i==0) velocity[i]=0.;
    else{
      velocity[i]=(output_data[i]-output_data[i-1])/(SAMPLING_TIME_US/1000000.);
      velocity[i]=0.5*(velocity[i]+velocity[i-1]);
    }
    if( fabs(velocity[i])>VELOCITY_LIMITER){
      printf("break by VELOCITY_LIMITER %f (rad/s)\n",VELOCITY_LIMITER);
      printf("veolcity=%f\n",velocity[i]);
      break;
    }

    // write da
    DaData[0] = 2048;	// (2048 for 0 Voltage)
    if(i >= ZERO_DATA_LENGTH){
      da_i = (int)(((INPUT_MAGNITUDE)*2048)/max_voltage);
      if(da_i>2047)  da_i=2047;
      if(da_i<-2048) da_i=-2048;
      DaData[0] += da_i;
    }
#ifdef DA_FLAG
    nRet = DaOutputDA( dnum, 1, &DaSmplChReq[0], &DaData[0] );
#endif
    input_data[i] = (DaData[0]-2048) * max_voltage / 2048;

    // set next clock time
    timespec_add_ns(&tsperiod, control_period_ns);
    clock_gettime(CLOCK_MONOTONIC, &tsnow);
    if (timespec_compare(&tsperiod, &tsnow)<0){
      printf("overruning!\n");
      tsperiod = tsnow;
      timespec_add_ns(&tsperiod, control_period_ns);
    }
  } // for(i;;)



  // --------------------------------------- 3 -------------------------------------------- close

#ifdef DA_FLAG
  DaData[0] = 2048;	// (2048 for 0 Voltage)
  nRet = DaOutputDA( dnum, 1, &DaSmplChReq[0], &DaData[0] );  
  nRet = DaClose(dnum);
#endif

#ifdef ENC_FLAG
  PencClose(nDevice);
  if (nRet != PENC_ERROR_SUCCESS) exit(EXIT_FAILURE);
#endif

  // record data
  fp=fopen(FILE_NAME_DATA, "w");
  if(fp==NULL){
    printf("FILE cannot be opened!\n");
    exit(EXIT_FAILURE);
  }
  for(int j=0;j<i;j++){
    fprintf(fp, "%f,%f,%f,%f\n",
            j*SAMPLING_TIME_US/1000000.,input_data[j],output_data[j],velocity[j]);
  }
  fclose(fp);
  printf("\nfinish!\n\n");

  return 0;
}

