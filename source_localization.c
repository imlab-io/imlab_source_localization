// source localization example
#include <stdio.h>
#include <string.h>
#include <math.h>

// compute and return \lVert P_k - P_i \lVert
float diffnorm(float *p1, float *p2, int n)
{
    float norm = 0.0f;
    int i = 0;
    for(i = 0; i < n; i++)
    {
        norm += (p1[i] - p2[i]) * (p1[i] - p2[i]);
    }

    return sqrtf(norm);
}

int main()
{
    // set the sample size and dimension
    const int m = 3;
    const int n = 2;

    // set the given parameters
    float Pi[3][2] = {{3.0f,9.0f}, {1.0f,1.0f}, {9.0f,2.0f}};
    float di[3] = {6.0f, 4.0f, 5.0f};

    // set the starting position of the X to somewhere
    float x[2] = {0.0f};

    // continue until the error is no more decreasing
    float difference = 0;
    int iter = 0;
    do
    {
        float xnew[2] = {0.0f};

        // compute \sum_{i \in S}  P_i + \sum_{i \in S}  d_i\frac{P_k - P_i}{\lVert P_k - P_i \lVert}
        int i = 0, j = 0;
        for(j = 0; j < n; j++)
        {
            for(i = 0; i < m; i++)
            {
                xnew[j] += (Pi[i][j] + di[i] * (x[j] - Pi[i][j]) / diffnorm(x, Pi[i], n)) / m;
            }
        }

        // now compute the difference between the xnew and x, and assign x = xn
        difference = diffnorm(x, xnew, n);
        memcpy(x, xnew, n * sizeof(float));

        ++iter;

    } while(difference > 1e-3);


    // print the results
    printf("Optimum position (%5.3f,%5.3f) found in %d iterations!\n", x[0], x[1], iter);

    return 0;
}