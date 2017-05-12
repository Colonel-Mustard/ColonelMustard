## Synopsis

A bot written in Python that plays [Tribal Wars](https://www.tribalwars.us).
## Code Example

```bazaar
cm = BasicBot.BasicBot()
cm.do_login()
cm.update_state()

# Show some resource data
print("[*] Village iron:", cm.state['village']['iron'])
print("[*] Village stone:", cm.state['village']['stone'])
print("[*] Village wood:", cm.state['village']['wood'])
```
## Motivation

Finally, a free, open-source Tribal Wars bot! The bold end-goal of this project is to create an AI that can compete with human players. However, a secondary (more achievable) goal is to create a tool that will help players manage their villages.
## Installation

Make sure Python3 and the Python Requests library are installed. Move `.env_example.json` to `.env.json` and fill in all the necessary variables. At this point the only way to run the bot is to create a script that imports the `BasicBot` module. 
## Contributors

Contributors of all levels welcome! There are plenty of TODO's scattered around the source, so if you don't know where to start, look at one of those. Forks/PRs are encouraged. This project is intended as a community effort.

### Development Workflow
Installing burpsuite (the free version should be sufficient for basic debugging) and setting up an intercept proxy is recommended. Running the project in 'debug' mode (specified in the .env.json file) will redirect all traffic to localhost:8080. More info about burp [here](https://portswigger.net/burp/)