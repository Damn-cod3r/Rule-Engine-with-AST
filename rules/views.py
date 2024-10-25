from rest_framework.decorators import api_view
from rest_framework.response import Response
from .logic import create_rule, combine_rules, evaluate_rule
from .models import Node
from .serializers import NodeSerializer

@api_view(['POST'])
def create_rule_view(request):
    rule_string = request.data.get('rule_string')
    root_node = create_rule(rule_string)
    return Response(NodeSerializer(root_node).data)

@api_view(['POST'])
def combine_rules_view(request):
    rule_strings = request.data.get('rules', [])
    root_node = combine_rules(rule_strings)
    return Response(NodeSerializer(root_node).data)

@api_view(['POST'])
def evaluate_rule_view(request):
    ast_data = request.data.get('ast')
    user_data = request.data.get('user_data')
    if not ast_data or not user_data:
        return Response({"error": "Invalid input"}, status=400)

    try:
        node_id = ast_data['id']
        node = Node.objects.get(id=node_id)
        is_eligible = evaluate_rule(node, user_data)
    except Node.DoesNotExist:
        return Response({"error": "Rule not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

    return Response({"eligible": is_eligible})
