Sprint 4
Chapter 4/6
Intermediate Python
Web Apps
Web Applications and Where They Live
If you have ever wondered what is behind a website, it is an application running on a server or on a group of servers, which are powerful computers usually hosted in data centers. The larger a web site is, the more sophisticated the application or applications behind it are.
The user interface of large web sites like Amazon, Facebook, or Google represents the ‘tip’ of the vast iceberg of many applications implementing many brilliant ideas running on many powerful servers. Smaller specialized web sites could be presented by just one application running on an entry-level server.
You will learn how to build your own application and host it on a cloud provider’s servers so that anyone could access the user interface of your application without you needing to worry about the infrastructure side (which can be really complicated).
Python and Web Development
Python has grown popular in recent years for developing web applications, winning considerable share in the area among other programming languages, like PHP, Perl, and Ruby. There are two popular generic frameworks (a framework in programming is a library of components that to aid development for a specific task) for web development under Python: Django and Flask, and some specific frameworks like Streamlit especially developed for Data Scientists (examples of web applications made with it can be found here).
We will learn how to build a web application with Streamlit and run it world-wide with Render, a service that provides hosting infrastructure for running applications. We’ll be making a simple application simulating random coinflips.
Render: Initial Configuration
The prerequisites for working with Render are
A Github account, to host a project repository
A Render account, you can get one for free by registering at render.com. You can link your Github account to your render account directly by clicking the “Github” option at signup.
A local Git repository, to host source files and deploy them to Render.
Local installation of git to maintain the local repository.
Render: Creating New App
Make a new Git repository for this lesson. Add the standard Python .gitignore and a README
Render requires at least three files for a Python-based application:
A requirements.txt file, listing of all Python packages required to run the application. Essentially, those are all the packages that the core program explicitly imports. Create a requirements.txt at the project root directory (next to the README.md) with the lines:
pandas==1.3.1
scipy==1.6.2
streamlit==1.12.2 
You could use different version numbers of these 3 packages, but these version numbers are known to work together.
At this point, you should git clone your Git repository to your local machine to work on it further.
We need to add a streamlitspecific configuration file. It should be in .streamlit/config.toml. So first, make a new directory in your Git repository called .streamlit. This directory will tell streamlit to look here for application information. Then, add a file config.toml in this directory with the following contents:
[server]
headless = true
port = 10000

[browser]
serverAddress = "0.0.0.0"
serverPort = 10000 
This tells the application to run in server (headless) mode. Once launched, it will be waiting for someone to connect on the URL address 0.0.0.0 at the port 10000 to respond with the application.
A host is a network location where a server can be found, and a port corresponds to a particular service on that server. This is similar to how a post office can be at one address, and then have many P.O. boxes inside for different people to use.
Render expects applications to serve on port 10000, so we have to set up the .streamlit/config.toml configuration file above to be compatible.
An app.py file (in the project root folder) that will dictate application logic in python
Now, it is a good time to specify what our application will do. Let’s build a simple application which emulates tossing a coin as many times as asked.
A basic Streamlit-based application can be as simple as:
import streamlit as st

st.header('Tossing a Coin')

st.write('It is not a functional application yet. Under construction.') 
Save these lines to app.py so that there are the following files in your local directory:
$ ls -a 
.git .gitignore .streamlit app.py README.md requirements.txt 
Let's commit the changes to make sure the repo is up to date:
$ git commit -am "initial commit"
$ git push 
Testing the App
Let's run the Streamlit application locally. First, make sure streamlit is installed:
pip install streamlit 
Our streamlit application is defined in app.py. To run it locally, use the streamlit run command from the root of your project repository folder:
streamlit run app.py 
The output should link to a URL that will host a webpage with the empty application. If you set the serverAddress to "0.0.0.0" in the configuration, you should enter http://0.0.0.0:10000/ in your browser to see the output.
Deploying to Render
To deploy to Render, first make a Render account tied to your Github account. When making a Render account, choose the “Github” option and follow the signup steps. Then, make a new web service:

image
Next, link the Github repository with the files we just created from your linked Github account to render. To do this, select it in the "make new web service" page:

image
Note: you need to link your Github account to your Render account to see your repositories in the above page.
Now, we'll want to configure the service. For the Render web service to be compatible with a streamlit app, we need a bit of configuration. We already added the configuration for streamlit in the .streamlit/config.toml file in our repository. For Render, we need to add:
In the Build Command section, we add pip install streamlit & pip install -r requirements.txt
In the Start Command section, we add streamlit run app.py
The configuration page will be like this:

image
Make sure the same text is present in the highlighted red boxes.
After this, click the button to start your first launch of the app, and it should start deploying:

image
Wait until the build completes successfully. The deployment takes some time, about 3-10min, to build the application from scratch. After it’s finished, you can open the application URL at https://{APP_NAME}.onrender.com (the exact URL is listed in the upper left of the deployment page) and see the application’s interface.
The build might fail here for various reasons. Here are a few debugging tips:
Can you deploy your app locally on your computer? Navigate to your local repository with the command line and run streamlit run [app.py](http://app.py) Make sure it works on your computer.
Does the build complete on Render? Your build on render.com should reach the “Build successful” stage (highlighted red in the image above). If it doesn’t successfully build, re-deploy it manually (blue button on the top right)
sometimes the build will randomly get stuck, fail, or time out on a free account.
If Render says your deploy was successful, you might still not see your application online at the onrender.com address. This is because the Render free tier shuts down inactive services, and they take 30-60sec to wake up. Refresh the page a few times, over a period of around one minute, and it should load.
When iterating on a project, we encourage you to often run the streamlit app locally (on your computer with the streamlit run app.py command) to quickly check for bugs. This is a faster way to develop than waiting minutes for an online deployment every time you commit.
Render: ‘Expanding’ Application
Now, let’s make our application useful by
adding an element that would allow users to set the number of coin tosses,
adding a button element to start the test,
calculating the mean of two outcomes coded as 0 and 1,
plotting the current progress,
showing a table of results for all runs.
Implementing all this requires widgets. Widgets are ‘construction blocks’ for graphical user interface. Think of a text box for text input fields, a scroll box to navigate a large page, a video player widget where video is displayed, etc.
We will require input widgets (where users input information) as well as output ones (where our application draws results from calculations). 
Luckily, Streamlit provides a good set of elements, described here. Let’s take the following interface elements:
the slider,
the button,
the line chart,
the dataframe dispay.
Adding the slider and the button to the program:
import streamlit as st

st.header('Tossing a Coin')

number_of_trials = st.slider('Number of trials?', 1, 1000, 10)
start_button = st.button('Run')

if start_button:
    st.write(f'Running the experient of {number_of_trials} trials.')

st.write('It is not a functional application yet. Under construction.')
 
Deploy the app locally (or to Render by committing to your Github repo). The behavior of the interface should look as follows to allow user interaction with your app:

image
Now, let’s add the trial outcomes to the user interface, calculating the mean, and displaying how it changes as the trials progress.
First, let’s add the chart variable for the line plot chart, and a the toss_coin function that emulates tossing a coin n times and calculating the mean with every new iteration, which adds to chart (as a new observatio
import scipy.stats
import streamlit as st
import time

st.header('Tossing a Coin')

chart = st.line_chart([0.5])

def toss_coin(n):

    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no +=1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)

    return mean

number_of_trials = st.slider('Number of trials?', 1, 1000, 10)
start_button = st.button('Run')

if start_button:
    st.write(f'Running the experient of {number_of_trials} trials.')
 
Now, let’s make the call of toss_coin as start_button is clicked (gets the True value).
import scipy.stats
import streamlit as st
import time

st.header('Tossing a Coin')

chart = st.line_chart([0.5])

def toss_coin(n):

    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no +=1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)

    return mean

number_of_trials = st.slider('Number of trials?', 1, 1000, 10)
start_button = st.button('Run')

if start_button:
    st.write(f'Running the experient of {number_of_trials} trials.')
    mean = toss_coin(number_of_trials)
 
Now, we can ‘toss’ a coin by clicking run with the application and see an interesting effect of this experiment - the computed mean value is running towards its true value (0.5) as the number of trials grows.

image
Now, let’s add the output to a table with results from all experiments. First, we need to add two stateful variables as keys of st.session_state. The session state is preserved over new runs of the Streamlit application. Then, we add collecting results of experiments in the dataframe kept as st.session_state['df_experiment_results']
import pandas as pd
import scipy.stats
import streamlit as st
import time

# these are stateful variables which are preserved as Streamlin reruns this script
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])

st.header('Tossing a Coin')

chart = st.line_chart([0.5])

def toss_coin(n):

    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no +=1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)

    return mean

number_of_trials = st.slider('Number of trials?', 1, 1000, 10)
start_button = st.button('Run')

if start_button:
    st.write(f'Running the experient of {number_of_trials} trials.')
    mean = toss_coin(number_of_trials)
 
Now, we use these variables to show the dataframe after each run of the application:
import pandas as pd
import scipy.stats
import streamlit as st
import time

# these are stateful variables which are preserved as Streamlin reruns this script
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])

st.header('Tossing a Coin')

chart = st.line_chart([0.5])

def toss_coin(n):

    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no +=1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)

    return mean

number_of_trials = st.slider('Number of trials?', 1, 1000, 10)
start_button = st.button('Run')

if start_button:
    st.write(f'Running the experient of {number_of_trials} trials.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            mean]],
                     columns=['no', 'iterations', 'mean'])
        ],
        axis=0)
    st.session_state['df_experiment_results'] = \\
        st.session_state['df_experiment_results'].reset_index(drop=True)

st.write(st.session_state['df_experiment_results'])
 

image
Submit the latest changes to the git repository
git add .
git commit -am 'version 1'
git push
 
When are the Streamlit stateful variables required?
When we need to keep constant values protected from any change.
When we need to keep values over new runs of a Streamlit application.

Check your answer
HomeSearchCtrlKProgram
Support chat
