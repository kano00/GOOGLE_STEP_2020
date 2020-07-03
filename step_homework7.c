#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#define FOR(i,n) for(i=0;i<n;i++)

double get_time()
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec + tv.tv_usec * 1e-6;
}

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        printf("usage: %s N\n", argv[0]);
        return -1;
    }

    int n = atoi(argv[1]);
    double *a = (double *)malloc(n * n * sizeof(double)); // Matrix A
    double *b = (double *)malloc(n * n * sizeof(double)); // Matrix B
    double *c = (double *)malloc(n * n * sizeof(double)); // Matrix C

    // Initialize the matrices to some values.
    int i, j, k;
    for (i = 0; i < n; i++)
    {
        for (j = 0; j < n; j++)
        {
            a[i * n + j] = i * n + j; // A[i][j]
            b[i * n + j] = j * n + i; // B[i][j]
            c[i * n + j] = 0;         // C[i][j]
        }
    }

    double begin = get_time();

    FOR(k,n)FOR(j,n)FOR(i,n)c[i * n + j] = a[i * n + k] + b[k * n + j];

    double end = get_time();
    printf("time: %.6lf sec\n", end - begin);

    /*
    n=1000　それぞれで３回実験
    i-j-k, time: 6.435926 sec　time: 6.136926 sec　time: 5.778343 sec
        平均time 6.117065 sec
    i-k-j, time: 3.169195 sec　time: 3.561532 sec　time: 3.087432 sec
        平均time 3.27271966667 sec
    j-i-k, time: 4.369725 sec　time: 4.338378 sec　time: 4.439861 sec
        平均time 4.38265466667 sec
    j-k-i, time: 9.149553 sec　time: 9.106518 sec　time: 8.974975 sec
        平均time 9.07701533333 sec
    k-i-j, time: 3.115564 sec　time: 3.126683 sec　time: 3.183471 sec
        平均time 3.141906 sec
    k-j-i, time: 7.762348 sec　time: 8.642236 sec　time: 7.813609 sec
        平均time 8.072731 sec
    i-k-j < k-i-j < j-i-k < i-j-k < k-j-i < j-k-i 
    */ 

    // Print C for debugging. Comment out the print before measuring the execution time.
    double sum = 0;
    for (i = 0; i < n; i++)
    {
        for (j = 0; j < n; j++)
        {
            sum += c[i * n + j];
            // printf("c[%d][%d]=%lf\n", i, j, c[i * n + j]);
        }
    }
    // Print out the sum of all values in C.
    // This should be 450 for N=3, 3680 for N=4, and 18250 for N=5.
    printf("sum: %.6lf\n", sum);

    free(a);
    free(b);
    free(c);
    return 0;
}