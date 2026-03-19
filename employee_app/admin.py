
from django.contrib import admin
from .models import Department, Designation, Employee ,LeaveRequest

# இதனால் Admin Panel‑ல் Table‑கள் காட்டும்
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Employee)
admin.site.register(LeaveRequest)