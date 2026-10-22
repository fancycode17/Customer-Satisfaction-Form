# customer-satisfaction-form
## Setup

**If using zip file:**
1. Download zip
2. Extract zip, open in editor

**If using git clone:**
1. Run: `git clone https://github.com/fancycode17/Customer-Satisfaction-Form.git`
2. Run: `cd Customer-Satisfaction-Form`

**Then:**
3. Create a virtual environment: `python -m venv .venv`
4. Activate the virtual environment:
  * If using Windows Command Prompt (cmd): `.venv\Scripts\activate.bat`
  * If using Windows PowerShell: `.venv\Scripts\Activate.ps1`
  * If using macOS/Linux bash/zsh: `source .venv/bin/activate`
  * If using macOS/Linux fish: `source .venv/bin/activate.fish`
5. Install requirements.txt: `pip install -r requirements.txt`

## Running the Program

1. Navigate to `customer-satisfaction-form/main`
2. Run: `python manage.py runserver`


## Database

There are 4 Django models in this app:

* **Question** – stores the text, help_text, type (email, name, short text, long text, 1–5 rating, 1–10 rating, or multi‑select with “Other” elaboration), version, is_active, is_required, and display_order.
* **Option** – stores the label, display_order, and is_active status for each option in multi‑select questions.
* **Submission** – stores submission time, name, email, and client (derived from email domain).
* **Answer** – stores the value and display_order of each answer, linked to Submission and Question via ForeignKey.

The Question and Option models use an `is_active` field to encourage deactivation rather than deletion, preventing confusion when viewing Answer records.

---

## Customer Form

The customer form pulls data from the Question and Option models and uses custom tags and widgets to create an HTML form with the correct layout and input type for each question.

In `main.html`, Django loops through every active question and:

* Creates an `<h3>` header with the question text and a red `*` if the question is required.
* Uses custom tags and widgets to create an appropriate input element for the question type by:
  1. Checking the question type: `{% if q.type == 'EMAIL' %}`.
  2. Calling the appropriate tag using the question and submitted_data (for if the form was reloaded after an invalid submission): `{% email_input q submitted_data %}`.
  3. To return values to the widget the tag is registered: `@register.inclusion_tag('widgets/email_input.html')`.
  4. relevant submitted_data is extracted and returned to the widget along with other parameters: `'value': submitted_data.get(f'question_{q.id}', '')`.
  5. If the question contains help text then a label is added.
  6. An input element is created using the parameters provided: `<input type="email" id="question_{{ q.id }}" name="question_{{ q.id }}" value="{{ value }}" placeholder="{{ placeholder }}" {% if q.is_required %}required{% endif %}>`.

After the form is successfully submitted, the customer is redirected to a Thank You page.

---

## Processing Form Data

Once a POST request has been made by the customer form, the post data is sent to a function called check_errors(), which does the following:

* Get all the active Question records: ```Question.objects.filter(is_active=True)```
* Loop through each question attempts to find the corresponding answer in the post data: <pre>key = f'question_{q.id}'<br>value = post_data.get(key, '')</pre>Or, for multiple choice questions:<pre>selections = post_data.getlist(key)<br>other_detail = post_data.get(f'other_detail_{q.id}','')</pre>
* Validate submission data based on question type
* Return `submitted_data` and a dictionary of errors

If an empty dictionary of errors is returned (i.e. no errors):

* Create a Submission (`submission = Submission.objects.create(...`:
  * Set the `submitted_at` field to the current time: `submitted_at=datetime.now(),`
  * Filter the post data for a key which contains the question id of a question of type "NAME", and set the `name` field of the submission to the key's corresponding value (or "N/A" if there was no answer to a question of type "NAME"): `name=post_data.get(get_name(post_data.keys()),"N/A"),`
  * Do the same for the answer to a question of type "EMAIL": `email = post_data.get(get_email(post_data.keys()),"N/A")`
  * Derive the client name from the email:<pre>domain = email.split('@')[1]<br>client = domain.split('.')[0].upper()</pre>
* Create an Answer for each response to a question:
  * Loop through each active question and get a list of values from the post data that match its id: `values = request.POST.getlist(f'question_{q.id}')`
  * If the question's type is "MSELECT":
    * Get `other_detail` from the post data (for if the "Other" option was selected): `other_detail = request.POST.getlist(f'other_detail_{q.id}')[0]`
    * Store the value as a string of selected options seperated by ",". If the "Other" option was selected use a ":" to join "Other" with `other_detail` (e.g. `Push notifications, Other: audio quality`).
