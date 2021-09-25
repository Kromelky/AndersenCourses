# Docker file for Flask application
****

This docker files builds container for Flask application from Task1.
DockerfileMin building minimal size image with multistage build. (It would be even less if i won't use bs4 in project)

1) For loading prepared image use:
````
docker pull kromelky/awesomezoo
````
2) Start image with:
````
docker run -d -p 8080:8080 kromelky/awesomezoo 
````

3) Open browser http://{%your vm ip/hostname}:8080/

<!--STATUS=DONE-->





