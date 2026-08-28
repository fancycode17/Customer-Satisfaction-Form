from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def email_input(q): #<label for="email">{{ x.text }}</label>
    id = q.id
    help_text = q.help_text
    required = q.is_required
    html = f'''
    {f'<label for="{id}">{help_text}</label><br>' if help_text != '' else ''}
    <input type="email" id="{id}" name="{id}" placeholder="you@example.com"{' required' if required else ''}>'''

    return mark_safe(html)

@register.simple_tag
def short_text(q, placeholder='Type your answer'):
    id = q.id
    help_text = q.help_text
    required = q.is_required
    html = f'''
    {f'<label for="{id}">{help_text}</label><br>' if help_text != '' else ''}
    <input type="text" id="{id}" name="{id}" placeholder="{placeholder}"{' required' if required else ''}>'''

    return mark_safe(html)

@register.simple_tag
def long_text(q, rows=10, cols=60, placeholder='Type your answer'):
    id = q.id
    help_text = q.help_text
    required = q.is_required
    html = f'''
    {f'<label for="{id}">{help_text}</label><br>' if help_text != '' else ''}
    <textarea id="{id}" name="{id}" placeholder="{placeholder}" rows="{rows}" cols="{cols}"{' required' if required else ''}></textarea>'''

    return mark_safe(html)

@register.simple_tag
def rating_1_5(q):
    id = q.id
    help_text = q.help_text
    required = q.is_required
    html = f'''
    <input type="radio" id="r5" name="{id}" value="5"{' required' if required else ''}>
    <label for="r5">★★★★★</label><br>
    <input type="radio" id="r4" name="{id}" value="4"{' required' if required else ''}>
    <label for="r4">★★★★☆</label><br>
    <input type="radio" id="r3" name="{id}" value="3"{' required' if required else ''}>
    <label for="r3">★★★☆☆</label><br>
    <input type="radio" id="r2" name="{id}" value="2"{' required' if required else ''}>
    <label for="r2">★★☆☆☆</label><br>
    <input type="radio" id="r1" name="{id}" value="1"{' required' if required else ''}>
    <label for="r1">★☆☆☆☆</label>'''

    return mark_safe(html)

@register.simple_tag
def rating_1_10(q):
    id = q.id
    help_text = q.help_text
    required = q.is_required
    html = f'''
    {f'<label for="{id}">{help_text}</label><br>' if help_text != '' else ''}
    <input type="number" id="{id}" name="{id}" min="1" max="10" step="1"{' required' if required else ''}>'''

    return mark_safe(html)

@register.simple_tag
def multi_select(q):
    html = f''''''
    options = q.options.filter(is_active=True).order_by('display_order')
    for o in options:
        html += f'''
        <input type="checkbox" id="opt-{o.id}" name="{o.id}" value="{o.label}">
        <label for="opt-{o.id}"> {o.label}</label><br>
        '''
        if o.label.lower() == "other":
            html += f'''
            <div id="other-text-{o.id}" style="display:none; margin-left:20px;">
                <textarea id="other-detail-{o.id}" name="other_detail" cols="45" rows="5" placeholder="Please elaborate"></textarea>
            </div>
            <script>
            document.getElementById("opt-{o.id}").addEventListener("change", function() {{
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