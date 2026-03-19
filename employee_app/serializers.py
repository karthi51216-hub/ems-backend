

from rest_framework import serializers
from .models import Department, Designation, Employee, LeaveRequest


class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField()
    total_salary = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'employee_count', 'total_salary', 'created_at']

    def get_employee_count(self, obj):
        return obj.employees.filter(status='active').count()

    def get_total_salary(self, obj):
        from django.db.models import Sum
        total = obj.employees.filter(status='active').aggregate(total=Sum('salary'))['total']
        return total or 0


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'


class EmployeeListSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    designation_title = serializers.CharField(source='designation.title', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id',
            'employee_id',
            'full_name',
            'email',
            'phone',
            'department',
            'department_name',
            'designation',
            'designation_title',
            'salary',
            'date_of_joining',
            'status',
            'profile_photo'
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class EmployeeDetailSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    designation_title = serializers.CharField(source='designation.title', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id',
            'employee_id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone',
            'salary',
            'date_of_birth',
            'date_of_joining',
            'gender',
            'address',
            'city',
            'state',
            'pincode',
            'emergency_contact_name',
            'emergency_contact_phone',
            'emergency_contact_relation',
            'department',
            'department_name',
            'designation',
            'designation_title',
            'status',
            'profile_photo',
            'created_at',
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class EmployeeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'employee_id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'date_of_birth',
            'gender',
            'address',
            'city',
            'state',
            'pincode',
            'emergency_contact_name',
            'emergency_contact_phone',
            'emergency_contact_relation',
            'department',
            'designation',
            'date_of_joining',
            'salary',
            'profile_photo',
            'status'
        ]

    def validate_employee_id(self, value):
        if value:
            if self.instance:
                if Employee.objects.exclude(pk=self.instance.pk).filter(employee_id=value).exists():
                    raise serializers.ValidationError("Employee ID already exists")
            else:
                if Employee.objects.filter(employee_id=value).exists():
                    raise serializers.ValidationError("Employee ID already exists")
        return value


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = LeaveRequest
        fields = [
            'id',
            'employee',
            'employee_name',
            'leave_type',
            'from_date',
            'to_date',
            'reason',
            'status',
            'created_at',
        ]

    def get_employee_name(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}"