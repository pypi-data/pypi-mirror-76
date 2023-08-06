fwiffo
======

a self-deploying bot

stage 1
-------

Run from Raspberry Pi:

1) Installs latest version of Terraform
2) Deploys Digital Ocean single-node Nomad cluster
3) registers DNS zone for fwiffo.scupper.org

stage 2
-------
1) Joins single-node Nomad cluster (as second node)
2) sync lmdb DB between each node
3) Bookmark management web app


notes
-----
2020.08.03

Raspberry Pi setup

$ sudo snap docker install

looking at docker in userspace
https://docs.docker.com/engine/security/rootless/

it is unclear how well supported this is for the snap install of docker
on Raspbian 10. i may "give up" and try a docker-rootless manual install


docker-rootless install notes:
manually edit install script to change `uname -m` instances and manually
specify `armhf` instead.

sudo apt install slirp4netns

nothing worked very well. need to learn more about docker xpile
