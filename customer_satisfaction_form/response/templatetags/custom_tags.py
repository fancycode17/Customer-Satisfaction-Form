from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def email_input(q): #<label for="email">{{ x.text }}</label>
    id = f'question_{q.id}'
    help_text = q.help_text
    required = q.is_required
    submitted_data = "{{ submitted_data|get_item:'question_'|add:q.id }}"
    html = f'''
    {f'<label for="{id}">{help_text}</label><br>' if help_text != '' else ''}
    <input type="email" id="{id}" name="{id}" value="{{ submitted_data|get_item:'question_'|add:q.id }}" placeholder="you@example.com"{' required' if required else ''}>'''

    return mark_safe(html)

@register.inclusion_tag('widgets/short_text.html')
def short_text(q, submitted_data, placeholder='Type your answer'):
    return {
        'q': q,
        'value': submitted_data.get(f'question_{q.id}', ''),
        'placeholder': placeholder
    }

@register.simple_tag
def long_text(q, rows=10, cols=60, placeholder='Type your answer'):
    id = f'question_{q.id}'
    help_text = q.help_text
    required = q.is_required
    submitted_data = "{{ submitted_data|get_item:'question_'|add:q.id }}"
    html = f'''
    {f'<label for="{id}">{help_text}</label><br>' if help_text != '' else ''}
    <textarea id="{id}" name="{id}" placeholder="{placeholder}" rows="{rows}" cols="{cols}"{' required' if required else ''}>
    {{ submitted_data|get_item:'question_'|add:q.id }}
    </textarea>'''

    return mark_safe(html)

@register.simple_tag
def rating_1_5(q):
    id = f'question_{q.id}'
    help_text = q.help_text
    required = q.is_required
    submitted_data = "{{ submitted_data|get_item:'question_'|add:q.id }}"
    html = f'''
    <input type="radio" id="r5" name="{id}" value="5"{' required' if required else ''}{' checked' if submitted_data=='5' else ''}>
    <label for="r5">★★★★★</label><br>
    <input type="radio" id="r4" name="{id}" value="4"{' required' if required else ''}{' checked' if submitted_data=='4' else ''}>
    <label for="r4">★★★★☆</label><br>
    <input type="radio" id="r3" name="{id}" value="3"{' required' if required else ''}{' checked' if submitted_data=='3' else ''}>
    <label for="r3">★★★☆☆</label><br>
    <input type="radio" id="r2" name="{id}" value="2"{' required' if required else ''}{' checked' if submitted_data=='2' else ''}>
    <label for="r2">★★☆☆☆</label><br>
    <input type="radio" id="r1" name="{id}" value="1"{' required' if required else ''}{' checked' if submitted_data=='1' else ''}>
    <label for="r1">★☆☆☆☆</label>'''

    return mark_safe(html)

@register.simple_tag
def rating_1_10(q):
    id = f'question_{q.id}'
    help_text = q.help_text
    required = q.is_required
    submitted_data = "{{ submitted_data|get_item:'question_'|add:q.id }}"
    html = f'''
    {f'<label for="{id}">{help_text}</label><br>' if help_text != '' else ''}
    <input type="number" id="{id}" name="{id}" min="1" max="10" value="{{ submitted_data|get_item:'question_'|add:q.id }}" step="1"{' required' if required else ''}>'''

    return mark_safe(html)

@register.simple_tag
def multi_select(q):
    name = f"question_{q.id}"  # consistent key for all checkboxes in this question
    html = ""
    submitted_data = "{{ submitted_data|get_item:'question_'|add:q.id }}"
    options = q.options.filter(is_active=True).order_by("display_order")

    for o in options:
        checkbox_id = f"opt-{q.id}-{o.id}"  # unique per option
        html += f'''
        <input type="checkbox" 
        id="{checkbox_id}" 
        name="{name}" 
        value="{o.label}"
        {'checked' if o.label in submitted_data else ''}>
        <label for="{checkbox_id}"> {o.label}</label><br>
        '''
        if o.label.lower() == "other":
            submitted_data = '{{ submitted_data.other_detail_q.id }}'
            html += f'''
            <div id="other-text-{o.id}" style="display:none; margin-left:20px;">
                <textarea id="other-detail-{o.id}" name="other_detail_{q.id}" cols="45" rows="5" placeholder="Please elaborate">
                {submitted_data}
                </textarea>
            </div>
            <script>
            document.getElementById("{checkbox_id}").addEventListener("change", function() {{
                const box = document.getElementById("other-text-{o.id}");
                const input = document.getElementById("other-detail-{o.id}");
                if (this.checked) {{
                    box.style.display = "block";
                    input.setAttribute("required", "required");
                }} else {{
                    box.style.display = "none";
                    input.removeAttribute("required");
                }}
            }});
            </script>
            '''

    return mark_safe(html)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)