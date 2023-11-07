# Product Line
### Use-Case model:
![Use-Case model](https://user-images.githubusercontent.com/94874872/200014466-e833f971-0d6b-4c0d-b6e0-81e1c6ceed63.jpg)
  There are three actors in the Use-Case model: Super User, Ordinary User and Guest User. Guest users are allowed to perform basic functions in the application, while Ordinary users perform more advanced functions related to their personal account created when they are Guest users. The Super user oversees the application management with functions that let them process requests from the other two types of users and make decisions with those requests such as banning, warning and collecting statistics for the application. 
### Other features:
- Removed OUs are banned without access to the application 
- A blacklist for items removed by SUs 
- An adaptive GUI where an OU can login directly to a certain page based on their interest 
