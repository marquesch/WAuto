# WAuto

Moodle related automations.

External Libraries used:

selenium, gmailapi, tkcalendar, beautifulsoup4, lxml

So far, these are the main implementations:

- UI:
  Simple, but functional(ish) UI to use the main services.

- Login:
  Logs in any of the following Moodle instances:
  ead.uniguairaca.edu.br;
  digita.uniguairaca.edu.br;
  lms.uniguairaca.agencianx.com.br

- Set tiles format:
  Sets the format of a course to tiles
  
- Set block names and images:
  Sets the names and images of the blocks, based on set aliases
  
- Fix quizzes:
  Formats finals and exams.
  Checks if the sum of the questions' marks is equal to the max grade of a given
  quiz. In case it isn't, the script fixes each questions' marks.
  Prints whether a quiz is empty or not
  
- Generate backup:
  Creates a backup file of a course to be restored in the future.
  
- Restore backup:
  Restores a backup of a course into another one, not importing the origin course's
  groups and students.
  
- Insert Questions Bank:
  Consumes a specifically formatted .txt file with all the questions and inserts
  them in a course.
  
- Import Sagah Course:
  Creates Sagah courses and read the external tools infos from the email. Then,
  creates the external tools inside the section of a given Moodle course.

Future:
- Exception handling throughout all the project.
