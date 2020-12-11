# Design

Below is an overview of the design of my Flask app.

### General Structure

Significant portions of the general structure of the Flask app were adapted from my solution for Finance (web track). This was because my project and the Finance website share several structural similarities, for example, the usage of user accounts and a similar navigational structure. As such, the register, login, and logout routes are similar to those for Finance (I also used the same `login_required` decorator function from `helpers.py` for the Profile template). In general, each page can be accessed from most of the other pages using the navigation bar, with the exception of pages exclusive to users who are/are not logged in, like Profile or Register.


### HTML templates

To preserve a uniformly styled appearance on all pages of the website, I first created a `layout.html` template from which most of the other templates extend. `layout.html` contains meta tags and includes Bootstrap and Javascript functionalities so that they are accessible to all other templates. `layout.html` also contains the navigation bar, whose links change depending on whether or not the current user is logged in. This was accomplished with a simple Jinja if statement that checks for `session["user_id]`. As a result, almost all pages have common visual styling. The exception is `leaderboard.html`, where the two side-by-side leaderboard tables required `<main>` to be wider than for the other pages. Therefore, I chose to make `leaderboard.html` a standalone template, copying over all the contents of `layout.html`.

### SQL Databases

In `typingtest.db`, there are two tables named `users` and `scores`. `users` stores the username and password hashes of each user along with a primary key. `scores` stores the results of all plays from all users for both test modes. This includes the time, test mode (75 or 150 letters), date achieved, and a foreign key `user_id` that references `users.id`. Since each user can have multiple times recorded, the two-table structure allows multiple results to be connected to one user. From here, SQL queries can be executed to determine all of the stats displayed in the Profile page as well as find the fastest 20 entries in each test mode to display on the leaderboard.

### Login/Register

Creating an account and logging in is accomplished virtually the same way as in Finance (finding a matching entry in `users`). In Finance, I implemented a password length requirement by taking the user to an error page if the password was too short. Here, I used classes to include the requirement directly in the password field to make the process more seamless. Similarly, errors during registration or login cause the user to stay on the same page so they can immediately try again.

### Leaderboard/Profile

The content of the Leaderboard and Profile pages, aside from styling, is simply results from SQL queries. I used Python to parse the objects returned by the SQL queries and passed them to Jinja to display in the template. For the leaderboard, to limit a user to one entry, I used MIN() and GROUP BY to retrieve the best time for each user. For the best time and 10-play average in the Profile page, I used MIN() and AVG() respectively.

### Typing Test

The bulk of the code is found within the typing test itself. To create the test, the first step was to generate a random sequence of characters of the correct length for the user to type. This was done using `random` in Python. Using Jinja, these letters were placed in a `<p>` element in the template. For appearance, I chose to use Consolas, a monospaced font, so that the letters would appear uniform. I also made the maximum width of the `<p>` element such that exactly 25 letters fit on each row, so that depending on the test chosen, the user sees either 3 or 6 complete rows.

To give the appearance of a cursor moving from letter to letter, I created three classes with different CSS attributes for the current letter (black background with white text), previous (correctly typed) letters (green text), and the current letter after pressing an incorrect key (red backgroud, white text). I used Javascript to change between these classes under the correct conditions. Each letter was placed in a `<span>` with a unique id so its appearance could change without affecting the other letters.

The main mechanism that allows the typing test to function is an event listener in Java that calls a function whenever a key is pressed. In this function, a counter is used to keep track of the current letter. The first time this function runs as a result of the key press, the current time is stored using `Date.now()`, which is accurate to the millisecond. When the correct letter is pressed, the function changes the current letter's class to `.correct`, making it green. The next letter's class changes to `.current` to move the "cursor." If an incorrect key is pressed, the function changes the current letter's class to `.incorrect`, which keeps the "cursor" on the same letter but changes the cursor color to red. A counter for mistakes is also incremented. An additional indicator is used to make multiple incorrect key presses on one letter only count as one mistake.

Upon the last letter being typed correctly, the current time is stored. Taking the difference between this time and the time stored at the start gives the time the user took to complete the test. This time is then formatted and displayed, along with the number of letters typed correctly on the first try (i.e. the number of letters in the test minus the number of mistakes), by changing an empty `<p>` element's inner HTML. The same method is used to display a Retry button that links back to the current page.

To save the user's time in the database, the time value must be passed back to Flask from JavaScript. This was done using JQuery's `post()` which sends a `'POST'` request to Flask. Another functionality added with JQuery was to prevent the backspace key from taking the user back a page. I encountered this issue multiple times while testing the typing test, since this particular version of the typing test does not require a user to delete incorrectly typed letters. Although the JQuery completely prevents the backspace key from functioning on the pages with the typing tests, there are no other situations on these pages where the user would need to use the backspace key. Once Flask receives the `'POST'` request, an SQL query is executed to insert the user's results into the database if the user is logged in.



