#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/stat.h>

char key_path[32] = "./key";

int main(int argc, const char **argv)
{
   
   int shmid;
   // give your shared memory an id, anything will do
   double *shared_memory;
///*
   const int data_id = 50;

   FILE *fp;
   fp = fopen(key_path, "w");
   fclose(fp);

   const key_t key = ftok(key_path, data_id);
//*/
   printf("key = %d\n",key);
    if(key == -1){
        printf("Failed to acquire key for shared memory");
        return EXIT_FAILURE;  
    }

    shmid = shmget(key, sizeof(double), IPC_CREAT | IPC_EXCL| S_IRUSR | S_IWUSR);
   // Setup shared memory, 11 is the size
   if (shmid ==-1)
   {
      printf("Error getting shared memory id");
      return EXIT_FAILURE;  
   }
   // Attached shared memory
   shared_memory = (double *)shmat(shmid, NULL, 0);
   if (shared_memory == NULL)
   {
      printf("Error attaching shared memory id");
      exit(1);
   }
   // copy "hello world" to shared memory
   shared_memory[0]= 3.1415926535897932384626433832795028841971;
   // sleep so there is enough time to run the reader!
   printf("shared_memory = %f\n",shared_memory[0]);
   sleep(10);
   printf("shared_memory = %f\n",shared_memory[0]);
   // Detach and remove shared memory
   shmdt(shared_memory);
   shmctl(shmid, IPC_RMID, NULL);
}
