resource "vultr_kubernetes" "k8s" {
  region  = "ewr"
  label   = "enough-recipes"
  version = "v1.23.5+3"

  node_pools {
    node_quantity = 2
    plan          = "vc2-4c-8gb"
    label         = "enough-recipes"
    auto_scaler   = true
    min_nodes     = 1
    max_nodes     = 3
  }
}

# this is an object storage instance,
# which contains multiple buckets.
# there is not presently a tf provider
# for a bucket inside an object storage instance
resource "vultr_object_storage" "tf" {
  cluster_id = 2
  label      = "enough-recipes-assets"
}
