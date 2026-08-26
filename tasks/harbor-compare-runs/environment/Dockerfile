FROM hmdyb-task-base:1

WORKDIR /app

RUN pip install --no-cache-dir matplotlib

# The starter workspace the agent edits.
COPY app/ /app/
# Out of /app on purpose: the generator states the rules the docs describe, and
# the grader uses it to build a second pair of runs the answer cannot be
# memorised on.
COPY gen_jobs.py /opt/gen_jobs.py
RUN python /opt/gen_jobs.py 151 /app/sample_jobs

# A git repo, because a harness that curates its own file list has no other way
# to find them: aider's context comes from its repo map, the repo map comes from
# git, and without one it asks the user to paste the code.
RUN cd /app \
 && git init -q \
 && git config user.email fixtures@example.com \
 && git config user.name fixtures \
 && git add -A \
 && git commit -qm "task fixtures"
