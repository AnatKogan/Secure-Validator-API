IMAGE=secure-validator-api:latest
NS=devops-exam

build:
	docker build -t $(IMAGE) -f docker/Dockerfile .

run:
	docker run --rm -p 8080:8080 -e APP_SECRET=1234 $(IMAGE)

minikube-load:
	minikube image load $(IMAGE)

k8s-apply:
	kubectl apply -f k8s/00-namespace.yaml
	kubectl apply -f k8s/01-secret.yaml
	kubectl apply -f k8s/02-deployment.yaml
	kubectl apply -f k8s/03-service.yaml

k8s-ingress:
	minikube addons enable ingress
	kubectl apply -f k8s/04-ingress.yaml

pf:
	kubectl -n $(NS) port-forward svc/validator-svc 8080:80
