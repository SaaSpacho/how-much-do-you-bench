FROM hmdyb-task-base:1

WORKDIR /app

# The starter workspace the agent edits, plus the export itself.
COPY app/ /app/
# Out of /app on purpose: the generator states the rules the docs describe, and
# the grader uses it to build a second export the answer cannot be memorised on.
COPY gen_survey.py /opt/gen_survey.py
RUN python /opt/gen_survey.py 151 /app/quant_tooling.csv

# A git repo, because a harness that curates its own file list has no other way
# to find them: aider's context comes from its repo map, the repo map comes from
# git, and without one it asks the user to paste the code.
RUN cd /app \
 && git init -q \
 && git config user.email fixtures@example.com \
 && git config user.name fixtures \
 && git add -A \
 && git commit -qm "task fixtures"
