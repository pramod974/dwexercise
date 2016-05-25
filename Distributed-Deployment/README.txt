* "deployME" is the folder contents which i wanna deploy , You can pass through command line arguments
            example:
             python.exe /home/ec2-user/exercises/Distributed-Deployment/deploy.py /home/ec2-user/exercises/Distributed-Deployment/deployMe


* Run the python file deploy.py to invoke the simulation

* The Number of Machines , Failure percentage and time to recovery ("t") are as follows by Default
    500 10 5 (You can Change the defaults at line 55 !)
* The deploy thread first deploys to all alive machines and then deploys on Recovered Machines as and when available with the probe running every "t" seconds i.e 5 !
   The Implementation is kept simple due time constraints :)
   Merkel Tree is used to verify the contents
* The Console Out Put shows the simulation
