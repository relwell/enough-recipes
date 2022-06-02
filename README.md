# Enough Recipes!

For the last year or two, recipe search has taken over TODO lists as
the go-to example website.

Funny part about that, of course, is that most of these sites aren't
bootstrapped with a decent number of recipes.

We used to be able to just pull recipes from the
[Recipe Wiki's](https://recipes.fandom.com) MediaWiki API.
Fandom has removed that capability, but fortunately
they still have some API functionality and the capability to scrape content.

So this is a quick and dirty recipe app to kick the tires on
a variety of Vultr's tooling, including:

- Terraform Provider + Modules
- DBaaS
- Load Balancer
- VKE

This is a Django app with many things operationalized into a `Makefile`.

Kuberenetes configs are in the `k8s` folder. Resources you can roll out locally
live in `base`, while the Vultr-specific resources are in `vultr`.

Please note that `k8s/helm` provides scripts for bootstrapping helm charts
with the appropriate configurations to integrate properly with Vultr's
block storage storage class.
