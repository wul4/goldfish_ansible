# goldfish test environment

## Word of warning
CentOS 7 EOL is Q4 2020  
This environment is not hardened at all, only for testing and playing around!

## About
The goldfish environment can be used to practice making REST API interfaces.  
goldfish itself is a flask-uwsgi web app that provides two REST API's for testing purposes.

The application code can be found in:
```
roles\control\files\goldfish\
```

Playbook `site.yml` deploys a goldfish test environment consisting of web app & nginx loadbalancer nodes.  
Preparation (such as preparing Docker images for nodes) happens on the control node
to centralize the file structure to one machine.

This Ansible directory includes some test scripts to make sure all the nodes are running properly.
See *running tests* for more information about testing the environment

## Components
This image uses the following Docker images:
```
nginx
tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8
```
Tested working using:
```
CentOS Linux release 7.6.1810
ansible 2.9.7
Docker version 19.03.8, build afacb8b
```

The flask app author is unknown, but its API's are based on:  
[connexion](https://connexion.readthedocs.io/en/latest/)  
[dynaconf](https://dynaconf.readthedocs.io/en/latest/)  
[uwsgi-nginx-flask-docker](https://github.com/tiangolo/uwsgi-nginx-flask-docker)


## Getting Started

### Prequisites
Make sure your sudo password prompt is disabled for remote users  
SSH keys should be properly configured, ssh-agent not supported  

If nodes don't have internet access make sure to pre-install
all required packages listed in `common` role tasks.
  
To prepare your control node, run the commands:
```
sudo yum -y install epel-release 
sudo yum -y install ansible jq git
```

cd to your preferred location and clone the repository:
```
git clone git://github.com/wul4/goldfish_ansible.git
cd goldfish_ansible
```

### Change the environment configuration
Configuration can be done in the `hosts` -file.

Define goldfish node addresses, remote usernames, http ports and the Ansible directory path. 
 
If working with multiple lb's, multiple A DNS-records can be defined in case one fails.  


### Playbooks - Deploying the environment
+ You can use the 'ping' module to check if hosts are up:
```
ansible all -m ping -i hosts
```

+ Run the site.yml playbook to deploy the environment  
```
cd goldfish_ansible
ansible-playbook site.yml -i hosts
```


## Running tests
You can browse to your loadbalancer IP for information about the API's:
```
http://LOADBALANCER_IP/api/v2/newapi/ui/
http://LOADBALANCER_IP/api/v1/hello/ui/
```

Test scripts are included to test the behavior of goldfish.

To run tests first set the correct IP-address and execute permission.  
Replace YOUR_LOADBALANCER_IP_HERE:
```
chmod +x test{1,2}.sh
sed -i 's/LOADBALANCER_IP/YOUR_LOADBALANCER_IP_HERE/g' test{1,2}.sh

./test1.sh
------ TEST 1 [OK] ------
------ TEST 2 [OK] ------
Stage 1 tests [OK]

./test2.sh
------ TEST 1 [OK] ------
------ TEST 2 [OK] ------
Stage 2 tests [OK]
```


## Roles
`common`  
Adds Docker repo and makes sure Docker is ready to be deployed.  
This role is used by all the groups by default.

`control`  
The control role prepares the files and Docker images for all of the nodes.

`web`  
Sets up a Docker container running a goldfish webserver using the image provided by control -role.

`lb`  
Sets up a Docker container running an nginx loadbalancer using the image provided by control -role.  
The lb.conf server block configuration file for nginx is templated using jinja2, and will loop the webserver IP's to the loadbalancer config: 
```
ansible/roles/control/templates/lb_conf.j2
```

```
upstream backend {
{% for host in groups['web'] %}
   server {{ host }};
}
...
location / { proxy_pass http://backend; }
```


## To Do
+ Sticky loadbalancing for nginx (not done for the sake of being able to test both web servers easily)
+ Add support for setting up a Docker registry node
+ Add support to spin the needed nodes up on some cloud platform?
+ Add support for using ssh agent
+ Make a hardened version for prod environments (
+ Make a version with tools included for dev environments (image vuln scan etc.)
+ Docker + python-docker installation on offline nodes?
+ Template port into nginx conf and app files 
+ Test Alpine image on nginx
