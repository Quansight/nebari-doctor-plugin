from nebari_doctor.agent import run_agent

if __name__ == '__main__':
    user_issue = 'My user ad tried to shut down the My Panel App (Git) app started by Andy.  The Jupyterhub landing page said "Server stopped succesfully", bu tthe Status of the dashboard remained "Running".  What\'s going on?'

    run_agent(user_issue)