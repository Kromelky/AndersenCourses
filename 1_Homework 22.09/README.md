## Ansible script for FlaskApplication
****

This is ansible playbook file, for deploying Flask application on Debian 10 OS.

Application deploying in /opt/FlaskApplication directory on your remote server.
Project is copping from private [repository](https://github.com/Kromelky/FlaskApplication) with ansible script

Copy it on your Ansible server. Navigate to this directory.
Change target host in inventory.txt.

Before you start playbook change authentication parameters in /group_vars/web_servers.yml

````
ansible_ssh_user=%your remote user name
ansible_ssh_pass=%your user pass 
ansible_sudo_pass=%your sudo pass 
````

For changing application settings such as protocol, port or default location in Andersen role vars section.
(/roles/Andersen/vars). 


#### Remote server requirements

If you're debian 10 using minimal configuration. "sudo" should be installed before you start

````
su -
apt-get install sudo 
````


<!--STATUS=DONE-->









