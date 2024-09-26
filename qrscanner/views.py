import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import AdminInput, User
from .qr import generate_qr_code

@api_view(['POST'])
def create_teams(request):
    num_students = request.data.get('num_students')
    num_teams = request.data.get('num_teams')
    if not num_students or not num_teams:
        return Response({'error': 'Please provide both number of students and teams.'}, status=status.HTTP_400_BAD_REQUEST)

    admin_input = AdminInput.objects.create(num_students=num_students, num_teams=num_teams)
    
    qr_code = generate_qr_code(admin_input.id)
    admin_input.qr_code.save(qr_code.name, qr_code)
    print(admin_input.qr_code.url)
    return Response({'message': 'QR Code generated', 'qr_code_url': admin_input.qr_code.url})


@api_view(['POST'])
def join_queue(request, admin_input_id):
    name = request.data.get('name')
    phone = request.data.get('phone')

    if not name or not phone:
        return Response({'error': 'Name and phone are required.'}, status=status.HTTP_400_BAD_REQUEST)

    admin_input = AdminInput.objects.get(id=admin_input_id)

    if User.objects.filter(admin_input=admin_input, name=name).exists():
        return Response({'error': 'A user with this name is already in the queue.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(admin_input=admin_input, phone=phone).exists():
        return Response({'error': 'A user with this phone number is already in the queue.'}, status=status.HTTP_400_BAD_REQUEST)

    queue_position = User.objects.filter(admin_input=admin_input).count() + 1

    if queue_position > admin_input.num_students:
        return Response({'error': 'Queue is already full.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(name=name, phone=phone, queue_position=queue_position, admin_input=admin_input)

    if queue_position == admin_input.num_students:
        assign_teams(admin_input)

    return Response({'message': 'You are in the queue', 'queue_position': queue_position})


def assign_teams(admin_input):
    users = list(User.objects.filter(admin_input=admin_input))
    random.shuffle(users)
    team_size = len(users) // admin_input.num_teams

    for i, user in enumerate(users):
        team_number = i // team_size + 1
        user.assigned_team = team_number
        user.save()



from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User

@api_view(['GET'])
def get_team_assignments(request, admin_input_id):
    # Fetch all users that match the given admin_input_id
    users = User.objects.filter(admin_input_id=admin_input_id).order_by('queue_position')

    # Prepare the response data
    data = []
    for user in users:
        # Get the team assigned to the current user
        current_team = user.assigned_team
        
        # Get all users in the same team (excluding the current user)
        same_team_users = User.objects.filter(admin_input_id=admin_input_id, assigned_team=current_team).exclude(id=user.id)

        # Get names of the other members in the same team
        same_team_members = [team_user.name for team_user in same_team_users]

        # Append the user data, including the names of the other team members
        data.append({
            'name': user.name,
            'phone': user.phone,
            'team': user.assigned_team,
            'same_team_members': same_team_members  # Names of users in the same team
        })

    # Return the response data
    return Response(data)

