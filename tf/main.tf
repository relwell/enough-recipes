resource "vultr_kubernetes" "k8s" {
  region  = "ewr"
  label   = "enough-recipes"
  version = "v1.23.5+3"

  node_pools {
    node_quantity = 1
    plan          = "vc2-2c-4gb"
    label         = "enough-recipes"
    auto_scaler   = true
    min_nodes     = 1
    max_nodes     = 2
  }
}
