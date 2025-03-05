I want LLM to be able to:
- check logs filtered at info level for last x amount of time (get all the logs from nebari and then tell a LLM to create regex to capture all the log types for that pod)
- check nebari config file and nebari config class attribute descriptions
- check nebari docs

- check all (pod, helm chart) health, digging into describe events if resource not healthy
- compare running pods with the expected running pods
- run (predefined?) promql queries / check kuberhealthy checks
- run nebari end to end tests
- check keycloak users, groups, permissions?
- check nebari github issues
- check nebari code
