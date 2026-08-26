# How Much Do You Bench? 🏋️

A hackathon where every team gets the same model and competes on everything
else: harness, skills, MCP servers, context engineering.

The model is Google's [Gemma 4 31B](https://huggingface.co/google/gemma-4-31b).
The weights are Apache-2.0 and it is small enough to run on your own hardware.

We run the gateway, the graders and the workspaces. You only have to work on
your agent.

## What a benchmark is

A benchmark is a fixed set of tasks plus a grader that says pass or fail for
each one. Because everyone runs the same tasks, the scores can be compared.

Here everyone also gets the same model, through the same gateway. That is on
purpose: the model is held still so that any difference on the board comes
from what you build around it. Which harness you pick, what tools it can call,
what you put in its context, how the prompt is worded.

One task is one Docker container. Your agent starts inside it with a short
instruction file and the files the task needs. It gets a time limit and a turn
limit. When it stops, a script we wrote checks the result and writes a 1 or a
0. There is no partial credit and no human reading your work.

Your day is one loop: run a task, read the trajectory, change one thing, run it
again. You are not writing the answer to a task. You are building an agent that
works out answers to tasks you have not seen.

## Start here

You need [Docker](https://docs.docker.com/get-started/), [uv](https://docs.astral.sh/uv/),
[just](https://github.com/casey/just) and [harbor](https://pypi.org/project/harbor/),
plus the team key from the kickoff message. The Conveyor IDE has the tools
already, so this list is for working on your own machine.

```
export GATEWAY_API_KEY=sk-...   # your team key, and your identity when you submit
just eval                       # run a task against your agent
just view                       # read the trajectory
just submit                     # when you want it scored
```

During the hackathon you work in a Conveyor IDE that already has this repo
checked out and can reach the gateway. Fork the repo from there:

```
gh auth login
gh repo fork --remote
git push -u origin main
```

**Keep the fork public.** The grader clones it without credentials, so a
private one passes `just submit` and then fails all seventeen rollouts.

`agent.yaml` picks your agent. Four are ready to use:

- [opencode](https://opencode.ai/docs/)
- [pi](https://pi.dev/docs/latest)
- [claude-code](https://docs.claude.com/en/docs/claude-code)
- [trae-agent](https://github.com/bytedance/trae-agent)

`agent.yaml` is also where you attach skills and MCP servers, and where you
set the system prompt: see the commented block on the opencode entry. Write
your own agent in `agent/` only if you want to.

`opencode.json` is for you, not for the benchmark. It points opencode at
Claude on Bedrock in the IDE's own account, so you can use it while you work.
Rollouts ignore it: they run in the task container, where this repo is not
checked out, and the model there is always Gemma through the gateway.

`tasks/` holds seven sample tasks to develop against.

`just eval` mounts your working tree, so you can edit and re-run without
committing. The model runs on the shared gateway; only the task container runs
locally. `just view` then shows every message and every tool call, which is
where you find out what your agent actually did.

## Layout

| Path | What it is |
|---|---|
| `tasks/` | Five sample tasks. One directory per task: Dockerfile, fixtures, pytest verifier |
| `agent/` | Your own agent, if you write one. A uv project with a fixed entrypoint, and the baseline to beat |
| `docs/` | Design notes |
| `adapter/` | Starts your `agent/` inside the task container and hands it the gateway, the skills and the MCP config. Read it if you write a custom agent |

Edits to `tasks/` and `adapter/` change your local runs only. `just eval`
builds the task image from your working tree, so they take effect at once,
including edits to the shared `tasks/base` image every task is built `FROM`.
Grading uses the instructor's copy, so a tool you install in `tasks/base` is
missing when it counts, and a task you fixed locally is the original one when
it is scored. `just eval` says so when they differ.

To change what a graded rollout gets, edit `agent.yaml`: harness, skills, MCP
servers, kwargs. The server checks it at submit time.

## What you are scored on

The five tasks in `tasks/` are samples and none of them counts. Your score
comes from seventeen tasks you never see, in a private repo, baked into the
grading worker.

The graders and the reference solutions have to live somewhere. While they
lived here, a team could read the expected output and write it into its agent
instead of solving anything. Public dev split, private test split, as
SWE-bench and ARC-AGI do it.

So tune for the general case. An agent that pattern-matches the samples scores
nothing. The scored tasks are the same kind of work, data engineering in one
container with a verifier that passes or fails, over the same ground: SQL and
dataframes, dbt and Airflow, Terraform, shell and git, survey exports whose
rules live in a codebook, reading someone else's run output. They are
harder on purpose.

Pick a sample you lose, find where your agent goes off the rails, fix the
context, run it again.

## Pointers

Ideas worth trying. None of them is required.

**Give the model documentation.** It is a small model with a training cutoff,
and a lot of failures are just a wrong API call. The
[context7](https://github.com/upstash/context7) MCP server looks up current
docs for a library on demand, so the agent can check the polars, dbt or
Terraform API instead of guessing at it:

```yaml
    mcp_servers:
      - name: context7
        transport: streamable-http
        url: https://mcp.context7.com/mcp
```

The transport matters. `mcp_servers` defaults to `sse`, and this server speaks
streamable-http, so leaving it out gets you a server that never connects.

**Give the model instructions for one kind of work.** A skill is a file of
instructions the agent reads when a task matches it. The polars team publish
theirs at [polars-inc/skills](https://github.com/polars-inc/skills). Several
tasks are dataframe work, so those are useful directly, and they also show how
a skill is written.

Copy the one you want into your own repo and point at the directory:

```
git clone --depth 1 https://github.com/polars-inc/skills /tmp/polars-skills
cp -r /tmp/polars-skills/polars skills/polars
```

```yaml
    skills:
      - ./skills/polars
```

A graded run only accepts a path inside your commit or the `org/repo@ref`
shorthand, and that shorthand always looks in a `skills/` directory at the root
of the repo it names. `polars-inc/skills` keeps its skill in `polars/`, so
`polars-inc/skills@main` finds nothing, says nothing, and you are scored with
no skill attached. Copying it in is also what makes your run reproducible: the
skill is pinned in your commit rather than tracking someone else's branch.

**Turn reasoning on.** The model can reason, but most harnesses do not ask it
to, and a harness that reasons before it acts makes different mistakes. opencode
is set up for it in `agent.yaml` already. pi is not: it defaults to thinking
off, and needs `kwargs: {thinking: high}`. Watch what changes in the trajectory
rather than assuming more thinking is better.

**Say less, but say the right thing.** A long system prompt is not a better
one. This model has 256K of context, but it gets one tool call per turn, so
every wasted turn costs you. Cutting instructions the agent ignores often
helps more than adding new ones.

**Watch the token count.** The board has two axes, tasks passed and tokens
spent, and draws the frontier of submissions nobody beat on both at once. An
agent that passes the same tasks for fewer tokens is on it; one that passes
fewer tasks and spends more is not.

## Submitting

```
just submit
```

It refuses uncommitted or unpushed work and sends the full commit hash. Both
would otherwise fail twenty minutes later. The server also reads the
`agent.yaml` in your commit before accepting it, so a config grading would
refuse costs you a rejection now rather than a submission later.

You get ten submissions of the full suite. Local runs are unlimited and
unscored. `just cancel <id>` stops one you no longer want, but does not give
it back.

## Operating the benchmark

Deployment, architecture and grading internals live in the instructor
repository, along with the scored tasks. You need none of it to compete.
