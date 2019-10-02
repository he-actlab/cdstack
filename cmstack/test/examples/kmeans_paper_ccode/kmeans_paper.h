#include "utils.h"


typedef struct _read_data
{
  int n;
  output x;
  char *path;
  char *type;
}  _read_data;

typedef struct _assignment
{
  int m;
  input x;
  int centers;
  input centroids;
  output centroids_oq;
  output cluster_assignment;
}  _assignment;

typedef struct _update_sum
{
  int m;
  input x;
  input cluster_assignment;
  int centers;
  input centroids_sum;
  output centroids_sum_oq;
  input cluster_sizes;
  output cluster_sizes_oq;
}  _update_sum;

typedef struct _kmeans_train
{
  int m;
  input x;
  int centers;
  input centroids;
  output centroid_sums;
  output cluster_sizes;
  _assignment *assignment_0;
  _update_sum *update_sum_0;
}  _kmeans_train;

typedef struct _update_centroids
{
  int centers;
  int m;
  input centroid_sums;
  input cluster_sizes;
  output new_centroids;
}  _update_centroids;

typedef struct _store_data
{
  int n;
  int m;
  input centroids;
  input epochs;
  char *path;
  char *type;
}  _store_data;

typedef struct _main_component
{
  _read_data *read_data_0;
  _kmeans_train *kmeans_train_0;
  _update_centroids *update_centroids_0;
  _store_data *store_data_0;
}  _main_component;

component read_data(_read_data *self);

component init_read_data(_read_data *self, int n, flow x, char *path, char *type);

component assignment(_assignment *self);

component init_assignment(_assignment *self, int m, flow x, int centers, flow centroids, flow cluster_assignment);

component update_sum(_update_sum *self);

component init_update_sum(_update_sum *self, int m, flow x, flow cluster_assignment, int centers, flow centroids_sum, flow cluster_sizes);

component kmeans_train(_kmeans_train *self);

component init_kmeans_train(_kmeans_train *self, int m, flow x, int centers, flow centroids, flow centroid_sums, flow cluster_sizes);

component update_centroids(_update_centroids *self);

component init_update_centroids(_update_centroids *self, int centers, int m, flow centroid_sums, flow cluster_sizes, flow new_centroids);

component store_data(_store_data *self);

component init_store_data(_store_data *self, int n, int m, flow centroids, flow epochs, char *path, char *type);

component main_component(_main_component *self);

component init_main_component(_main_component *self);

