# Random Letter Typing Test

The Random Letter Typing Test is a Flask app located within CS50 IDE. Below are instructions for running and using the website.

### Getting Started

First, navigate to the directory containing the source code for the project and execute `flask run`. The server will start. Click on the link shown to open the website. You should see the homepage. At the top is a navigation bar with links to the homepage itself and the leaderboard, as well as links to register an account and log in. Since no account is logged in, a blue alert bar is shown informing the user to log in to save typing test scores. Below is a short description and buttons to the two test modes (75 letters and 150 letters.)

### Creating an Account

It is highly recommended to create an account before proceeding. Creating an account allows a user's scores and statistics to be saved and allows a user's best scores to be recorded on the leaderboard. If you wish to use the website without making an account, skip to "Taking the Test," below.

To create an account, click on the "Register" link on the navigation bar. You will see a form with username, password, and password confirmation fields. A password must be at least 8 characters in length, and the password confirmation must match the above password. Once all the fields have been filled out, click on the Register button to create an account. You will be redirected to the login page.

### Log In

Input your username and password, then click on the button below to log in. If the username and password combination is not found, the login page will reload with a message that the username or password is incorrect. Upon successful login, you will be redirected to the home page. The navigation bar has links to the home page and the leaderboard as before, but the links to register and log in are replaced with links to view your profile and log out. The alert bar is also no longer displayed.

### Taking the Test

From the homepage, click on either button to take the corresponding test. You will see brief directions followed by the block of letters you will type. The cursor is on the first letter, as indicated by the inverted color. When a key is pressed, the timer will begin. Type the letter at the cursor's position to advance to the next letter. If the correct key is pressed, the cursor will advance, and the letter typed will turn green. If the incorrect key is pressed, the cursor will turn red. The cursor will not advance until the letter is correctly typed. Once you have typed all the letters correctly, the timer will stop. Your time will be displayed at the bottom of the screen along with the number of letters typed correctly on the first try. If you are logged in, you score will be saved automatically. Click the Retry button or refresh the page to try again.

### Viewing the Leaderboard

From any page, click on the "Leaderboard" link in the navigation bar to view the leaderboard. There are separate leaderboards for the 75 and 150 letter tests. The top 20 times are shown alongside the corresponding usernames. Only a user's best time is shown on the leaderboard, so no user can appear on one of the leaderboards twice.

### Viewing your Profile

When logged in, click on the "Profile" link in the navigation bar to view your profile. Your username will be shown in the heading. Separate stats are displayed for the two tests. For each test, you will be able to view the number of times you have played, your best time, and the average time of your most recent 10 plays. If you have not played yet, your best time and 10-play average will display N/A. If you have played less than 10 times, your 10-play average will be calculated by averaging all of your times.

### Log Out

When logged in, click on the "Log Out" link in the navigation bar to log out. You will be redirected to the homepage. Note that once logged out, you will still be able to take typing tests, but your scores will not be saved and will not be shown on the leaderboard.