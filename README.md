# Opendate Yellow

Your Opendate work as a Gen 1 Pokemon battle. Open tickets are wild encounters, your fixes are moves, and milestones are gym badges.

## Play it online

https://claude.ai/artifact/UiNfaG6kWf9SiE3zmu7LSX (private until you share it from the page's Share menu)

A recorded walkthrough is in `opendate-yellow-demo.mp4`.

## Run it locally (1 minute)

```
git clone -b claude/zealous-carson-dw65wj https://github.com/abusch419/work-as-a-game
cd work-as-a-game
python3 -m http.server 8000
```

Open http://localhost:8000. Or just double-click `index.html`.

Controls: arrow keys, Z or Enter = A, X or Esc = B, M = mute. Clicking the screen or the A and B buttons also works. You can click any ticket in the list to battle it.

## Demo script (4 minutes)

1. Press A on the title screen. Oak tells you how many tickets are open.
2. Battle FLAKY TEST. Pick WRITE TEST to get "super effective" (each ticket has a weakness). Watch the terminal under the Game Boy: it writes a failing regression test, patches the code and runs the suite.
3. On LEGACY CODE or PROD INCIDENT, pick CLAUDE CODE. The terminal starts a Claude Code session, shows a plan, edits the file, runs tests and opens a PR.
4. Win and watch the XP, the level up, and a gym badge unlocking on the right.
5. Click PROD INCIDENT (P0, a Voltorb) and battle it with SHIP PR.
6. Try RUN on the Q4 LAUNCH boss. You can't run from Q4.

## How the pitch maps

| Game | Opendate work |
|---|---|
| Wild Pokemon | Linear tickets, failing CI, Sentry alerts |
| Level | Priority and size |
| Moves | SHIP PR (git push + PR + CI), WRITE TEST (red then green), CLAUDE CODE (plan, edit, test, PR), COFFEE |
| Gym badges | Hold Confirmed, Offer Sent, Sold Out Show, Show Settled... |
| Fainting | Burnout, so the ticket goes back to the backlog |

## Where it goes next

1. Pull real tickets from the Linear and GitHub APIs to replace the hardcoded `TICKETS` array in `index.html`.
2. Award XP from merged PRs through a GitHub webhook.
3. Add a shared team leaderboard (Elite Four = top 4 closers this sprint).
4. Push real stats into an actual Pokemon Yellow save file built from the `pret/pokeyellow` disassembly.

## Notes

- Music is the original Gen 1 note data (title, route, wild battle, gym leader battle, victory) compiled from  by  and played with Web Audio. It starts on your first key press. Use the Music button or M to mute.

- Sprites in `sprites/` come unmodified from the `pret/pokeyellow` disassembly. Pokemon is owned by Nintendo and Game Freak, so this is for internal fun only. Don't publish it.
- Everything in the terminal is scripted fake output. No commands run, nothing touches git, GitHub, Linear or Claude.
- Everything runs in a single file (`index.html`) with no build step.
