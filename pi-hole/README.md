# pi-hole
run pi-hole container
Pi-hole is a Linux-based web application that we are using to protect our network from intrusive advertisements while also blocking internet tracking systems. This is a simple to use network that is suited for home and small office use to large scale company. In advance, we are using it to manage the accessibility and blocklist unwanted content.
Starting with a setup in a docker container:
First step by using this command in figure 1 to download pi-hole: 

```sudo docker pull pihole/pihole```

After that we used Docker composer tool that allow us to define the services on that specific container to easily manage different services at once. We need to create a YAML file.

```docker-compose up -d```

In order for Pi-hole to occupy a docker container we use this command:

```sudo docker exec -it pihole bash```

Change pihole password:

```pihole -a -p```

To open Pi-hole on a web browser we type in the searching bar "http://localhost/admin/"  and we can see Pi-hole is running perfectly:
![image](https://user-images.githubusercontent.com/86531445/159133503-d36bf548-82a4-43a1-b4b6-fe74cc507159.png)

Now, the raspberry pi default dns server should be changed to pi-hole IP address (the ip that docker0 interface has assigned)
To show IP address of pi-hole container:

```docker inspect pihole | grep IPAddress```

In this project, the container IP Address is 172.18.0.2
Next, navigate to dhcpcd.conf file:

```sudo nano /etc/dhcpcd.conf```

Scroll down to “#static domain_name_servers=” to uncomment it, after that, set the IP address of the pi-hole container.

```1static domain_name_servers=172.18.0.2```

Lastly, restart the dhcpcd daemen:

```sudo service dhcpcd restart```