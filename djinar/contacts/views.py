from django.views.generic import TemplateView


class ContactsView(TemplateView):
    """[summary]

    [description]
    """
    template_name = 'contacts.html'
    extra_context = {
        'contacts': [
            {
                "name": "Brunux",
                "label": "Cool Project",
                "email": "bruno.fosados@gmail.com",
                "phone": "3319441821",
                "company": "StackPath",
                "jobTitle": "Full stack developer",
                "notes": "Strong python developer"
            },
            {
                "name": "Brunux",
                "label": "Cool Project",
                "email": "bruno.fosados@gmail.com",
                "phone": "3319441821",
                "company": "StackPath",
                "jobTitle": "Full stack developer",
                "notes": "Strong python developer"
            },
            {
                "name": "Brunux",
                "label": "Cool Project",
                "email": "bruno.fosados@gmail.com",
                "phone": "3319441821",
                "company": "StackPath",
                "jobTitle": "Full stack developer",
                "notes": "Strong python developer"
            },
            {
                "name": "Brunux",
                "label": "Cool Project",
                "email": "bruno.fosados@gmail.com",
                "phone": "3319441821",
                "company": "StackPath",
                "jobTitle": "Full stack developer",
                "notes": "Strong python developer"
            },
            {
                "name": "Brunux",
                "label": "Cool Project",
                "email": "bruno.fosados@gmail.com",
                "phone": "3319441821",
                "company": "StackPath",
                "jobTitle": "Full stack developer",
                "notes": "Strong python developer"
            },
        ]
    }
