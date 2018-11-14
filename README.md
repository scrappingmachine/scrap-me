# scrap-me 
[![CircleCI](https://circleci.com/gh/scrappingmachine/scrap-me/tree/master.svg?style=svg)](https://circleci.com/gh/scrappingmachine/scrap-me/tree/master)
[![Build Status](https://travis-ci.org/scrappingmachine/scrap-me.svg?branch=master)](https://travis-ci.org/scrappingmachine/scrap-me)

**Scrap-me** allows you to get hotel reviews from [tripadvisor](https://www.tripadvisor.com).
It supports reviews in two languages: polish and english. Results are saved in Minio.

## Technologies
### Kubernetes
We are using kubernetes to manage containers. 
To run kubernetes cluster we are using minikube.

### Helm
Helm is used to automate and simplify deployment process. Minio and RabbitMQ charts are taken from 
kubernetes charts [link](https://kubernetes-charts.storage.googleapis.com).
Additionally helm creates 2 secrets: one for Minio credentials, second for RabbitMQ.
Scrapper deployment is defined in a separate subchart.


### Docker Hub
Scrapper image is kept in public repository in [Docker Hub](https://hub.docker.com/r/scrappingmachine/scrap-me/)

### CircleCI
CircleCI is responsible for:
* building project
* running deployment
* running style check
* running tests
It is also integrated with Github: each PR requires passing CircleCI checks.

### Travis
Travis is another tool for CI used in our project. It runs style check and tests.

## Environment preparation
* install docker
* install minikube
* install helm
* install kubectl
* run k8s cluster `minikube start`
* install helm in cluster
```bash
kubectl -n kube-system create sa tiller
kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
helm init --wait --service-account tiller
```
in case of problem with RBAC role, please run `kubectl create clusterrolebinding add-on-cluster-admin --clusterrole cluster-admin --serviceaccount=kube-system:default`

## Deployment
* build project and push new image to Docker Hub (you need to login to docker first)
	* `make build`
	* `make push`
* if you want to use custom `scrap-me` image, please override `image`/`tag` value/values used by 
scrap-me-chart
* run `helm dep up helm-deployment/` to get minio and rabbitmq
* run `helm install helm-deployment` to deploy project
	* additional options (please check helm-deployment/ to get more info)
		* set workerArgs variable to choose reviews language
		* set dispatcherArgs variable to choose city/region

## Troubleshooting
RabbitMQ and Minio are not exposed (there are no external IP).
If you need to get access to RabbitMQ/Minio web interfaces, then please use port-forwarding on 
RabbitMQ/Minio pod.
Example:
```bash
kubectl port-forward rabbit_mq_pod_name 15672:15672 &
kubectl port-forward minio_pod_name 9000:9000 &
```
Then you can access RabbitMQ panel with localhost:15672 and Minio panel with localhost:9000.g
