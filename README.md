# MEEP - a Pomodoro Bot
A productivity Discord bot that sets up Pomodoro sessions for users.

## Commands

### Single Pomodoro Session

*  `;pomo help`: View the Pomodoro help message 
*  `;pomo [time in minutes]`: To start a single Pomodoro session. 
    *   Example: `;pomo 25` to start a 25-minute Pomodoro session. 


### Multiple Chained Pomodoro Sessions
* `;multi [# of sessions] (# min work / # min break)`: To run multiple work/break Pomodoro sessions in a row. Defaults to 25 minutes work and 5 minutes break if no bracket arguments are specified by the user. 
    * Example: `;multi 3 (25/5)` to run 3 25-minute work sessions and 3 5-minute break sessions. 

### Group Study
* React to any `;pomo` command and the bot will add you to that Pomodoro session and ping you when it's complete.
