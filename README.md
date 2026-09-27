# customer-satisfaction-form

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
