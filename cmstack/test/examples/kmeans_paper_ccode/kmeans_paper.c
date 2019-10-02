#include "kmeans_paper.h"
#include <tgmath.h>


component read_data(_read_data *self)
{
  char *type = self->type;
  char *path = self->path;
  int n = self->n;
  float x[n];
  char *lines[n];
  /* Spring component, read lines from file */
  flow lines_flow = QUEUE(sizeof(lines));
  input lines_iq = INPUT_QUEUE(lines_flow);
  output lines_oq = OUTPUT_QUEUE(lines_flow);
  FREE_QUEUE(lines_flow);
  FREAD(path, ",", n, lines_oq);
  FREE_OUTPUT_QUEUE(lines_oq);
  while (READ(lines_iq, lines))
  {
    /* Read from inputs continually */
    /* Read from states */
    for (int i = 0; i <= n-1; ++i)
    {
      x[i]=FLOAT_CAST(lines[i]);
    }
    /* Write to outputs and states */
    WRITE(self->x, &x);
  }
  FREE_OUTPUT_QUEUE(self->x);
  FREE_INPUT_QUEUE(lines_iq);
}

component init_read_data(_read_data *self, int n, flow x, char *path, char *type)
{
  self->n = n;
  self->x = OUTPUT_QUEUE(x);
  self->path = path;
  self->type = type;
}

component assignment(_assignment *self)
{
  int centers = self->centers;
  int m = self->m;
  float x[m];
  float centroids[centers][m];
  int cluster_assignment;
  double distances[((centers-1)-0)+1];
  while (READ(self->x, x))
  {
    /* Read from inputs continually */
    /* Read from states */
    READ(self->centroids, centroids);
    for (int i = 0; i <= centers-1; ++i)
    {
      double group_0 = 0;
      for (int j = 0; j <= m-1; ++j)
      {
        group_0 = group_0 + (x[j]-centroids[i][j])^2.0;
      }
      distances[i]=pow(group_0,0.5);
    }
    double min;
    min = FLT_MAX;
    int amin[1]
      = { 0 };
    for (int i = 0; i <= centers-1; ++i)
    {
      if (min > distances[i])
      {
        min = distances[i];
        amin[0] = i;
      }
    }
    cluster_assignment=group_0;
    /* Write to outputs and states */
    WRITE(self->cluster_assignment, &cluster_assignment);
    WRITE(self->centroids_oq, &centroids);
  }
  FREE_INPUT_QUEUE(self->x);
  FREE_INPUT_QUEUE(self->centroids);
  FREE_OUTPUT_QUEUE(self->centroids_oq);
  FREE_OUTPUT_QUEUE(self->cluster_assignment);
}

component init_assignment(_assignment *self, int m, flow x, int centers, flow centroids, flow cluster_assignment)
{
  self->m = m;
  self->x = INPUT_QUEUE(x);
  self->centers = centers;
  self->centroids = INPUT_QUEUE(centroids);
  self->centroids_oq = OUTPUT_QUEUE(centroids);
  float centroids_temp[centers][m];
  memset(centroids_temp, 0, sizeof(centroids_temp));
  WRITE(self->centroids_oq, centroids_temp);
  self->cluster_assignment = OUTPUT_QUEUE(cluster_assignment);
}

component update_sum(_update_sum *self)
{
  int centers = self->centers;
  int m = self->m;
  float x[m];
  int cluster_assignment;
  float centroids_sum[centers][m];
  float cluster_sizes[centers];
  while (READ(self->x, x) && READ(self->cluster_assignment, cluster_assignment))
  {
    /* Read from inputs continually */
    /* Read from states */
    READ(self->centroids_sum, centroids_sum);
    READ(self->cluster_sizes, cluster_sizes);
    for (int i = 0; i <= m-1; ++i)
    {
      centroids_sum[cluster_assignment][i]=centroids_sum[cluster_assignment][i]+x[i];
    }
    cluster_sizes[cluster_assignment]=cluster_sizes[cluster_assignment]+1;
    /* Write to outputs and states */
    WRITE(self->centroids_sum_oq, &centroids_sum);
    WRITE(self->cluster_sizes_oq, &cluster_sizes);
  }
  FREE_INPUT_QUEUE(self->x);
  FREE_INPUT_QUEUE(self->cluster_assignment);
  FREE_INPUT_QUEUE(self->centroids_sum);
  FREE_OUTPUT_QUEUE(self->centroids_sum_oq);
  FREE_INPUT_QUEUE(self->cluster_sizes);
  FREE_OUTPUT_QUEUE(self->cluster_sizes_oq);
}

component init_update_sum(_update_sum *self, int m, flow x, flow cluster_assignment, int centers, flow centroids_sum, flow cluster_sizes)
{
  self->m = m;
  self->x = INPUT_QUEUE(x);
  self->cluster_assignment = INPUT_QUEUE(cluster_assignment);
  self->centers = centers;
  self->centroids_sum = INPUT_QUEUE(centroids_sum);
  self->centroids_sum_oq = OUTPUT_QUEUE(centroids_sum);
  float centroids_sum_temp[centers][m];
  memset(centroids_sum_temp, 0, sizeof(centroids_sum_temp));
  WRITE(self->centroids_sum_oq, centroids_sum_temp);
  self->cluster_sizes = INPUT_QUEUE(cluster_sizes);
  self->cluster_sizes_oq = OUTPUT_QUEUE(cluster_sizes);
  float cluster_sizes_temp[centers];
  memset(cluster_sizes_temp, 0, sizeof(cluster_sizes_temp));
  WRITE(self->cluster_sizes_oq, cluster_sizes_temp);
}

component kmeans_train(_kmeans_train *self)
{
  int centers = self->centers;
  int m = self->m;
  float x[m];
  float centroids[centers][m];
  float centroid_sums[centers][m];
  float cluster_sizes[centers];
  flow cluster_assignment = QUEUE(sizeof(int)*1);
  init_assignment(self->assignment_0, m, x, centers, centroids, cluster_assignment);
  init_update_sum(self->update_sum_0, m, x, cluster_assignment, centers, centroid_sums, cluster_sizes);
  FREE_QUEUE(cluster_assignment);
  while (READ(self->x, x) && READ(self->centroids, centroids))
  {
    /* Read from inputs continually */
    /* Read from states */
    cluster_sizes=0;
    centroid_sums=0;
    /* Write to outputs and states */
    WRITE(self->centroid_sums, &centroid_sums);
    WRITE(self->cluster_sizes, &cluster_sizes);
  }
  assignment(self->assignment_0);
  update_sum(self->update_sum_0);
  FREE_INPUT_QUEUE(self->x);
  FREE_INPUT_QUEUE(self->centroids);
  FREE_OUTPUT_QUEUE(self->centroid_sums);
  FREE_OUTPUT_QUEUE(self->cluster_sizes);
}

component init_kmeans_train(_kmeans_train *self, int m, flow x, int centers, flow centroids, flow centroid_sums, flow cluster_sizes)
{
  self->m = m;
  self->x = INPUT_QUEUE(x);
  self->centers = centers;
  self->centroids = INPUT_QUEUE(centroids);
  self->centroid_sums = OUTPUT_QUEUE(centroid_sums);
  self->cluster_sizes = OUTPUT_QUEUE(cluster_sizes);
  self->assignment_0 = malloc(sizeof(_assignment));
  self->update_sum_0 = malloc(sizeof(_update_sum));
}

component update_centroids(_update_centroids *self)
{
  int m = self->m;
  int centers = self->centers;
  float centroid_sums[centers][m];
  float cluster_sizes[centers];
  float new_centroids[centers][m];
  while (READ(self->centroid_sums, centroid_sums) && READ(self->cluster_sizes, cluster_sizes))
  {
    /* Read from inputs continually */
    /* Read from states */
    for (int i = 0; i <= centers-1; ++i)
    {
      for (int j = 0; j <= m-1; ++j)
      {
        new_centroids[i][j]=centroid_sums[i][j]/cluster_sizes[i];
      }
    }
    /* Write to outputs and states */
    WRITE(self->new_centroids, &new_centroids);
  }
  FREE_INPUT_QUEUE(self->centroid_sums);
  FREE_INPUT_QUEUE(self->cluster_sizes);
  FREE_OUTPUT_QUEUE(self->new_centroids);
}

component init_update_centroids(_update_centroids *self, int centers, int m, flow centroid_sums, flow cluster_sizes, flow new_centroids)
{
  self->centers = centers;
  self->m = m;
  self->centroid_sums = INPUT_QUEUE(centroid_sums);
  self->cluster_sizes = INPUT_QUEUE(cluster_sizes);
  self->new_centroids = OUTPUT_QUEUE(new_centroids);
}

component store_data(_store_data *self)
{
  char *type = self->type;
  char *path = self->path;
  int m = self->m;
  int n = self->n;
  float centroids[n][m];
  int epochs;
  while (READ(self->centroids, centroids) && READ(self->epochs, epochs))
  {
    /* Read from inputs continually */
    /* Read from states */
    /* Write to outputs and states */
  }
  FREE_INPUT_QUEUE(self->centroids);
  FREE_INPUT_QUEUE(self->epochs);
}

component init_store_data(_store_data *self, int n, int m, flow centroids, flow epochs, char *path, char *type)
{
  self->n = n;
  self->m = m;
  self->centroids = INPUT_QUEUE(centroids);
  self->epochs = INPUT_QUEUE(epochs);
  self->path = path;
  self->type = type;
}

component main_component(_main_component *self)
{
  flow train_data = QUEUE(sizeof(float)*784);
  flow centroids = QUEUE(sizeof(float)*10*784);
  flow new_centroids = QUEUE(sizeof(float)*10*784);
  flow centroid_sums = QUEUE(sizeof(float)*10*784);
  flow cluster_sizes = QUEUE(sizeof(float)*10);
  init_read_data(self->read_data_0, 784, train_data, "data/train.csv", "csv");
  init_kmeans_train(self->kmeans_train_0, 784, train_data, 10, centroids, centroid_sums, cluster_sizes);
  init_update_centroids(self->update_centroids_0, 10, 784, centroid_sums, cluster_sizes, new_centroids);
  init_store_data(self->store_data_0, 10, 784, new_centroids, 5, "data/model.csv", "csv");
  FREE_QUEUE(train_data);
  FREE_QUEUE(centroids);
  FREE_QUEUE(new_centroids);
  FREE_QUEUE(centroid_sums);
  FREE_QUEUE(cluster_sizes);
  read_data(self->read_data_0);
  kmeans_train(self->kmeans_train_0);
  update_centroids(self->update_centroids_0);
  store_data(self->store_data_0);
}

component init_main_component(_main_component *self)
{
  self->read_data_0 = malloc(sizeof(_read_data));
  self->kmeans_train_0 = malloc(sizeof(_kmeans_train));
  self->update_centroids_0 = malloc(sizeof(_update_centroids));
  self->store_data_0 = malloc(sizeof(_store_data));
}

int main()
{
  _main_component *main_0 = malloc(sizeof(_main_component));
  init_main_component(main_0);
  main_component(main_0);
}

