# customer-satisfaction-form
Database:
  There are 4 Django models in this app:
    * Question - this stores the text, help_text, type (either email, name, short text, long text, 1-5 rating, 1-10 rating or multi-select with built in support for elaboration if the "Other" option is selected), version, is_active status, is_required status and display order (automatically assigned but can be manually updated) of all questions.
    * Option - this stores the label, display_order (automatically assigned but can be manually updated) and is_active status for each option in multi-select questions through a ForeignKey.
    * Submission - this stores the submission time, name, email and client (derived from domain of email) of each submission.
    * Answer - this stores the value and display_order of each answer in a response. It uses a ForeignKey link to connect to the Submission and Question models.

  The Question and Option modules contain an is_active field to encourage deactivation rather than the deletion of records to prevent confusion whilst viewing the records in the Answer model.
---
Customer Form:
  The customer form pulls data from the Question and Option models and uses custom tags and widgets to create an html form with the proper layout and type for each question. In main.html, Django logic is used to loop through every active question in the Question model and do the following:
    Create an h3 header with the question text and a red *