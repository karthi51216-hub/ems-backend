

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum

from .models import Department, Designation, Employee, LeaveRequest
from .serializers import (
    DepartmentSerializer,
    DesignationSerializer,
    EmployeeListSerializer,
    EmployeeDetailSerializer,
    EmployeeCreateUpdateSerializer,
    LeaveRequestSerializer,
)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    permission_classes = [IsAuthenticated]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('department', 'designation').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email', 'employee_id', 'phone']
    ordering_fields = ['date_of_joining', 'salary', 'created_at', 'first_name']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EmployeeCreateUpdateSerializer
        elif self.action == 'list':
            return EmployeeListSerializer
        return EmployeeDetailSerializer

    def get_queryset(self):
        queryset = Employee.objects.select_related('department', 'designation').all()

        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        department = self.request.query_params.get('department')
        if department:
            queryset = queryset.filter(department_id=department)

        designation = self.request.query_params.get('designation')
        if designation:
            queryset = queryset.filter(designation_id=designation)

        return queryset

    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        total_employees = Employee.objects.count()
        active_employees = Employee.objects.filter(status='active').count()
        total_departments = Department.objects.count()
        total_salary = Employee.objects.filter(status='active').aggregate(
            total=Sum('salary')
        )['total'] or 0

        recent = Employee.objects.order_by('-created_at')[:5]

        return Response({
            'total_employees': total_employees,
            'active_employees': active_employees,
            'total_departments': total_departments,
            'total_salary': total_salary,
            'recent_employees': EmployeeListSerializer(recent, many=True).data
        })

    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            employee = Employee.objects.get(email=request.user.email)
            serializer = EmployeeDetailSerializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response(
                {'error': 'Employee profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    stats = {
        'total_employees': Employee.objects.filter(status='active').count(),
        'total_departments': Department.objects.count(),
        'total_salary': Employee.objects.filter(status='active').aggregate(
            total=Sum('salary')
        )['total'] or 0
    }
    return Response(stats)


class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.select_related('employee').all().order_by('-created_at')
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['employee__first_name', 'employee__last_name', 'leave_type', 'status']
    ordering_fields = ['from_date', 'to_date', 'created_at']