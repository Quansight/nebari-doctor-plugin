#  Nebari Doctor

This plugin uses an AI agent to attempt to diagnose your issue with Nebari.

# How it works
Build a nebari doctor LLM functionality
- user describe issues
- LLM gets context:
    - pod logs (1.5M words)
    - code base (260K words)
    - nebari docs (224K words)
        - FAQ
    - search/look at open github issues
    - search/look at discussions
- system prompt describes Nebari, tell user what is wrong

Too many words for most LLMs context so, we'll have an agent assess which pod logs it thinks are going to be most useful or look at all sequentially and assess if they look useful or not.