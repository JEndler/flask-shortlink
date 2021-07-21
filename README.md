# flask-shortlink
flask-shortlink is an short, self-hostable open-source link shortening web application. 
It allows you to host your own URL shortener, to brand your URLs, and to gain control over your data. flask-shortlink is especially easy to use, and provides a modern, themable feel.

## Quickstart
flask-shortlink is a flask-application written in Python3, using the shelve module as its primary data storage.

To get started with flask-shortlink on your server, you need to install Poetry[https://python-poetry.org/]. 
You can clone this repository, then just type "poetry install" and all the necessary dependencies will be installed.

You can then use a production Webserver of your choice to host this app.

### Demo

The default landing page looks like this:

<img src="https://i.imgur.com/gDtQQot.png" width="350px" alt="shortlink" />

Additionally, there is an Analytics Page for every created shortlink, which tracks the total Number of views and provides a graph.

<img src="https://i.imgur.com/7qblXjx.png" width="350px" alt="analytics" />
